import React from 'react';
import {AbsoluteFill,Composition,interpolate,registerRoot,useCurrentFrame,useVideoConfig,Easing} from 'remotion';
const defaults={
tech:{background:'#101827',foreground:'#f5f7ff',muted:'#a5b5cc',accent:'#42cfb0',segmentColors:['#4577d4','#986deb','#42cfb0','#f3b652']},
travel:{background:'#f4eee4',foreground:'#493c35',muted:'#817267',accent:'#b17e49',segmentColors:['#c68d59','#83a88f','#79a8b6','#d4a184']},
game:{background:'#201435',foreground:'#fff5f1',muted:'#cbb5e5',accent:'#f3b652',segmentColors:['#ad69f0','#ec72ac','#f3b652','#54d5d5']},
minimal:{background:'#121212',foreground:'#ffffff',muted:'#b6b6b6',accent:'#ffffff',segmentColors:['#ededed']}
};
const hex=s=>typeof s==='string'&&/^#[0-9a-fA-F]{6}$/.test(s);
function colors(design){
const preset=defaults[design?.theme]||defaults.tech;
const d={...preset,...Object.fromEntries(Object.entries(design||{}).filter(([k,v])=>['background','foreground','muted','accent'].includes(k)&&hex(v)))};
if(Array.isArray(design?.segmentColors)&&design.segmentColors.length>0&&design.segmentColors.length<=20&&design.segmentColors.every(hex))d.segmentColors=design.segmentColors;
return d;
}
export function Timeline({chapters,durationMs,design={}}){
const frame=useCurrentFrame(),{fps}=useVideoConfig(), now=frame/fps*1000;
const d=colors(design), active=chapters.findIndex(c=>now>=c.startMs&&now<c.endMs);
const current=chapters[Math.max(0,active)];
const progress=Math.min(1,Math.max(0,now/durationMs));
const format=s=>String(Math.floor(s/60)).padStart(2,'0')+':'+String(Math.floor(s%60)).padStart(2,'0');
const shown=design.motion==='linear'?progress:progress; // time mapping is always linear; motion never distorts timestamps
return <AbsoluteFill style={{background:d.background,color:d.foreground,fontFamily:'Arial,"Noto Sans CJK SC","PingFang SC",sans-serif',padding:'12px 24px',boxSizing:'border-box',overflow:'hidden'}}>
<div style={{display:'flex',justifyContent:'space-between',alignItems:'center',height:26,gap:10}}>
<span style={{fontSize:19,fontWeight:700,whiteSpace:'nowrap',overflow:'hidden',textOverflow:'ellipsis'}}>{current?.title||'章节导航'}</span>
<span style={{fontSize:14,color:d.muted,fontVariantNumeric:'tabular-nums',flexShrink:0}}>{format(now/1000)} / {format(durationMs/1000)}</span>
</div>
<div style={{display:'flex',width:'100%',height:15,gap:3,marginTop:8}}>
{chapters.map((c,i)=>{
const ratio=(c.endMs-c.startMs)/durationMs;
const fill=Math.max(0,Math.min(1,(now-c.startMs)/(c.endMs-c.startMs)));
return <div key={i} style={{flex:ratio,minWidth:0,overflow:'hidden',background:d.muted+'40',borderRadius:3}}>
<div style={{width:fill*100+'%',height:'100%',background:d.segmentColors[i%d.segmentColors.length]}}/>
</div>;})}
</div>
<div style={{display:'flex',width:'100%',gap:3,marginTop:5}}>
{chapters.map((c,i)=><div key={i} style={{flex:(c.endMs-c.startMs)/durationMs,minWidth:0,fontSize:13,fontWeight:i===active?700:400,opacity:i===active?1:0.67,whiteSpace:'nowrap',overflow:'hidden',textOverflow:'ellipsis'}}>{c.title}</div>)}
</div>
</AbsoluteFill>;
}
const sample={chapters:[{title:'开始',startMs:0,endMs:5000},{title:'结束',startMs:5000,endMs:10000}],durationMs:10000,design:{}};
registerRoot(()=> <Composition id="Chaptr" component={Timeline} width={1920} height={104} fps={30} durationInFrames={Math.ceil(sample.durationMs/1000*30)} calculateMetadata={({props})=>({durationInFrames:Math.max(1,Math.ceil(props.durationMs/1000*30)),width:props.videoWidth||1920,height:104})} defaultProps={sample}/>);
