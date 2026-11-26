import asyncio,os
os.environ['WEBDIR']='/tmp/webT'
src=open('/home/claude/firebase/fbtest.py').read().split('async def main():')[0].replace('PORT=8765','PORT=8871')
exec(src)
async def main():
    errs=[]
    async with async_playwright() as pw:
        b=await pw.chromium.launch(args=['--autoplay-policy=no-user-gesture-required']);p=await newpage(b,errs,'s');await asyncio.sleep(2)
        await p.mouse.click(5,300);await asyncio.sleep(3)
        print('불러온 파일',await p.evaluate("()=>window.__T.ev('JSON.stringify(Object.fromEntries(Object.entries(SNDF).map(([k,b])=>[k,+b.duration.toFixed(2)])))')"))
        print('승리 재생(파일)',await p.evaluate("()=>window.__T.ev(`sndFile('win')`)"),'| 합성음 대체 확인',await p.evaluate("()=>window.__T.ev(`sndFile('five')`)"))
        print('errors',[e for e in errs if 'ERR_' not in e][:3]);await b.close()
asyncio.run(main())
