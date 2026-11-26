import asyncio,os
os.environ['WEBDIR']='/tmp/webT'
src=open('/home/claude/firebase/fbtest.py').read().split('async def main():')[0].replace('PORT=8765','PORT=8865')
exec(src)
async def main():
    errs=[]
    async with async_playwright() as pw:
        b=await pw.chromium.launch()
        for theme in ('dark','light'):
            ctx=await b.new_context(viewport={'width':360,'height':740},color_scheme=theme)
            await ctx.add_init_script("localStorage.setItem('bo-rkintro','1');localStorage.setItem('bo-rklg','1');sessionStorage.setItem('bo-noatt','1')")
            async def route(rt): await rt.fulfill(path=FAKE[rt.request.url.split('/')[-1]],content_type='application/javascript')
            await ctx.route('https://www.gstatic.com/**',route)
            p=await ctx.new_page();p.on('pageerror',lambda e:errs.append(str(e)))
            await p.expose_function('__fsSend',lambda j,p=p:asyncio.ensure_future(relay(p,j)));PAGES.append(p)
            await p.goto(f'http://127.0.0.1:{PORT}/index.html');await asyncio.sleep(2)
            try: await p.click('[data-act=wskip]',timeout=1500)
            except Exception: pass
            await p.evaluate("()=>window.__T.ev('T.start()')");await asyncio.sleep(0.6)
            seen=[]
            for k in range(12):
                st=await p.evaluate("()=>window.__T.ev('JSON.stringify([T.s.step,TUT[T.s.step].k,TUT[T.s.step].title])')");seen.append(st)
                stp=await p.evaluate("()=>window.__T.ev('T.s.step')")
                if stp==4:
                    await p.screenshot(path=f'/tmp/bt/tut_carry_{theme}.png')
                    r=await p.evaluate("()=>{const e=document.querySelector('.tcar');if(!e)return 'no tcar';return [e.getBoundingClientRect().height,[...e.children].map(c=>c.getBoundingClientRect().height)]}")
                    print('carry box',r, await p.evaluate("()=>document.querySelector('.tdots').getAttribute('aria-label')"))
                kind=await p.evaluate("()=>window.__T.ev('TUT[T.s.step].k')")
                if await p.evaluate("()=>window.__T.ev('!!TUT[T.s.step].end')"):break
                if kind=='info' or kind=='result':
                    await p.evaluate("()=>document.querySelector('[data-act=tnext]').click()")
                elif kind=='designate':
                    await p.evaluate("()=>window.__T.ev('UI.sel=null')");await p.evaluate("()=>{const t=window.__T.ev('TUT[T.s.step].tap');window.__T.ev(`T.s.cells=legalTriples(T.s.bd).find(x=>x.some(([r,c])=>r===${t[0]}&&c===${t[1]}));T.go(1)`)}")
                elif kind=='bet':
                    need=await p.evaluate("()=>window.__T.ev('JSON.stringify(TUT[T.s.step].need||null)')")
                    if need!='null':
                        await p.evaluate("()=>{const n=window.__T.ev('TUT[T.s.step].need');window.__T.ev(`UI.bet=[1,1,1];UI.bet[${n[0]}]=${n[1]}`)}")
                    await p.evaluate("()=>{window.__T.ev('updateBetSum(T.s.pts.A)');document.querySelector('[data-act=tsubmit]').click()}")
                await asyncio.sleep(1.8)
            print(theme,seen)
            await ctx.close()
        print('errors',errs);await b.close()
asyncio.run(main())
