import asyncio,os
os.environ['WEBDIR']='/tmp/webT'
src=open('/home/claude/firebase/fbtest.py').read().split('async def main():')[0].replace('PORT=8765','PORT=8833')
exec(src)
async def main():
    async with async_playwright() as pw:
        b=await pw.chromium.launch();errs=[]
        ctx=await b.new_context(viewport={'width':360,'height':800},device_scale_factor=2)
        await ctx.add_init_script("localStorage.setItem('bo-tut-done','1');localStorage.setItem('bo-rkintro','1');localStorage.setItem('bo-rklg','1');sessionStorage.setItem('bo-noatt','1');localStorage.setItem('bo-airec',JSON.stringify({pro:{w:1,l:0,d:0}}));localStorage.setItem('bo-nick','성민')")
        async def route(rt): await rt.fulfill(path=FAKE[rt.request.url.split('/')[-1]],content_type='application/javascript')
        await ctx.route('https://www.gstatic.com/**',route)
        p=await ctx.new_page();p.on('pageerror',lambda e:errs.append(str(e)));await p.expose_function('__fsSend',lambda j,p=p:asyncio.ensure_future(relay(p,j)));PAGES.append(p)
        await p.goto(f'http://127.0.0.1:{PORT}/index.html');await asyncio.sleep(1.5)
        for seq in ['WWWWWWWW','WWWWWWLLL','LLLLL']:
            r=await p.evaluate("""seq=>{const T=window.__T,me=T.seat(),now=Date.now();T.RK.bdocs=[...seq].map((c,i)=>{const gid='k'+(0x10000000+i).toString(16);return{id:me+'_'+gid,by:me,gid,bot:'b'+String(i%50).padStart(2,'0'),na:'성민',w:c==='W'?'me':'bot',turns:20,why:'오목',ended:now-(seq.length-i)*120e3}});
              const out=[];let prev=1000;for(let k=1;k<=seq.length;k++){const all=T.RK.bdocs;T.RK.bdocs=all.slice(0,k);T.rankCompute();const q=T.RK.map.get(me);out.push(seq[k-1]+(Math.round(q.r)-prev>=0?'+':'')+(Math.round(q.r)-prev));prev=Math.round(q.r);T.RK.bdocs=all}
              T.ev('renderRank()');document.querySelector('.tabbar [data-k=rank]').click();return out.join(' ')+' | '+document.querySelector('#rkMe').innerText.replace(/\\s+/g,' ')}""",seq)
            print(seq,r)
            await asyncio.sleep(0.3);await p.screenshot(path=f'/tmp/bt/strk_{seq}.png',clip={'x':0,'y':0,'width':360,'height':260})
        print('errors',errs);await b.close()
asyncio.run(main())
