# 보상 띠: 상점 팀 코드가 붙었을 때(받을 보상 ready) 모양 미리보기 — 가짜 공급자
import asyncio,os
os.environ.setdefault('GPORT','8837')
exec(open('/home/claude/eval/gd2/tests/gshots.py').read().split('async def main():')[0])
DEMO="rwAdd({id:'demo',order:0,items:()=>[{id:'m0',t:'대국 3판',st:'ready',g:10},{id:'p2',t:'골드 첫 도달',st:'ready',g:50},{id:'m2',t:'랭크전 1판',st:'prog',p:'0/1'}],claim:async()=>{RW.prov.delete('demo');toast('보상 받기 · 구슬 +60')}})"
async def main():
    async with async_playwright() as pw:
        b=await pw.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
        for tag,w,h,th in [('ph',390,844,'dark'),('ph',390,844,'light'),('s360',360,740,'dark'),('pc',1280,800,'dark')]:
            seed();ctx,p=await ctxpage(b,w,h,th,games=False);n=f'{tag}_{th}'
            await ev(p,"lrm('bo-pz');renderPzTile()");await ev(p,DEMO);await shot(p,n+'_rw_ready')
            await tab(p,'rank');await shot(p,n+'_rw_pip')
            await tab(p,'home');await p.click('[data-act=rwclaim]');await p.wait_for_timeout(600);await shot(p,n+'_rw_after')
            await ctx.close()
        print('errors',ERRS);await b.close()
asyncio.run(main())
