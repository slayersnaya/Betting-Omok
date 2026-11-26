import asyncio,json
import importlib.util,sys
src=open('fbtest.py').read().split('async def main():')[0]
exec(src)
async def main():
    errs=[]
    async with async_playwright() as pw:
        b=await pw.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
        # 1) 처음 기기: uid 고정, 구글 연결, 닉네임·AI 전적
        ctx=await b.new_context(viewport={'width':390,'height':844})
        await ctx.add_init_script("sessionStorage.setItem('fake-uid','uGoogleOld0000000000');localStorage.setItem('bo-airec',JSON.stringify({ultimate:{w:2,l:5,d:0}}));localStorage.setItem('bo-rkintro','1');localStorage.setItem('bo-rklg','1');sessionStorage.setItem('bo-noatt','1')")
        async def route(rt): await rt.fulfill(path=FAKE[rt.request.url.split('/')[-1]],content_type='application/javascript')
        await ctx.route('https://www.gstatic.com/**',route)
        p=await ctx.new_page();p.on('pageerror',lambda e:errs.append(str(e)))
        await p.expose_function('__fsSend',lambda j,p=p:asyncio.ensure_future(relay(p,j)));PAGES.append(p)
        await p.goto(f'http://127.0.0.1:{PORT}/index.html');await asyncio.sleep(1.5)
        print('welcome shown:',await p.evaluate("()=>!document.querySelector('#welcome').classList.contains('hide')"),'| wgl visible:',await p.locator('.wgl').first.is_visible())
        await p.click('[data-act=wskip]');await asyncio.sleep(0.3)
        await p.evaluate("()=>document.querySelector('[data-act=sheet][data-k=nick]').click()");await asyncio.sleep(0.3);await p.fill('#nick','성민');await p.click('#nickOk');await asyncio.sleep(1)
        await p.evaluate("()=>document.querySelector('[data-act=sheet][data-k=set]').click()");await asyncio.sleep(0.3)
        await p.click('#acct [data-act=acc]');await asyncio.sleep(0.4);await p.click('#sh-acc [data-act=glink]');await asyncio.sleep(2.5)
        print('acct:',await txt(p,'#acct'));print('doc:',{k:{kk:vv for kk,vv in v.items() if kk!='h'} for k,v in STORE.items() if k.startswith(('ailearn/','prof/'))})
        PAGES.remove(p);await ctx.close()
        # 2) 앱 삭제 후 재설치: 저장소 비움 → 새 익명 → 구글로 기록 불러오기
        ctx=await b.new_context(viewport={'width':390,'height':844});await ctx.route('https://www.gstatic.com/**',route)
        await ctx.add_init_script("window.__fakeGoogleInUse=true")
        p=await ctx.new_page();p.on('pageerror',lambda e:errs.append(str(e)))
        await p.expose_function('__fsSend',lambda j,p=p:asyncio.ensure_future(relay(p,j)));PAGES.append(p)
        await p.goto(f'http://127.0.0.1:{PORT}/index.html');await asyncio.sleep(1.5)
        print('fresh nick:',await p.evaluate("()=>document.querySelector('#nick').value"),'| airec:',await txt(p,'#aiRec'))
        await p.click('[data-act=wglink]');await asyncio.sleep(3)
        print('after reload nick:',await p.evaluate("()=>document.querySelector('#nick').value"),'| airec:',await txt(p,'#aiRec'),'| welcome hidden:',await p.evaluate("()=>document.querySelector('#welcome').classList.contains('hide')"))
        await p.evaluate("()=>document.querySelector('[data-act=sheet][data-k=set]').click()");await asyncio.sleep(0.3)
        print('airec ls:',await p.evaluate("()=>localStorage.getItem('bo-airec')"));print('acct:',await txt(p,'#acct'),'| toast:',await txt(p,'#toast'))
        await p.screenshot(path='/tmp/prof.png')
        print('denied',await p.evaluate("()=>window.__deniedList||[]"),'errors',errs);await b.close()
asyncio.run(main())
