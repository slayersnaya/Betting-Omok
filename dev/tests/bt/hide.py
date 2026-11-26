import asyncio,os
os.environ['WEBDIR']='/tmp/webT'
src=open('/home/claude/firebase/fbtest.py').read().split('async def main():')[0].replace('PORT=8765','PORT=8875')
exec(src)
ST="()=>window.__T.ev(`JSON.stringify({scene:BG.scene,ctx:actx&&actx.state,playing:BG.u.filter(u=>!u.el.paused).length})`)"
async def main():
    errs=[]
    async with async_playwright() as pw:
        b=await pw.chromium.launch(args=['--autoplay-policy=no-user-gesture-required']);p=await newpage(b,errs,'s');await asyncio.sleep(3)
        print('켜짐',await p.evaluate(ST))
        await p.evaluate("()=>{Object.defineProperty(document,'hidden',{configurable:true,get:()=>true});Object.defineProperty(document,'visibilityState',{configurable:true,get:()=>'hidden'});document.dispatchEvent(new Event('visibilitychange'))}");await asyncio.sleep(0.3)
        print('뒤로 감(0.3초 뒤)',await p.evaluate(ST));await asyncio.sleep(2);print('2초 뒤',await p.evaluate(ST))
        await p.evaluate("()=>{Object.defineProperty(document,'hidden',{configurable:true,get:()=>false});Object.defineProperty(document,'visibilityState',{configurable:true,get:()=>'visible'});document.dispatchEvent(new Event('visibilitychange'))}");await asyncio.sleep(1.5)
        print('돌아옴',await p.evaluate(ST))
        print('errors',[e for e in errs if 'ERR_' not in e]);await b.close()
asyncio.run(main())
