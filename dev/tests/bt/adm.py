import asyncio,os
os.environ['WEBDIR']='/tmp/webT'
src=open('/home/claude/firebase/fbtest.py').read().split('async def main():')[0].replace('PORT=8765','PORT=8862')
exec(src)
async def adminpage(b,errs):
    ctx=await b.new_context(viewport={'width':390,'height':844})
    await ctx.add_init_script("localStorage.setItem('bo-tut-done','1');localStorage.setItem('bo-rkintro','1');localStorage.setItem('bo-rklg','1');sessionStorage.setItem('bo-noatt','1');localStorage.setItem('bo-nick','관리자');localStorage.setItem('bo-airec',JSON.stringify({pro:{w:1,l:0,d:0}}));window.__fakeAdmin=true;window.__fakeEmail='slayersnaya@gmail.com';sessionStorage.setItem('fake-g','1')")
    async def route(rt): await rt.fulfill(path=FAKE[rt.request.url.split('/')[-1]],content_type='application/javascript')
    await ctx.route('https://www.gstatic.com/**',route)
    p=await ctx.new_page();p.on('pageerror',lambda e:errs.append('adm:'+str(e)))
    p.on('console',lambda m:errs.append('adm console:'+m.text) if m.type=='error' else None)
    await p.expose_function('__fsSend',lambda j,p=p:asyncio.ensure_future(relay(p,j)))
    PAGES.append(p);await p.goto(f'http://127.0.0.1:{PORT}/index.html')
    try: await p.click('[data-act=wskip]',timeout=1500)
    except Exception: pass
    return p
async def main():
    errs=[]
    async with async_playwright() as pw:
        b=await pw.chromium.launch()
        a=await newpage(b,errs,'원이짱');await a.evaluate("()=>{localStorage.setItem('bo-nick','원이짱');window.__T.ev('syncNick()')}")
        c=await newpage(b,errs,'둘째');await asyncio.sleep(1.5)
        n=await newpage(b,errs,'일반');await asyncio.sleep(1)
        vis=await n.evaluate("()=>!document.querySelector('#admUsers').classList.contains('hide')");print('normal sees btn',vis)
        ad=await adminpage(b,errs);await asyncio.sleep(2)
        await ad.evaluate("()=>document.querySelector('.tabbar:not(.tbw) [data-k=set]')?.click()");await asyncio.sleep(0.4)
        print('admin btn visible',await ad.evaluate("()=>!document.querySelector('#admUsers').classList.contains('hide')"))
        await ad.evaluate("()=>document.querySelector('#admUsers').click()");await asyncio.sleep(1)
        print('sum',await txt(ad,'#admSum'));print('list',await txt(ad,'#admList'))
        await ad.screenshot(path='/tmp/bt/adm.png')
        await ad.evaluate("()=>document.querySelector('#admFlt [data-k=g]').click()");await asyncio.sleep(0.3);print('google',await txt(ad,'#admList'))
        # 일반 사용자가 seen 읽기 시도
        r=await n.evaluate("async()=>{try{await window.__T.ev('db').collection('seen').get();return 'read ok'}catch(e){return 'denied'}}");print('normal read',r)
        print('errors',[e for e in errs if 'TUNNEL' not in e]);await b.close()
asyncio.run(main())
