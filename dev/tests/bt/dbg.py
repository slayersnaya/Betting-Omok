exec(open('/home/claude/tests/atttest.py').read().split('async def main():')[0])
async def main():
    errs=[]
    async with async_playwright() as pw:
        b=await pw.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
        p=await newpage(b,errs,'성민');p.on('console',lambda m:print('C',m.text[:200]) if m.type in('error','warning') else None);await asyncio.sleep(3);await ev(p,"goLobby()")
        print(await p.evaluate("async()=>{try{const x=await window.__T.ev('db').doc('wal/'+window.__T.ev('SEAT')).get();return 'ok '+x.exists+' '+JSON.stringify(x.data())}catch(e){return 'ERR '+(e.code||'')+' '+e.message}}"));print(await ev(p,'ECO.err'),await ev(p,'String(!!ecoSrv())'),await p.evaluate('()=>window.__walDeny'));print(await ev(p,"JSON.stringify({ok:ECO.ok,w:ECO.w,prov:[...RW.prov.keys()],items:rwItems()})"));print(await p.evaluate("()=>document.querySelector('#rwBar').outerHTML.slice(0,600)"))
        print(await p.evaluate("()=>document.querySelector('#ecoCard').innerText.slice(0,200)"))
        print(errs[:5]);await b.close()
asyncio.run(main())
