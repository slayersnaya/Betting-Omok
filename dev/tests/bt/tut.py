import asyncio,os
os.environ['WEBDIR']='/tmp/webT'
src=open('/home/claude/firebase/fbtest.py').read().split('async def main():')[0].replace('PORT=8765','PORT=8864')
exec(src)
async def main():
    errs=[]
    async with async_playwright() as pw:
        b=await pw.chromium.launch();ctx=await b.new_context(viewport={'width':360,'height':740})
        await ctx.add_init_script("localStorage.setItem('bo-tut-done','1');localStorage.setItem('bo-rkintro','1');localStorage.setItem('bo-rklg','1');sessionStorage.setItem('bo-noatt','1')")
        async def route(rt): await rt.fulfill(path=FAKE[rt.request.url.split('/')[-1]],content_type='application/javascript')
        await ctx.route('https://www.gstatic.com/**',route)
        p=await ctx.new_page();p.on('pageerror',lambda e:errs.append(str(e)))
        await p.expose_function('__fsSend',lambda j,p=p:asyncio.ensure_future(relay(p,j)));PAGES.append(p)
        await p.goto(f'http://127.0.0.1:{PORT}/index.html');await asyncio.sleep(2)
        await p.evaluate("()=>window.__T.ev('T.start()')");await asyncio.sleep(1)
        r=await p.evaluate('''()=>{const pn=document.querySelector('.tstep')?.parentElement||document.body;const d=document.createElement('div');d.className='tstep sm';d.innerHTML=window.__T.ev("`<i>3</i><div><b>${TUT[3].title}</b><small>${TUT[3].text}</small></div>`");pn.prepend(d);const sm=d.querySelector('small');const lh=parseFloat(getComputedStyle(sm).lineHeight)||16;return [sm.getBoundingClientRect().height,lh,sm.innerText]}''');print(r)
        await p.screenshot(path='/tmp/bt/tut.png');print(errs);await b.close()
asyncio.run(main())
