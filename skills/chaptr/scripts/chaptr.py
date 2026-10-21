#!/usr/bin/env python3
"""Chaptr CLI: deterministic video fetching, chapter validation and compositing."""
import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

# The reusable JZSub media and subtitle logic lives directly in Chaptr.
# Python executes this file's directory on sys.path for normal CLI invocation.
import media_fetch
import subtitle_source

def digest(data):
    return hashlib.sha256(data).hexdigest()

def save(path, data):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    tmp=path.with_suffix(path.suffix+'.tmp')
    tmp.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    tmp.replace(path)

def load(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))

def command(args, capture=False):
    p=subprocess.run(args,check=False,text=True,stdout=subprocess.PIPE if capture else None,stderr=subprocess.PIPE if capture else None)
    if p.returncode:
        raise ValueError(f'{args[0]} failed: '+(p.stderr or '')[-500:])
    return p.stdout if capture else None

def probe(video):
    obj=json.loads(command(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(video)],True))
    v=next((s for s in obj['streams'] if s.get('codec_type')=='video'),None)
    if v is None:raise ValueError('No video stream')
    sec=float(obj['format'].get('duration') or v.get('duration') or 0)
    if sec<=0:raise ValueError('Unknown video duration')
    return {'durationMs':round(sec*1000),'width':int(v['width']),'height':int(v['height']),'hasAudio':any(s.get('codec_type')=='audio' for s in obj['streams'])}

def srt_time(text):
    m=re.fullmatch(r'(\d+):(\d\d):(\d\d)[,.](\d{3})',text.strip())
    if not m:raise ValueError('Invalid SRT time '+text)
    a,b,c,d=map(int,m.groups())
    if b>=60 or c>=60:raise ValueError('Invalid minute/second')
    return ((a*60+b)*60+c)*1000+d

def parse_srt(raw):
    # Reuse JZSub's strict SRT grammar, filtering and hashed Cue Ledger.
    pipeline = subtitle_source
    parsed = pipeline.parse_srt_bytes(raw)
    ledger = pipeline._build_cue_ledger(parsed)
    if not ledger:
        raise ValueError("No dialogue cues after JZSub filtering")
    return [
        {
            "id": f"cue-{i+1:06d}",
            "upstreamCueId": item["id"],
            "cueSha256": item["cue_sha256"],
            "textSha256": item["text_sha256"],
            "startMs": item["start_ms"],
            "endMs": item["end_ms"],
            "text": item["text"],
        }
        for i,item in enumerate(ledger)
    ]

def prepare(video,srt,job):
    video=Path(video).resolve();srt=Path(srt).resolve();job=Path(job).resolve()
    if (job/'manifest.json').exists():raise ValueError('Job already initialized')
    raw=srt.read_bytes();cues=parse_srt(raw);media=probe(video)
    if cues[-1]['startMs']>=media['durationMs']:raise ValueError('Subtitle exceeds video')
    save(job/'manifest.json',{'video':str(video),'srt':str(srt),'sourceSha256':digest(raw),**media})
    save(job/'cues.json',{'sourceSha256':digest(raw),'cues':cues})
    batches=[]
    for start in range(0,len(cues),70):
        idx=len(batches)+1
        selected=cues[start:start+70]
        output=job/'analysis'/f'batch-{idx:04d}.json'
        payload={'items':selected,'contextBefore':cues[max(0,start-2):start],'contextAfter':cues[start+70:start+72]}
        save(job/'batches'/f'batch-{idx:04d}.json',payload)
        batches.append({'input':str(job/'batches'/f'batch-{idx:04d}.json'),'output':str(output),'ids':[c['id'] for c in selected]})
    save(job/'batches.json',{'batches':batches})
    return {'cues':len(cues),'batches':len(batches),**media}

def fetch(url,job, browser_cookies="auto", source_lang=None):
    """Delegate probing, authentication, format selection and subtitle extraction to JZSub."""
    job = Path(job).resolve()
    job.mkdir(parents=True, exist_ok=True)
    if any(job.iterdir()):
        raise ValueError("Job directory must be empty")
    fetcher = media_fetch
    args = fetcher.build_parser().parse_args([
        url, "--output-dir", str(job / "source"),
        "--deliver", "video",
        "--target-lang", "zz",  # No language exclusion: Chaptr needs source captions in any language.
        "--browser-cookies", browser_cookies,
        *(['--source-lang', source_lang] if source_lang else []),
    ])
    result = fetcher.execute(args)
    if result is None:
        raise ValueError("JZSub did not return a download manifest")
    info = load(result)
    artifacts = info.get("artifacts") or {}
    subtitle = artifacts.get("subtitle") or {}
    record = subtitle.get("source_srt") or {}
    base = Path(result).parent

    def existing(record):
        if not isinstance(record, dict) or not record.get("path"):
            return None
        path = Path(record["path"])
        if not path.is_absolute():
            path = base / path
        return path.resolve() if path.is_file() else None

    video = next(
        (p for p in [
            existing(artifacts.get("lossless_mp4_master")),
            existing(artifacts.get("intermediate")),
            existing((artifacts.get("lossy_mp4_fallback") or {}).get("created")),
        ] if p), None
    )
    srt = existing(record)
    if not video or not srt:
        raise ValueError("JZSub did not provide video and usable source SRT; Chaptr v0.2 requires subtitles")
    result = prepare(video,srt,job)
    manifest = load(job / "manifest.json")
    manifest["sourceDownloadManifest"] = str(Path(base / "download-manifest.json").resolve())
    manifest["subtitleLanguage"] = subtitle.get("language")
    manifest["subtitleKind"] = subtitle.get("kind")
    save(job / "manifest.json", manifest)
    return {"mediaCore": "JZSub-derived", "downloadManifest": str(base / "download-manifest.json"), **result}

