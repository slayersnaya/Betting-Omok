import asyncio,os
os.environ['WEBDIR']='/tmp/webT'
src=open('/home/claude/firebase/fbtest.py').read().split('async def main():')[0].replace('PORT=8765','PORT=8870')
exec(src)
async def main():
    errs=[]
    async with async_playwright() as pw:
        b=await pw.chromium.launch(args=['--autoplay-policy=no-user-gesture-required']);p=await newpage(b,errs,'s');await asyncio.sleep(2)
        await p.mouse.click(5,300);await asyncio.sleep(1.5)
        st=lambda: p.evaluate("()=>window.__T.ev(`JSON.stringify({scene:BG.scene,cur:BG.cur,g:BG.u[BG.cur]?+BG.u[BG.cur].g.gain.value.toFixed(3):null,t:BG.u[BG.cur]?+BG.u[BG.cur].el.currentTime.toFixed(1):null,paused:BG.u[BG.cur]?BG.u[BG.cur].el.paused:null,err:BG.u[BG.cur]&&BG.u[BG.cur].el.error?BG.u[BG.cur].el.error.code:null})`)")
        print('1.5s',await st());await asyncio.sleep(6);print('7.5s (목표 0.24)',await st())
        await p.evaluate("()=>window.__T.ev(`snd('win')`)");await asyncio.sleep(0.6);print('win 덕킹',await st());await asyncio.sleep(3.5);print('복귀',await st())
        await p.evaluate("()=>window.__T.ev(`UI.view='game';UI.mode='local'`)");await asyncio.sleep(3.5);print('대국(곡 없음→조용)',await st())
        await p.evaluate("()=>window.__T.ev(`UI.view='lobby'`)");await asyncio.sleep(3);print('로비 복귀',await st())
        await p.evaluate("()=>{localStorage.setItem('bo-bgm','0')}");await asyncio.sleep(3);print('배경음 끔',await st())
        print('errors',[e for e in errs if 'ERR_' not in e]);await b.close()
asyncio.run(main())
