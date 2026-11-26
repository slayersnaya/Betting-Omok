import asyncio,os
src=open('/home/claude/firebase/fbtest.py').read().split('async def main():')[0].replace('PORT=8765','PORT=8841')
exec(src)
async def main():
    errs=[]
    async with async_playwright() as pw:
        b=await pw.chromium.launch()
        p=await newpage(b,errs,'성민');await asyncio.sleep(1.5)
        print('acct',await txt(p,'#acct'))
        await p.evaluate("()=>document.querySelector('[data-act=sheet][data-k=set]').click()");await asyncio.sleep(0.3)
        await p.click('#acct [data-act=acc]');await asyncio.sleep(0.4)
        print('sheet',await txt(p,'#sh-acc'))
        await p.fill('#accEm','bad');await p.fill('#accPw','123');await p.click('#emLink');await asyncio.sleep(0.3);print('err1',await txt(p,'#accErr'))
        await p.fill('#accEm','me@test.com');await p.fill('#accPw','123');await p.click('#emLink');await asyncio.sleep(0.3);print('err2',await txt(p,'#accErr'))
        await p.fill('#accPw','secret12');await p.click('#emLink');await asyncio.sleep(1.5)
        print('after link acct',await txt(p,'#acct'),'| sheet open',await p.evaluate("()=>!document.querySelector('#sh-acc').classList.contains('hide')"))
        # 랭크 게임 가능해졌는지(관문 다이얼로그 없이 매칭)
        await p.evaluate("()=>{const s=document.querySelector('#sh-set');}");
        await p.keyboard.press('Escape');await asyncio.sleep(0.3)
        await p.evaluate("()=>document.querySelector('.tabbar:not(.tbw) [data-k=rank]').click()");await asyncio.sleep(0.3)
        await p.click('#mmBtn');await asyncio.sleep(0.8);print('mm',await txt(p,'#mmSt'),'| dlg',await txt(p,'#dlg'))
        await p.click('#mmBtn');await asyncio.sleep(0.3)
        # 다른 기기에서 로그인
        p2=await newpage(b,errs,'다른폰');await asyncio.sleep(1.5)
        await p2.evaluate("()=>document.querySelector('[data-act=sheet][data-k=set]').click()");await asyncio.sleep(0.3);await p2.click('#acct [data-act=acc]');await asyncio.sleep(0.3)
        await p2.fill('#accEm','me@test.com');await p2.fill('#accPw','wrong1');await p2.evaluate("()=>{}")
        await p2.fill('#accPw','wrong');await p2.fill('#accPw','wrong');
        await p2.evaluate("()=>{document.querySelector('#accPw').value='wrong'}")
        await p2.click('#emLogin');await asyncio.sleep(0.5);print('wrong pw',await txt(p2,'#accErr'))
        await p2.fill('#accPw','secret12');await p2.click('#emLogin');await asyncio.sleep(2.5)
        print('p2 after login acct',await txt(p2,'#acct'))
        await p2.evaluate("()=>document.querySelector('[data-act=sheet][data-k=set]').click()");await asyncio.sleep(0.3);
        await p2.evaluate("()=>document.querySelector('#acct [data-act=acc]')&&document.querySelector('#acct [data-act=acc]').click()");
        print('p2 acct text',await txt(p2,'#acct'))
        # 재설정
        p3=await newpage(b,errs,'p3');await asyncio.sleep(1.2);await p3.evaluate("()=>document.querySelector('[data-act=sheet][data-k=set]').click()");await asyncio.sleep(0.3);await p3.click('#acct [data-act=acc]');await asyncio.sleep(0.3)
        await p3.click('[data-act=emreset]');await asyncio.sleep(0.3);print('reset empty',await txt(p3,'#accErr'))
        await p3.fill('#accEm','me@test.com');await p3.click('[data-act=emreset]');await asyncio.sleep(0.5);print('reset sent to',await p3.evaluate("()=>window.__fakeReset"))
        print('errors',[e for e in errs if 'TUNNEL' not in e][:8]);await b.close()
asyncio.run(main())
