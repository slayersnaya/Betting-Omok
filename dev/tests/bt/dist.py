import asyncio,os
os.environ['WEBDIR']='/tmp/webT'
src=open('/home/claude/firebase/fbtest.py').read().split('async def main():')[0].replace('PORT=8765','PORT=8832')
exec(src)
async def main():
    async with async_playwright() as pw:
        b=await pw.chromium.launch();errs=[]
        p=await newpage(b,errs,'x');await asyncio.sleep(1.5)
        for d in (0,1,7,30,60,94):
            r=await p.evaluate("""d=>{const n0=Date.now;const off=d*864e5;Date.now=()=>n0.call(Date)+off;const T=window.__T;T.rankCompute();Date.now=n0;
              const c={};T.RK.list.forEach(p=>{const t=T.tierOf(p);c[t.n]=(c[t.n]||0)+1});const rs=T.RK.list.filter(p=>p.bot).map(p=>p.r-p.bot.base);
              return [c,Math.round(Math.max(...rs)),Math.round(Math.min(...rs)),T.RK.list.slice(0,3).map(p=>p.nick+' '+Math.round(p.r)).join(', ')]}""",d)
            print(d,'일 후',r)
        await b.close()
asyncio.run(main())
