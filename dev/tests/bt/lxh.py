import asyncio,os
os.environ['WEBDIR']='/tmp/webT'
src=open('/home/claude/firebase/fbtest.py').read().split('async def main():')[0].replace('PORT=8765','PORT=8835')
exec(src)
async def main():
    async with async_playwright() as pw:
        b=await pw.chromium.launch();errs=[]
        p=await newpage(b,errs,'x');await asyncio.sleep(1.5)
        await p.evaluate("()=>{localStorage.setItem('bo-rkintro','1');window.__T.ev(\"setTab('rank')\")}");await asyncio.sleep(1.5)
        H=[]
        for items in (0,1,2,5):
            hh=await p.evaluate("""n=>{const ev=window.__T.ev;const real=ev('lxItems');window.lxItems=null;ev('LX').more=false;
              const fake=Array.from({length:n},(_,i)=>({k:'k'+i,na:'가나다'+i,nb:'abc'+i,ra:1000+i*50,rb:1020,st:Date.now()-i*6e4}));
              eval('lxItems=()=>fake');ev('lxRender()');const c=document.getElementById('lxCard');const r=c.getBoundingClientRect();return [Math.round(r.height),c.classList.contains('hide')]}""",items)
            H.append((items,hh));await p.screenshot(path=f'/tmp/bt/lx{items}.png')
        print(H,'errors',[e for e in errs if 'ERR_' not in e]);await b.close()
asyncio.run(main())
