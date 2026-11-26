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
        await ev(p1,"(L.start(null,'mid'),renderAll(),0)");await local_turn(p1,9);await asyncio.sleep(3.5)
        await p1.click('#oppbar [data-act=cnthelp]');await asyncio.sleep(.6);print('help:',await txt(p1,'#dlg'));await p1.screenshot(path='/tmp/bt/cnthelp.png')
        await p1.click('#dlg [data-act=dlgok]');await asyncio.sleep(.3)
        await ev(p1,"(L.start(null,'ultimate'),renderAll(),0)");await local_turn(p1,9);await asyncio.sleep(3.5)
        print('godlike pill:',await p1.evaluate("()=>document.querySelectorAll('#oppbar .cnt').length"),await ev(p1,"L.s.ai"))
        print('errors',errs);await b.close()
asyncio.run(main())
