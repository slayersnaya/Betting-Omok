import asyncio,os
os.environ['WEBDIR']='/tmp/webT'
src=open('/home/claude/firebase/fbtest.py').read().split('async def main():')[0].replace('PORT=8765','PORT=8831')
exec(src)
async def main():
    errs=[]
    async with async_playwright() as pw:
        b=await pw.chromium.launch()
        for w in (360,412):
            ctx=await b.new_context(viewport={'width':w,'height':900},device_scale_factor=3,is_mobile=True,has_touch=True)
            await ctx.add_init_script("localStorage.setItem('bo-tut-done','1');localStorage.setItem('bo-rkintro','1');localStorage.setItem('bo-rklg','1');sessionStorage.setItem('bo-noatt','1');localStorage.setItem('bo-airec',JSON.stringify({pro:{w:1,l:0,d:0}}));localStorage.setItem('bo-nick','슬레열스타왕')")
            async def route(rt): await rt.fulfill(path=FAKE[rt.request.url.split('/')[-1]],content_type='application/javascript')
            await ctx.route('https://www.gstatic.com/**',route)
            p=await ctx.new_page();await p.expose_function('__fsSend',lambda j,p=p:asyncio.ensure_future(relay(p,j)));PAGES.append(p)
            await p.goto(f'http://127.0.0.1:{PORT}/index.html');await asyncio.sleep(1.5)
            await p.evaluate("()=>{const T=window.__T;T.RK.master=[T.seat()];T.rankCompute();T.ev('renderRank()');document.querySelector('.tabbar [data-k=rank]').click()}");await asyncio.sleep(0.5)
            print(w,await p.evaluate("()=>[document.documentElement.scrollWidth,innerWidth,document.querySelector('#rkPod').innerText.replace(/\\s+/g,' ').slice(0,80)]"))
            await p.screenshot(path=f'/tmp/bt/ovf{w}.png')
        await b.close()
asyncio.run(main())
