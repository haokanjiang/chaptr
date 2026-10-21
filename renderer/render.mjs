import fs from 'node:fs/promises';
import path from 'node:path';
import {bundle} from '@remotion/bundler';
import {renderMedia,selectComposition} from '@remotion/renderer';

const ix=process.argv.indexOf('--job');
if(ix<0||!process.argv[ix+1]) throw new Error('Usage: node render.mjs --job ABSOLUTE_JOB');
const job=path.resolve(process.argv[ix+1]);
const manifest=JSON.parse(await fs.readFile(path.join(job,'manifest.json'),'utf8'));
const chapters=JSON.parse(await fs.readFile(path.join(job,'chapters.resolved.json'),'utf8'));
let design={};
try{design=JSON.parse(await fs.readFile(path.join(job,'timeline-design.json'),'utf8'));}catch(e){if(e.code!=='ENOENT')throw e;}
const inputProps={chapters:chapters.chapters, durationMs:manifest.durationMs,design};
const serveUrl=await bundle({entryPoint:path.resolve('src/index.jsx')});
const composition=await selectComposition({serveUrl,id:'Chaptr',inputProps});
const output=path.join(job,'timeline.mp4');
await renderMedia({serveUrl,composition,inputProps,outputLocation:output,codec:'h264',pixelFormat:'yuv420p',crf:17,concurrency:2});
console.log(output);
