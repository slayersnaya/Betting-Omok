import asyncio,os
os.environ['WEBDIR']='/tmp/webT'
src=open('/home/claude/firebase/fbtest.py').read().split('async def main():')[0].replace('PORT=8765','PORT=8868')
exec(src)
async def main():
    errs=[]
    async with async_playwright() as pw:
        b=await pw.chromium.launch();p=await newpage(b,errs,'성민');await asyncio.sleep(2)
        await p.set_viewport_size({'width':360,'height':780})
        await p.evaluate("()=>{document.querySelectorAll('.lsheet').forEach(x=>x.classList.add('hide'));const s=document.getElementById('sh-chat');s.classList.remove('hide');document.getElementById('chNick').textContent='하율'}")
        await asyncio.sleep(.5);await p.screenshot(path='/tmp/bt/kb0.png')
        # resizes-content 흉내: 키보드만큼 화면이 줄어듦
        await p.set_viewport_size({'width':360,'height':430});await asyncio.sleep(.5)
        r=await p.evaluate("()=>{const h=document.querySelector('#sh-chat .shh').getBoundingClientRect(),f=document.getElementById('chForm').getBoundingClientRect();return [Math.round(h.top),Math.round(f.bottom),innerHeight]}")
        print('header top, form bottom, vh:',r);await p.screenshot(path='/tmp/bt/kb1.png')
        print('errors',[e for e in errs if 'ERR_' not in e]);await b.close()
asyncio.run(main())
