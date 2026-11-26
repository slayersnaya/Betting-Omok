# 시트(lsheet)·대화창(#dlg) 화면 맞춤 점검: 낮은 창·넓은 화면에서 머리(제목·닫기)가 화면 안에 있고 시트가 화면을 넘지 않는지
import asyncio, os, sys, json
os.environ.setdefault('WEBDIR','/home/claude/eval/gd3/web');os.environ.setdefault('GPORT','8863')
exec(open('/home/claude/eval/gd3/tests/gshots.py').read().split('async def main():')[0])
OUTD=os.environ.get('SHOTD','')
M="""()=>{const e=[...document.querySelectorAll('.lsheet:not(.hide),#dlg:not(.hide) .card')].find(x=>x.getClientRects().length);if(!e)return null;const r=e.getBoundingClientRect(),h=e.matches('#dlg .card')?e:e.querySelector('.shh,h2,h3');const hr=h?h.getBoundingClientRect():null;const sc=[e,...e.querySelectorAll('*')].some(x=>{const s=getComputedStyle(x);return /(auto|scroll)/.test(s.overflowY)&&x.scrollHeight>x.clientHeight+2});
 return {id:e.id||'dlg',top:Math.round(r.top),bot:Math.round(r.bottom),H:innerHeight,head:hr?[Math.round(hr.top),Math.round(hr.bottom)]:null,scroll:sc,over:e.scrollHeight>e.clientHeight+2}}"""
SHEETS=[('shop',"ecoOpen('shop')"),('set',"openSheet('set')"),('nick',"openSheet('nick')"),('friend',"openSheet('friend')"),('local',"openSheet('local')"),('acc',"openSheet('acc')"),('fadd',"openSheet('fadd')"),('fset',"openSheet('fset')"),('prof',"frOpenProf(SEAT)"),('prof2',"frOpenProf('uF1aaaaaaaaaaaaaaaa1')"),('chat',"frOpenChat('uF1aaaaaaaaaaaaaaaa1')"),('puz',"pzOpen()"),('att',"attShow(-1)"),('item',"ecoItemTap('x1')")]
async def main():
    bad=0
    async with async_playwright() as pw:
        b=await pw.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
        for w,h in [(1280,720),(1366,768),(1600,900),(1920,1000),(1920,1080),(2560,1300),(2560,1400),(2560,1440),(390,844),(360,640),(844,390)]:
            seed();ctx,p=await ctxpage(b,w,h,'dark',games=False);await asyncio.sleep(1.2)
            for k,js in SHEETS:
                await closeall(p);await ev(p,js);await p.wait_for_timeout(450);r=await p.evaluate(M)
                if not r: print(w,h,k,'(none)');continue
                ok=r['top']>=-1 and r['bot']<=r['H']+1 and r['head'] and r['head'][0]>=0 and r['head'][1]<=r['H']
                bad+=not ok
                if not ok or k in ('set','prof','chat'): print(w,h,k,'OK' if ok else 'BAD',r,flush=True)
                if OUTD and (not ok or (k=='set' and w>=1920)): await p.screenshot(path=f'{OUTD}/sheet_{w}x{h}_{k}.png')
            await ctx.close()
        print('BAD',bad,'errors',[e for e in ERRS if 'ERR_' not in e][:4]);await b.close()
asyncio.run(main())
