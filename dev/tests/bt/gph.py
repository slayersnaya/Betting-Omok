import asyncio,os,json,shutil,re,sys
src=open('/home/claude/firebase/fbtest.py').read().split('async def main():')[0].replace('PORT=8765','PORT=8868')
os.environ['WEBDIR']='/tmp/webV'
exec(src)
JS="""()=>window.__T.ev(`(()=>{const SS=seasonOf(Date.now());const out={};
 for(const [lab,at] of [['+30d',Date.now()+30*864e5],['+60d',Date.now()+60*864e5],['end',Date.UTC(2027,1,28,14)]]){
  const R=rankCalc(SS,null,[],[],null,at);const bots=R.list.filter(p=>p.bot);const cnt={};for(const p of bots){const t=tierOf(p);cnt[t.n]=(cnt[t.n]||0)+1}
  out[lab]={max:Math.round(bots[0].r),tiers:cnt}}return JSON.stringify(out)})()`)"""
async def run(g):
    shutil.rmtree('/tmp/webV',ignore_errors=True);shutil.copytree('/tmp/webT','/tmp/webV')
    p='/tmp/webV/index.html';s=open(p).read();s=s.replace('const BOT_GPH=10,','const BOT_GPH=%s,'%g,1);open(p,'w').write(s)
    errs=[]
    async with async_playwright() as pw:
        b=await pw.chromium.launch();pg=await newpage(b,errs,'x');await asyncio.sleep(2)
        r=json.loads(await pg.evaluate(JS));print('GPH',g,r,flush=True);await b.close()
async def main():
    for g in sys.argv[1:]: await run(g)
asyncio.run(main())
