import asyncio,os,json
os.environ['WEBDIR']='/tmp/webT'
src=open('/home/claude/firebase/fbtest.py').read().split('async def main():')[0].replace('PORT=8765','PORT=8873')
exec(src)
async def main():
    errs=[]
    async with async_playwright() as pw:
        b=await pw.chromium.launch();p=await newpage(b,errs,'s');await asyncio.sleep(3)
        r=await p.evaluate("""()=>window.__T.ev(`(()=>{const SS=seasonOf(Date.now());const R=rankCalc(SS,null,[],[],null,Date.now());const bots=R.list.filter(p=>p.bot);
          const g=bots.map(p=>p.g-80>0?p.g:0);const since=bots.map(p=>p.w+p.l+p.d);const moved=bots.filter(p=>Math.abs(p.r-BOT_R0.get(p.bot.id))>0.5).length;
          return JSON.stringify({now:new Date().toISOString(),hours:((Date.now()-BOT_RESET)/36e5).toFixed(1),bots:bots.length,moved,gamesAfterReset:Math.round(((Date.now()-BOT_RESET)/36e5)*BOT_GPH),top:bots.slice(0,5).map(p=>[p.nick,Math.round(p.r),p.w+'승'+p.l+'패'])})})()`)""")
        print(r);await b.close()
asyncio.run(main())
