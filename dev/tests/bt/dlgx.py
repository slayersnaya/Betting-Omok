import asyncio,os
os.environ['WEBDIR']='/tmp/webT'
S=open('/tmp/bt/rklg.py').read();S=S[:S.rindex('async def main():')].replace('8863','8874')
exec(S)
async def main():
    errs=[]
    async with async_playwright() as pw:
        b=await pw.chromium.launch()
        p=await pg(b,errs,"sessionStorage.setItem('cnt-ask','1');localStorage.removeItem('bo-cntok');localStorage.setItem('bo-rkintro','1');localStorage.setItem('bo-rklg','1');localStorage.setItem('bo-nick','성민2');")
        await p.evaluate("()=>window.__T.ev('mmStart()')");await asyncio.sleep(.6)
        print('btns:',await p.evaluate("()=>[...document.querySelectorAll('#dlg button')].map(b=>b.textContent.trim()||b.className)"));await p.screenshot(path='/tmp/bt/dx1.png')
        await p.click('#dlg .dlgx');await asyncio.sleep(.4)
        print('X 닫힘:',await p.evaluate("()=>document.querySelector('#dlg').classList.contains('hide')"),'매칭',await p.evaluate("()=>window.__T.MM.on"))
        await p.evaluate("()=>window.__T.ev(\"dialog('긴 안내 문장이 이렇게 길게 들어가면 오른쪽 위 닫기 버튼과 겹치지 않는지 확인하는 문장이에요.','확인',null)\")");await asyncio.sleep(.4)
        await p.screenshot(path='/tmp/bt/dx2.png')
        await p.mouse.click(10,10);await asyncio.sleep(.4)
        print('바깥 닫힘:',await p.evaluate("()=>document.querySelector('#dlg').classList.contains('hide')"))
        await p.evaluate("()=>{const T=window.__T.ev('TIERS');window.__T.ev('tupShow')(T[1],T[2])}");await asyncio.sleep(2.8);await p.screenshot(path='/tmp/bt/dx3.png')
        await p.mouse.click(10,10);await asyncio.sleep(.5);print('승급창 바깥 닫힘:',await p.evaluate("()=>!document.getElementById('tup')"))
        print('errors',errs);await b.close()
asyncio.run(main())
