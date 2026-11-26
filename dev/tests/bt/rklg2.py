import asyncio,os
os.environ['WEBDIR']='/tmp/webT'
S=open('/tmp/bt/rklg.py').read();S=S[:S.rindex('async def main():')].replace('8863','8864')
exec(S)
async def main():
    errs=[]
    async with async_playwright() as pw:
        b=await pw.chromium.launch()
        p=await pg(b,errs,"")
        print('A dlg:',await txt(p,'#dlg'));await p.screenshot(path='/tmp/bt/rk1.png')
        print('A buttons:',await p.evaluate("()=>[...document.querySelectorAll('#dlg button')].map(b=>b.textContent.trim())"))
        await p.click('[data-act=dlgok]');await asyncio.sleep(1.2)
        print('A after 나중에: tab',await p.evaluate("()=>window.__T.UI.tab"))
        # 게스트로 랭크 매칭 시도 → 닉네임 안내
        await p.evaluate("()=>window.__T.ev('mmStart()')");await asyncio.sleep(.6)
        print('A mm no-nick dlg:',await txt(p,'#dlg'));await p.screenshot(path='/tmp/bt/rk2.png')
        await p.click('[data-act=dlgok]');await asyncio.sleep(.6)
        print('nick sheet open:',await p.evaluate("()=>!document.querySelector('#sh-nick').classList.contains('hide')"))
        await p.fill('#nick','테스트게스트');await asyncio.sleep(.2)
        await p.evaluate("()=>{const b=document.querySelector('#sh-nick [data-act=nickok], #sh-nick .btn:not(.ghost)');b&&b.click()}");await asyncio.sleep(2.5)
        for _ in range(4):
            if not await p.evaluate("()=>document.querySelector('#dlg').classList.contains('hide')"):
                await p.click('[data-act=dlgok]');await asyncio.sleep(1.5)
        print('MM on:',await p.evaluate("()=>window.__T.MM.on"),'| toast/dlg',await txt(p,'#dlg'))
        q=await pg(b,errs,"localStorage.setItem('bo-rkintro','1');localStorage.setItem('bo-nick','성민2');")
        print('B dlg:',await txt(q,'#dlg'));await q.screenshot(path='/tmp/bt/rk3.png')
        print('errors',errs);await b.close()
asyncio.run(main())
