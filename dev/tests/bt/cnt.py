import asyncio,os,json
os.environ['WEBDIR']='/tmp/webT';os.environ['FPORT']='9831'
S=open('/home/claude/eval/spec/tests/spectest.py').read()
S=S[:S.index('async def main():')]
exec(S)
async def main():
    errs=[]
    async with async_playwright() as pw:
        b=await pw.chromium.launch();p1=await page(b,errs,'성민');await asyncio.sleep(3)
        await ev(p1,"(UI.aiLevel='mid',closeSheet(),leaveGame(),UI.mode='local',L.start(null,'mid'),show('game'),$('#cover').classList.add('hide'),renderAll(),0)")
        res=[]
        for k in range(4):
            r=await local_turn(p1,k);await asyncio.sleep(3.5)
            v=await p1.evaluate("()=>{const e=document.querySelector('#oppbar .pp.cnt');return e?e.textContent:''}")
            if k==0:await p1.screenshot(path='/tmp/bt/cnt0.png',clip={'x':0,'y':0,'width':390,'height':180})
            real=await ev(p1,"L.s.pts.B");res.append((r,v,real,await ev(p1,"JSON.stringify([cntOn(),cntMax(vstate(),'B'),vstate().me,vstate().t,vstate().phase,(rkP(SEAT)||{}).r])"),await p1.evaluate("()=>document.querySelector('#oppbar')?.innerHTML.slice(0,200)")))
        for x in res:print(x[0],repr(x[1]),x[2],x[3])
        await p1.screenshot(path='/tmp/bt/cnt1.png')
        ok=all(int(''.join(c for c in x[1] if c.isdigit()))>=x[2] for x in res if x[1])
        print('ok(최대치 ≥ 실제)',ok)
        # 플래티넘 승급 창
        await ev(p1,"(tupShow(TIERS.find(t=>t.n==='골드'),TIERS.find(t=>t.n==='플래티넘')),0)");await asyncio.sleep(3)
        await p1.screenshot(path='/tmp/bt/cnt2.png');print(await txt(p1,'#tup'))
        print('errors',errs);await b.close()
asyncio.run(main())
