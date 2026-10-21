import React from 'react';
import {AbsoluteFill,Composition,registerRoot,useCurrentFrame,useVideoConfig} from 'remotion';
const defaults={
tech:{background:'#101827',foreground:'#f5f7ff',muted:'#a5b5cc',accent:'#42cfb0',transition:'#4577d4'},
travel:{background:'#f4eee4',foreground:'#493c35',muted:'#817267',accent:'#b17e49',transition:'#83a88f'},
game:{background:'#201435',foreground:'#fff5f1',muted:'#cbb5e5',accent:'#f3b652',transition:'#ec72ac'},
minimal:{background:'#121212',foreground:'#ffffff',muted:'#b6b6b6',accent:'#ffffff',transition:'#b6b6b6'}
};
const hex=s=>typeof s==='string'&&/^#[0-9a-fA-F]{6}$/.test(s);
function colors(design){
const preset=defaults[design?.theme]||defaults.tech;
const d={...preset,...Object.fromEntries(Object.entries(design||{}).filter(([k,v])=>['background','foreground','muted','accent','transition'].includes(k)&&hex(v)))};
if(!hex(design?.transition)&&Array.isArray(design?.segmentColors)&&design.segmentColors.length>0&&design.segmentColors.every(hex))d.transition=design.segmentColors[0];
return d;
}
export function Timeline({chapters,durationMs,design={}}){
const frame=useCurrentFrame(),{fps}=useVideoConfig(), now=frame/fps*1000;
const d=colors(design), active=chapters.findIndex(c=>now>=c.startMs&&now<c.endMs);
const chapterIndex=Math.max(0,active),current=chapters[chapterIndex];
const format=s=>String(Math.floor(s/60)).padStart(2,'0')+':'+String(Math.floor(s%60)).padStart(2,'0');
return <AbsoluteFill style={{background:d.background,color:d.foreground,fontFamily:'Arial,"Noto Sans CJK SC","PingFang SC",sans-serif',padding:'0 24px',boxSizing:'border-box',overflow:'hidden',justifyContent:'center'}}>
<div style={{display:'flex',flexDirection:'column',gap:11}}>
<div style={{display:'flex',justifyContent:'space-between',alignItems:'center',height:30,gap:16,minWidth:0}}>
<div style={{display:'flex',alignItems:'center',gap:11,minWidth:0,flex:1}}>
<span style={{fontSize:11,fontWeight:700,letterSpacing:1,color:d.accent,border:`1px solid ${d.accent}66`,background:`${d.accent}18`,borderRadius:999,padding:'5px 9px',whiteSpace:'nowrap',fontVariantNumeric:'tabular-nums'}}>{String(chapterIndex+1).padStart(2,'0')} / {String(chapters.length).padStart(2,'0')}</span>
<span style={{fontSize:19,fontWeight:700,whiteSpace:'nowrap',overflow:'hidden',textOverflow:'ellipsis',minWidth:0}}>{current?.title||'章节导航'}</span>
</div>
<span style={{fontSize:14,color:d.muted,fontVariantNumeric:'tabular-nums',flexShrink:0,whiteSpace:'nowrap'}}>{format(now/1000)} / {format(durationMs/1000)}</span>
</div>
<div style={{display:'flex',width:'calc(100% + 48px)',height:13,gap:3,marginLeft:-24}}>
{chapters.map((c,i)=>{
const ratio=(c.endMs-c.startMs)/durationMs;
const fill=Math.max(0,Math.min(1,(now-c.startMs)/(c.endMs-c.startMs)));
return <div key={i} style={{flex:ratio,minWidth:0,overflow:'hidden',background:d.muted+'25',borderRadius:4,border:`1px solid ${d.muted}20`,boxSizing:'border-box'}}>
<div style={{width:fill*100+'%',height:'100%',background:i===chapterIndex?`linear-gradient(90deg, ${d.accent}, ${d.transition})`:d.accent}}/>
</div>;})}
</div>
</div>
</AbsoluteFill>;
}
const sample={chapters:[{title:'开始',startMs:0,endMs:5000},{title:'结束',startMs:5000,endMs:10000}],durationMs:10000,design:{}};
registerRoot(()=> <Composition id="Chaptr" component={Timeline} width={1920} height={104} fps={30} durationInFrames={Math.ceil(sample.durationMs/1000*30)} calculateMetadata={({props})=>({durationInFrames:Math.max(1,Math.ceil(props.durationMs/1000*30)),width:props.videoWidth||1920,height:104})} defaultProps={sample}/>);
