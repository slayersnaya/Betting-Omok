import asyncio,os
os.environ['WEBDIR']='/tmp/webT'
src=open('/home/claude/firebase/fbtest.py').read().split('async def main():')[0].replace('PORT=8765','PORT=8871')
exec(src)
async def main():
    errs=[]
    async with async_playwright() as pw:
        b=await pw.chromium.launch(args=['--autoplay-policy=no-user-gesture-required']);p=await newpage(b,errs,'s');await asyncio.sleep(2)
        await p.mouse.click(5,300);await asyncio.sleep(2)
        await p.evaluate("c=>window.__T.ev(c)","pzOpen()");await asyncio.sleep(3.5);print('묘수 풀이',await p.evaluate("()=>window.__T.ev('BG.scene')"))
        await p.evaluate("c=>window.__T.ev(c)","closeSheet()");await asyncio.sleep(3.5);print('닫음',await p.evaluate("()=>window.__T.ev('BG.scene')"))
        print('errors',[e for e in errs if 'ERR_' not in e][:3]);await b.close()
asyncio.run(main())
