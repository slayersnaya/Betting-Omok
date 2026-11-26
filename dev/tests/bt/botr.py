import asyncio,os,json
os.environ['WEBDIR']='/tmp/webT'
src=open('/home/claude/firebase/fbtest.py').read().split('async def main():')[0].replace('PORT=8765','PORT=8866')
exec(src)
async def main():
    errs=[]
    async with async_playwright() as pw:
        b=await pw.chromium.launch();p=await newpage(b,errs,'성민');await asyncio.sleep(4)
        r=await p.evaluate("""()=>window.__T.ev(`(()=>{const SS=seasonOf(Date.now());const out={};
          for(const [lab,at] of [['now',Date.now()],['+1d',Date.now()+864e5],['+7d',Date.now()+7*864e5],['+30d',Date.now()+30*864e5],['+90d',Date.UTC(2027,1,28)]]){
            const R=rankCalc(SS,null,[],[],null,at);const bots=R.list.filter(p=>p.bot);const cnt={};for(const p of bots){const t=tierOf(p);cnt[t.n]=(cnt[t.n]||0)+1}
            out[lab]={n:bots.length,max:Math.round(bots[0].r),min:Math.round(bots[bots.length-1].r),top:bots.slice(0,3).map(p=>p.nick+' '+Math.round(p.r)),tiers:cnt}}
          return JSON.stringify(out)})()`)""")
        for k,v in json.loads(r).items(): print(k,v)
        print('errors',[e for e in errs if 'ERR_' not in e]);await b.close()
asyncio.run(main())
