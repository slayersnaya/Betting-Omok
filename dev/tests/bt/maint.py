import asyncio,os
os.environ['WEBDIR']='/tmp/webT'
src=open('/home/claude/firebase/fbtest.py').read().split('async def main():')[0].replace('PORT=8765','PORT=8861')
exec(src)
async def main():
    errs=[]
    async with async_playwright() as pw:
        b=await pw.chromium.launch();p=await newpage(b,errs,'성민');await asyncio.sleep(1.5)
        await p.evaluate("()=>document.querySelector('.tabbar:not(.tbw) [data-k=rank]').click()");await asyncio.sleep(0.4)
        print('card',await txt(p,'#rankCard'));await p.click('#mmBtn');await asyncio.sleep(0.4);print('dlg',await txt(p,'#dlg'))
        await p.screenshot(path='/tmp/bt/maint.png');print('errors',[e for e in errs if 'TUNNEL' not in e]);await b.close()
asyncio.run(main())
