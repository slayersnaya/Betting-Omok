import asyncio,random
exec(open('fbtest.py').read().split('async def main():')[0])
async def main():
    errs=[]
    async with async_playwright() as pw:
        b=await pw.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
        ctx=await b.new_context(viewport={'width':360,'height':740},accept_downloads=True)
        await ctx.add_init_script("localStorage.setItem('bo-tut-done','1');localStorage.setItem('bo-rkintro','1');localStorage.setItem('bo-rklg','1');sessionStorage.setItem('bo-noatt','1');localStorage.setItem('bo-airec',JSON.stringify({pro:{w:1,l:0,d:0}}));window.__fakeAdmin=true;window.__fakeEmail='slayersnaya@gmail.com';sessionStorage.setItem('fake-g','1')")
        async def route(rt): await rt.fulfill(path=FAKE[rt.request.url.split('/')[-1]],content_type='application/javascript')
        await ctx.route('https://www.gstatic.com/**',route)
        p=await ctx.new_page();p.on('pageerror',lambda e:errs.append(str(e)))
        await p.expose_function('__fsSend',lambda j,p=p:asyncio.ensure_future(relay(p,j)));PAGES.append(p)
        await p.goto(f'http://127.0.0.1:{PORT}/index.html#admin');await asyncio.sleep(2)
        await p.click('[data-act=level][data-k=ultimate]');await p.click('[data-act=solo]');await asyncio.sleep(.4)
        await p.click('#coin');random.seed(3)
        for step in range(80):
            ph=await p.evaluate("()=>document.querySelector('.phase')?.textContent||''")
            if '종료' in ph: break
            if await p.locator('[data-act=dconfirm]').count():
                for _ in range(40):
                    await tap(p,random.randint(4,14),random.randint(4,14));await p.wait_for_timeout(50)
                    if not await p.locator('[data-act=dconfirm][disabled]').count(): break
                await p.click('[data-act=dconfirm]')
            elif await p.locator('#bsub').count():
                if not await p.locator('#bsub[disabled]').count(): await p.wait_for_timeout(650);await p.click('#bsub')
            await p.wait_for_timeout(900)
        await asyncio.sleep(1)
        ks=[k for k in STORE if k.startswith('aigames/')];print('aigames docs',ks,{k:(STORE[k]['level'],STORE[k]['winner'],len(__import__('json').loads(STORE[k]['hj']))) for k in ks})
        await p.click('[data-act=lobby]');await asyncio.sleep(.5)
        await p.evaluate("()=>document.querySelector('[data-act=sheet][data-k=set]').click()");await asyncio.sleep(.4)
        print('admin btn visible',await p.locator('#admDl').is_visible(),await txt(p,'#acct'))
        async with p.expect_download() as dl: await p.click('#admDl')
        d=await dl.value;import json;print('download',d.suggested_filename,len(json.load(open(await d.path()))['games']))
        print('denied',await p.evaluate("()=>window.__deniedList||[]"),'errs',errs)
        await b.close()
asyncio.run(main())
