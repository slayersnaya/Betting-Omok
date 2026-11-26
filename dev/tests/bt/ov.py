import asyncio,os
os.environ['WEBDIR']='/tmp/webT'
src=open('/home/claude/firebase/fbtest.py').read().split('async def main():')[0].replace('PORT=8765','PORT=8867')
exec(src)
JS="""()=>{const bd=window.__T.ev('emptyBoard()');for(let c=4;c<=9;c++)bd[9][c]=1;bd[8][6]=2;bd[10][7]=2;
 let d=document.getElementById('ovt');if(!d){d=document.createElement('div');d.id='ovt';d.style.cssText='position:fixed;inset:0;z-index:999;background:#111;padding:10px;width:500px';document.body.appendChild(d)}
 const Z=window.__T.ev('SZ');d.innerHTML='<svg viewBox="0 0 '+Z+' '+Z+'" width="480" height="480">'+window.__T.ev('boardSVG')(bd,{overs:[[[9,4],[9,9]]]})+'</svg>';const t=d.querySelector('.ovtag');return [!!t,d.querySelectorAll('line[stroke="#E5484D"]').length]}"""
async def main():
    errs=[]
    async with async_playwright() as pw:
        b=await pw.chromium.launch();p=await newpage(b,errs,'성민');await asyncio.sleep(2)
        print('first render (tag, red lines):',await p.evaluate(JS));await asyncio.sleep(0.6);await p.screenshot(path='/tmp/bt/ov1.png',clip={'x':0,'y':0,'width':520,'height':520})
        await asyncio.sleep(1.0);print('redraw at 1.6s:',await p.evaluate(JS))
        await asyncio.sleep(1.6);print('redraw at 3.2s:',await p.evaluate(JS));await p.screenshot(path='/tmp/bt/ov2.png',clip={'x':0,'y':0,'width':520,'height':520})
        print('errors',[e for e in errs if 'ERR_' not in e]);await b.close()
asyncio.run(main())
