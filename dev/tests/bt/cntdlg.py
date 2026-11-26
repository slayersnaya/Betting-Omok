import asyncio,os
os.environ['WEBDIR']='/tmp/webT'
S=open('/tmp/bt/rklg.py').read();S=S[:S.rindex('async def main():')].replace('8863','8873')
exec(S)
async def main():
    errs=[]
    async with async_playwright() as pw:
        b=await pw.chromium.launch()
        p=await pg(b,errs,"localStorage.setItem('bo-rkintro','1');localStorage.setItem('bo-rklg','1');localStorage.setItem('bo-nick','성민2');")
        await p.evaluate("()=>window.__T.ev('mmStart()')");await asyncio.sleep(.6)
        print('1 dlg:',await txt(p,'#dlg'));await p.screenshot(path='/tmp/bt/cntdlg.png')
        await p.click('[data-act=dlgok]');await asyncio.sleep(1)
        print('확인 → 매칭:',await p.evaluate("()=>window.__T.MM.on"))
        await p.evaluate("()=>window.__T.ev('mmStop()')");await asyncio.sleep(.5)
        await p.evaluate("()=>window.__T.ev('mmStart()')");await asyncio.sleep(.6)
        print('2 다시 뜸:',await p.evaluate("()=>!document.querySelector('#dlg').classList.contains('hide')"))
        await p.click('[data-act=cntnever]');await asyncio.sleep(1)
        print('다시 보지 않기 → 매칭:',await p.evaluate("()=>window.__T.MM.on"),await p.evaluate("()=>localStorage.getItem('bo-cntok')"))
        await p.evaluate("()=>window.__T.ev('mmStop()')");await asyncio.sleep(.5)
        await p.evaluate("()=>window.__T.ev('mmStart()')");await asyncio.sleep(.6)
        print('3 안 뜸:',await p.evaluate("()=>document.querySelector('#dlg').classList.contains('hide')"),await p.evaluate("()=>window.__T.MM.on"))
        print('errors',errs);await b.close()
asyncio.run(main())
