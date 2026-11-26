import asyncio,os
os.environ['WEBDIR']='/tmp/webT'
src=open('/home/claude/firebase/fbtest.py').read().split('async def main():')[0].replace('PORT=8765','PORT=8851')
exec(src)
async def main():
    errs=[]
    async with async_playwright() as pw:
        b=await pw.chromium.launch()
        p=await newpage(b,errs,'성민');await asyncio.sleep(2)
        await p.evaluate("()=>{const n0=Date.now.bind(Date);Date.now=()=>n0()+864e5}")
        r=await p.evaluate("""()=>{const T=window.__T;T.rankCompute();const ch=[...(T.RK.chal||[])];return [T.RK.chalD, ch.map(s=>{const q=T.RK.map.get(s);return q.nick+' '+Math.round(q.r)}), T.RK.list.slice(0,7).map(q=>q.nick+' '+Math.round(q.r)+' '+(T.tierOf(q)||{}).n)]}""")
        print('today chal',r)
        # 내 자리를 오늘 챌린저로 만든 캐시 → 진급 창
        r2=await p.evaluate("""()=>{const T=window.__T;const c=JSON.parse(localStorage.getItem('bo-chal'));c.s=[T.seat(),...c.s.slice(0,4)];localStorage.setItem('bo-chal',JSON.stringify(c));localStorage.setItem('bo-chalst',JSON.stringify({D:0,in:false}));T.RK.map.set(T.seat(),{seat:T.seat(),r:1720,g:20,w:15,l:5,d:0});T.rankCompute();return [...T.RK.chal].includes(T.seat())}""")
        print('state',await p.evaluate("()=>[window.__T.UI.view,document.querySelector('#dlg').className,document.querySelector('#welcome').className,localStorage.getItem('bo-chalst')]"));await asyncio.sleep(4)
        print('me in chal',r2,'| popup',await p.evaluate("()=>{const e=document.getElementById('tup');return e?e.innerText.replace(/\\s+/g,' '):null}"))
        await p.screenshot(path='/tmp/bt/chal_pop.png')
        # 다시 열어도 같은 날엔 안 뜸
        await p.evaluate("()=>{const e=document.querySelector('#tup button');if(e){e.click();e.click()}}");await asyncio.sleep(0.5)
        await p.evaluate("()=>window.__T.rankCompute()");await asyncio.sleep(1)
        print('popup again',await p.evaluate("()=>!!document.getElementById('tup')"))
        print('errors',[e for e in errs if 'TUNNEL' not in e][:5]);await b.close()
asyncio.run(main())
