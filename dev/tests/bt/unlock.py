import asyncio,os
os.environ['WEBDIR']='/tmp/webT'
src=open('/home/claude/firebase/fbtest.py').read().split('async def main():')[0].replace('PORT=8765','PORT=8872')
exec(src)
ST="()=>window.__T.ev(`JSON.stringify({ctx:actx?actx.state:null,done:!!sndUnlock.done,scene:BG.scene,files:Object.keys(SNDF)})`)"
async def main():
    errs=[]
    async with async_playwright() as pw:
        # A: 브라우저가 소리를 허용하는 경우(설치 앱과 비슷) → 터치 없이 바로
        b=await pw.chromium.launch(args=['--autoplay-policy=no-user-gesture-required']);p=await newpage(b,errs,'a');await asyncio.sleep(3)
        print('A 허용·터치 없음',await p.evaluate(ST));await b.close()
        # B: 기본 정책(사용자 동작 필요) → 모바일 탭 한 번
        b=await pw.chromium.launch();ctx=await b.new_context(viewport={'width':390,'height':844},has_touch=True,is_mobile=True)
        await ctx.add_init_script("localStorage.setItem('bo-tut-done','1');localStorage.setItem('bo-rkintro','1');localStorage.setItem('bo-rklg','1');sessionStorage.setItem('bo-noatt','1')")
        async def route(rt): await rt.fulfill(path=FAKE[rt.request.url.split('/')[-1]],content_type='application/javascript')
        await ctx.route('https://www.gstatic.com/**',route)
        q=await ctx.new_page();await q.expose_function('__fsSend',lambda j,q=q:asyncio.ensure_future(relay(q,j)));PAGES.append(q)
        await q.goto(f'http://127.0.0.1:{PORT}/index.html');await asyncio.sleep(2.5)
        print('B 터치 전',await q.evaluate(ST))
        await q.tap('body',position={'x':200,'y':700});await asyncio.sleep(1.5)
        print('B 탭 한 번 뒤',await q.evaluate(ST))
        await b.close()
        print('errors',[e for e in errs if 'ERR_' not in e])
asyncio.run(main())
