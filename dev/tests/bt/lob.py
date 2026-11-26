import asyncio,os
os.environ['WEBDIR']='/tmp/webT'
S=open('/tmp/bt/rklg.py').read();S=S[:S.rindex('async def main():')].replace('8863','8871')
exec(S)
async def main():
    errs=[]
    async with async_playwright() as pw:
        b=await pw.chromium.launch()
        p=await pg(b,errs,"localStorage.setItem('bo-rkintro','1');localStorage.setItem('bo-rklg','1');localStorage.setItem('bo-nick','슬레열스나야');")
        print(await p.evaluate("()=>{const h=document.querySelector('#lobby .ltop'),t=document.getElementById('nickTxt'),m=document.getElementById('hMail');return [h.className,t&&t.scrollWidth,t&&t.clientWidth,m&&m.className,innerWidth]}"))
        await p.screenshot(path='/tmp/bt/lob1.png',full_page=True)
        await p.set_viewport_size({'width':1280,'height':800});await asyncio.sleep(1);await p.screenshot(path='/tmp/bt/lob2.png')
        print('errors',errs);await b.close()
asyncio.run(main())