def next_batch(job):
    job=Path(job).resolve();manifest=load(job/'manifest.json')
    if digest(Path(manifest['srt']).read_bytes())!=manifest['sourceSha256']:raise ValueError('Source changed')
    batches=load(job/'batches.json')['batches']
    for b in batches:
        output=Path(b['output'])
        if not output.exists():
            return {'done':False,'outputPath':str(output),'batch':load(b['input'])}
        row=load(output)
        if not isinstance(row.get('summary'),str) or not isinstance(row.get('boundaries'),list):raise ValueError('Invalid analysis')
        if any(not isinstance(v,dict) or v.get('cueId') not in b['ids'] for v in row['boundaries']):raise ValueError('Invalid cue boundary')
    return {'done':True,'analyses':[load(x['output']) for x in batches]}

def finalize(job):
    job=Path(job).resolve()
    if not next_batch(job)['done']:raise ValueError('Incomplete semantic analysis')
    manifest=load(job/'manifest.json');cues=load(job/'cues.json')['cues']
    src=load(job/'chapters.json')
    rows=src.get('chapters')
    if src.get('schemaVersion')!=1 or not isinstance(rows,list) or not (1<=len(rows)<=30):raise ValueError('Invalid chapter schema')
    byid={c['id']:c for c in cues}
    if rows[0].get('startCueId')!=cues[0]['id']:raise ValueError('First chapter must start at first cue')
    resolved=[];prev=-1
    for i,row in enumerate(rows):
        cid=row.get('startCueId');title=row.get('title')
        if cid not in byid or not isinstance(title,str) or not title.strip() or len(title)>32:raise ValueError('Invalid chapter')
        start=0 if i==0 else byid[cid]['startMs']
        if start<=prev or start>=manifest['durationMs']:raise ValueError('Invalid chapter order')
        resolved.append({'title':title.strip(),'startCueId':cid,'startMs':start})
        prev=start
    for i,row in enumerate(resolved):
        row['endMs']=resolved[i+1]['startMs'] if i+1<len(resolved) else manifest['durationMs']
        if row['endMs']<=row['startMs']:raise ValueError('Empty chapter')
    result={'schemaVersion':1,'durationMs':manifest['durationMs'],'chapters':resolved}
    save(job/'chapters.resolved.json',result)
    return result

def compose(job):
    job=Path(job).resolve();manifest=load(job/'manifest.json')
    overlay=job/'timeline.mp4'
    if not overlay.exists():raise ValueError('Missing timeline; run Remotion first')
    destination=job/'chaptr.mp4'
    if destination.exists():raise ValueError('Output exists; remove explicitly before recomposing')
    # Scale the source to exactly 1920 wide and preserve display ratio; lower panel adds 104 pixels.
    # Audio may be copied when the original codec is compatible with MP4.
    info=probe(manifest['video'])
    height=round(info['height']*1920/info['width']/2)*2
    filters=f'[0:v:0]scale=1920:{height}:flags=lanczos,setsar=1[top];[top][1:v:0]vstack=inputs=2:shortest=1[v]'
    opts=['-c:a','copy'] if info['hasAudio'] else ['-an']
    args=['ffmpeg','-hide_banner','-loglevel','error','-y','-i',manifest['video'],'-i',str(overlay),'-filter_complex',filters,'-map','[v]']
    if info['hasAudio']:args+=['-map','0:a:0']
    args+=['-c:v','libx264','-crf','18','-preset','medium','-pix_fmt','yuv420p',*opts,'-movflags','+faststart','-shortest',str(destination)]
    try:command(args)
    except ValueError:
        if not info['hasAudio']:raise
        args[args.index('copy')]='aac';args[args.index('aac')+1:args.index('aac')+1]=['-b:a','192k']
        command(args)
    return {'output':str(destination)}

def verify(job):
    job=Path(job).resolve()
    target=job/'chaptr.mp4'
    if not target.is_file() or target.stat().st_size==0:raise ValueError('Missing output')
    source=load(job/'manifest.json');result=probe(target)
    if abs(result['durationMs']-source['durationMs'])>1200:raise ValueError('Unexpected output duration')
    if result['width']!=1920:raise ValueError('Unexpected output dimensions')
    if source['hasAudio'] and not result['hasAudio']:raise ValueError('Missing original audio')
    return {'verified':True,'output':str(target),**result}

def main():
    p=argparse.ArgumentParser();sub=p.add_subparsers(dest='command',required=True)
    a=sub.add_parser('fetch');a.add_argument('url');a.add_argument('--job',required=True);a.add_argument('--browser-cookies',default='auto');a.add_argument('--source-lang')
    a=sub.add_parser('prepare');a.add_argument('--video',required=True);a.add_argument('--srt',required=True);a.add_argument('--job',required=True)
    for name in ['next-batch','finalize','compose','verify']:
        a=sub.add_parser(name);a.add_argument('--job',required=True)
    a=p.parse_args()
    try:
        if a.command=='fetch':result=fetch(a.url,a.job,a.browser_cookies,a.source_lang)
        elif a.command=='prepare':result=prepare(a.video,a.srt,a.job)
        elif a.command=='next-batch':result=next_batch(a.job)
        elif a.command=='finalize':result=finalize(a.job)
        elif a.command=='compose':result=compose(a.job)
        else:result=verify(a.job)
        print(json.dumps(result,ensure_ascii=False,indent=2))
    except (ValueError,FileNotFoundError,subprocess.SubprocessError,RuntimeError) as e:
        print(f'chaptr: {e}',file=sys.stderr);sys.exit(1)
if __name__=='__main__':main()
