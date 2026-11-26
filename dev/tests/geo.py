# 머리줄·탭 줄 겹침/넘침 점검: 긴 닉네임(12자)으로 여러 폭, 다크/라이트·큰 글씨
import asyncio, os, sys, json
os.environ.setdefault('WEBDIR','/home/claude/eval/gd3/web');os.environ.setdefault('GPORT','8857')
exec(open('/home/claude/eval/gd3/tests/gshots.py').read().split('async def main():')[0])
JS="""()=>{const r=e=>{if(!e||!e.getClientRects().length)return null;if(e.tagName==='H1'){const g=document.createRange();g.selectNodeContents(e);return g.getBoundingClientRect()}return e.getBoundingClientRect()};const vis=e=>!!(e&&e.getClientRects().length&&getComputedStyle(e).visibility!=='hidden'&&e.getBoundingClientRect().width>0);
 const h=document.querySelector('#lobby .ltop');const parts=[h.querySelector('.logo'),h.querySelector('h1'),h.querySelector('.hgem'),[...document.querySelectorAll('.tabbar.tbw')].find(vis),h.querySelector('.nickchip'),h.querySelector('.hrule'),h.querySelector('[data-k=set]')].filter(e=>e&&vis(e));
 const ov=[];for(let i=0;i<parts.length;i++)for(let j=i+1;j<parts.length;j++){const a=r(parts[i]),b=r(parts[j]);if(a&&b&&a.left<b.right-0.5&&b.left<a.right-0.5&&a.top<b.bottom&&b.top<a.bottom)ov.push(parts[i].className+'|'+parts[j].className)}
 const out=[];for(const e of parts){const b=r(e);if(b.right>innerWidth+0.5||b.left<-0.5)out.push(e.className||e.tagName)}
 const h1=h.querySelector('h1');const h1clip=h1.scrollWidth>h1.clientWidth+1;const h1w=[h1.scrollWidth,h1.clientWidth];
 const bar=[...document.querySelectorAll('.tabbar')].find(vis);const btns=[...bar.querySelectorAll('button')].filter(vis);
 const lab=btns.map(b=>{const s=b.querySelector('span');return s?{t:s.textContent,w:Math.round(s.getBoundingClientRect().width),bw:Math.round(b.getBoundingClientRect().width),h:Math.round(b.getBoundingClientRect().height),clip:s.scrollWidth>s.clientWidth+1||s.getClientRects().length>1}:null});
 const small=[...document.querySelectorAll('#lobby button,#lobby [role=button]')].filter(vis).map(b=>[b,r(b)]).filter(([b,x])=>x.width<44&&x.height<44&&!b.closest('.rcards')).map(([b,x])=>(b.getAttribute('aria-label')||b.textContent).trim().slice(0,20)+':'+Math.round(x.width)+'x'+Math.round(x.height));
 const nt=document.querySelector('#nickTxt');const nch=Math.floor(nt.clientWidth/(nt.scrollWidth/nt.textContent.length)+0.05);return {nch,tight:h.classList.contains('tight'),gem:(h.querySelector('.hgem')||{}).textContent,h1w,w:innerWidth,sw:document.documentElement.scrollWidth,ov,out,h1clip,nick:Math.round(r(h.querySelector('.nickchip')).width),lab,small}}"""
NAMES=[('가나다라마바사아자차카타',12345),('슬레열스나야',820),('슬레열스나야',1234),('가나다라마바사',99999),('abcdefghijkl',12345),('성민',0)]
async def names(b):
    for w in (360,375,390):
        for nm,g in NAMES:
            seed();ctx,p=await ctxpage(b,w,740,'dark',name=nm,games=False);await asyncio.sleep(1)
            await ev(p,f"ECO.w&&(ECO.w.g={g});ecoPaint()");await asyncio.sleep(0.3);r=await p.evaluate(JS)
            print('NAME',w,nm,g,'visible',r['nch'],'/',len(nm),'tight' if r['tight'] else 'title','ov',r['ov'],'sw',r['sw'],flush=True);await ctx.close()
async def main():
    async with async_playwright() as pw:
        b=await pw.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
        bad=0
        await names(b)
        if os.environ.get('ONLYN'): return
        for w,h,th,big in [(320,640,'dark',0),(320,640,'dark',1),(390,844,'dark',1),(412,915,'dark',1),(430,932,'dark',1),(375,667,'dark',1),(360,740,'dark',0),(360,740,'light',1),(375,667,'dark',0),(390,844,'dark',0),(412,915,'light',0),(600,960,'dark',0),(768,1024,'dark',0),(844,390,'dark',0),(1023,768,'dark',0),(1024,768,'dark',0),(1100,800,'dark',0),(1279,800,'dark',0),(1280,800,'dark',0),(1366,768,'dark',0),(1600,900,'dark',0),(1920,1080,'light',0),(2560,1440,'dark',0)]:
            seed();ctx,p=await ctxpage(b,w,h,th,name='가나다라마바사아자차카타',games=False)
            if big: await ev(p,"document.body.classList.add('big')")
            await asyncio.sleep(1.2);await ev(p,"ECO.w&&(ECO.w.g=12345);ecoPaint()");await asyncio.sleep(0.3);r=await p.evaluate(JS)
            flag=r['sw']>r['w'] or r['ov'] or r['out'] or r['h1clip'] or any(l and l['clip'] for l in r['lab'])
            bad+=bool(flag)
            print(w,h,th,'nick',r['nch'],'/12','tight' if r['tight'] else '-','gem',r['gem'],'h1',r.get('h1w'),'big' if big else '', 'BAD' if flag else 'ok','sw',r['sw'],'ov',r['ov'],'out',r['out'],'h1clip',r['h1clip'],'nick',r['nick'],'tabs',[(l['t'],l['bw'],l['h']) for l in r['lab'] if l][:7],'small',r['small'][:6],flush=True)
            await ctx.close()
        print('BAD',bad,'errors',[e for e in ERRS if 'ERR_' not in e][:5]);await b.close()
asyncio.run(main())
