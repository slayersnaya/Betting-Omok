import asyncio,os
os.environ['WEBDIR']='/tmp/webT'
src=open('/home/claude/firebase/fbtest.py').read().split('async def main():')[0].replace('PORT=8765','PORT=8834')
exec(src)
async def main():
    async with async_playwright() as pw:
        b=await pw.chromium.launch();errs=[]
        p=await newpage(b,errs,'x');await asyncio.sleep(1.5)
        print(await p.evaluate("""()=>{const f=window.__T.ev('rkLvFor');const o={};for(const r of [850,1000,1200,1400,1600])for(const wr of [null,.3,.7]){const c={};for(let i=0;i<2000;i++){const l=f(r,Math.random(),wr);c[l]=(c[l]||0)+1}o[r+'/'+wr]=JSON.stringify(c)}return o}"""))
        print('errors',[e for e in errs if 'ERR_' not in e]);await b.close()
asyncio.run(main())
