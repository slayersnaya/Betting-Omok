import asyncio,os,json
os.environ['WEBDIR']='/tmp/webT'
src=open('/home/claude/firebase/fbtest.py').read().split('async def main():')[0].replace('PORT=8765','PORT=8833')
exec(src)
async def main():
    async with async_playwright() as pw:
        b=await pw.chromium.launch();errs=[]
        p=await newpage(b,errs,'x');await asyncio.sleep(1.5)
        out={}
        for d in (1,30,60,94):
            r=await p.evaluate("""d=>{const n0=Date.now;const off=d*864e5;Date.now=()=>n0.call(Date)+off;const T=window.__T;T.rankCompute();Date.now=n0;
              return T.RK.list.filter(p=>p.bot).map(p=>[T.ev('BOTMAP').get(p.seat.slice(4)).k,Math.round(p.r)])}""",d)
            out[d]=r
        json.dump(out,open('/tmp/bt/botr.json','w'));print({d:len(v) for d,v in out.items()});await b.close()
asyncio.run(main())
