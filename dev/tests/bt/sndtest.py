import asyncio,os,json,base64,struct
os.environ['WEBDIR']='/tmp/webT'
src=open('/home/claude/firebase/fbtest.py').read().split('async def main():')[0].replace('PORT=8765','PORT=8869')
exec(src)
JS="""async()=>{const T=window.__T;const keys=T.ev('Object.keys(SND)');const out={};
 for(const k of keys){const sr=44100,oc=new OfflineAudioContext(1,sr*2.2,sr);
  T.ev('actx=null');window.__oc=oc;T.ev(`(()=>{actx=window.__oc;SNDM=actx.createGain();SNDM.connect(actx.destination);const n=actx.createBuffer(1,actx.sampleRate*.5,actx.sampleRate),d=n.getChannelData(0);for(let i=0;i<d.length;i++)d[i]=Math.random()*2-1;SNDN=n})()`);
  T.ev(`snd('${k}',0)`);const buf=await oc.startRendering();const d=buf.getChannelData(0);let pk=0,ss=0,last=0;for(let i=0;i<d.length;i++){const a=Math.abs(d[i]);if(a>pk)pk=a;ss+=d[i]*d[i];if(a>.002)last=i}
  const n=last+1000<d.length?last+1000:d.length;const pcm=new Int16Array(n);for(let i=0;i<n;i++)pcm[i]=Math.max(-1,Math.min(1,d[i]))*32767;
  let bin='';const u8=new Uint8Array(pcm.buffer);for(let i=0;i<u8.length;i++)bin+=String.fromCharCode(u8[i]);
  out[k]={pk:+pk.toFixed(3),rms:+Math.sqrt(ss/d.length).toFixed(4),len:+(last/sr).toFixed(2),b64:btoa(bin)}}
 return JSON.stringify(out)}"""
async def main():
    errs=[]
    async with async_playwright() as pw:
        b=await pw.chromium.launch();p=await newpage(b,errs,'s');await asyncio.sleep(2)
        r=json.loads(await p.evaluate(JS));os.makedirs('/tmp/snd',exist_ok=True)
        for k,v in r.items():
            pcm=base64.b64decode(v['b64']);hdr=b'RIFF'+struct.pack('<I',36+len(pcm))+b'WAVEfmt '+struct.pack('<IHHIIHH',16,1,1,44100,88200,2,16)+b'data'+struct.pack('<I',len(pcm))
            open(f'/tmp/snd/{k}.wav','wb').write(hdr+pcm)
            flag='' if 0.03<v['pk']<0.99 else '  <-- CHECK'
            print(f"{k:10s} peak {v['pk']:.3f} len {v['len']:.2f}s{flag}")
        print('errors',len([e for e in errs if 'ERR_' not in e]));json.dump({k:v['pk'] for k,v in r.items()},open('/tmp/snd/peaks.json','w'));await b.close()
asyncio.run(main())
