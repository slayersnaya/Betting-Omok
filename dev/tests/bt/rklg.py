import asyncio,os
os.environ['WEBDIR']='/tmp/webT'
src=open('/home/claude/firebase/fbtest.py').read().split('async def main():')[0].replace('PORT=8765','PORT=8863')
exec(src)
async def pg(b,errs,init):
    ctx=await b.new_context(viewport={'width':360,'height':740})
    await ctx.add_init_script("localStorage.setItem('bo-tut-done','1');localStorage.setItem('bo-airec',JSON.stringify({mid:{w:1,l:0,d:0}}));sessionStorage.setItem('bo-noatt','1');"+init)
    async def route(rt): await rt.fulfill(path=FAKE[rt.request.url.split('/')[-1]],content_type='application/javascript')
    await ctx.route('https://www.gstatic.com/**',route)
    p=await ctx.new_page();p.on('pageerror',lambda e:errs.append(str(e)))
    await p.expose_function('__fsSend',lambda j,p=p:asyncio.ensure_future(relay(p,j)))
    PAGES.append(p);await p.goto(f'http://127.0.0.1:{PORT}/index.html');await asyncio.sleep(5);return p
async def main():
    errs=[]
    async with async_playwright() as pw:
        b=await pw.chromium.launch()
        p=await pg(b,errs,"")
        print('A dlg:',await txt(p,'#dlg'),'| btn',await txt(p,'[data-act=dlgok]'));await p.screenshot(path='/tmp/bt/rklg1.png')
        await p.click('[data-act=dlgok]');await asyncio.sleep(1.2)
        print('A after: tab',await p.evaluate("()=>window.__T.UI.tab"),'| acct',await txt(p,'#acct'))
        q=await pg(b,errs,"localStorage.setItem('bo-rkintro','1');")
        print('B dlg:',await txt(q,'#dlg'),'| btn',await txt(q,'[data-act=dlgok]'));await q.screenshot(path='/tmp/bt/rklg2.png')
        await q.click('[data-act=rkacc]');await asyncio.sleep(0.5)
        print('B acc sheet open:',await q.evaluate("()=>!document.querySelector('#sh-acc').classList.contains('hide')"),'dlg hidden',await q.evaluate("()=>document.querySelector('#dlg').classList.contains('hide')"))
        r=await pg(b,errs,"localStorage.setItem('bo-rkintro','1');localStorage.setItem('bo-rklg','1');sessionStorage.setItem('bo-noatt','1');")
        print('C dlg hidden:',await r.evaluate("()=>document.querySelector('#dlg').classList.contains('hide')"))
        print('errors',errs);await b.close()
asyncio.run(main())
