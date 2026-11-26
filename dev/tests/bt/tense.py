import asyncio,os
os.environ['WEBDIR']='/tmp/webT'
src=open('/home/claude/firebase/fbtest.py').read().split('async def main():')[0].replace('PORT=8765','PORT=8871')
exec(src)
async def main():
    errs=[]
    async with async_playwright() as pw:
        b=await pw.chromium.launch(args=['--autoplay-policy=no-user-gesture-required']);p=await newpage(b,errs,'s');await asyncio.sleep(2)
        await p.mouse.click(5,300);await p.evaluate("c=>window.__T.ev(c)","L.start(null,'mid');UI.mode='local';show('game');renderAll()");await asyncio.sleep(4)
        st="window.__T.ev('JSON.stringify([BG.scene,bgmTense()])')"
        print('대국 시작',await p.evaluate("()=>"+st))
        await p.evaluate("c=>window.__T.ev(c)","for(let c=3;c<7;c++)L.s.bd[9][c]=1;L.s.t++;renderAll()");await asyncio.sleep(3.5)
        print('검은돌 4개+빈칸',await p.evaluate("()=>"+st))
        await p.evaluate("c=>window.__T.ev(c)","L.s.bd[9][7]=2;L.s.bd[9][2]=2;L.s.t++;renderAll()");await asyncio.sleep(3.5)
        print('양쪽 막힘',await p.evaluate("()=>"+st))
        print('errors',[e for e in errs if 'ERR_' not in e][:3]);await b.close()
asyncio.run(main())
