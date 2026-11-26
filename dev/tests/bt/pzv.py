import asyncio,os
os.environ['WEBDIR']='/tmp/webT'
S=open('/tmp/bt/rklg.py').read();S=S[:S.rindex('async def main():')].replace('8863','8872')
exec(S)
JS="""()=>{const ev=window.__T.ev;let bad=0,maxn=0;const out=[];
 for(let i=0;i<120;i++){const d=new Date(Date.UTC(2026,10,1+i)).toISOString().slice(0,10);const pz=ev('pzMake')(d);if(!pz)continue;
  const svg=ev('pzBoardSVG')(pz);const m=/viewBox="0 0 ([\\d.]+)/.exec(svg);const n=Math.round((+m[1]-36)/30)+1;maxn=Math.max(maxn,n);
  const pts=ev('pzPts')(pz);// 보이는 범위 확인
  const vis=(svg.match(/url\\(#fxs/g)||[]).length;out.push(n)}
 const pz=ev('pzMake')('2026-11-27');return {maxn,ns:out.slice(0,30).join(','),today:ev('pzPts')(pz).length}}"""
async def main():
    errs=[]
    async with async_playwright() as pw:
        b=await pw.chromium.launch()
        p=await pg(b,errs,"localStorage.setItem('bo-rkintro','1');localStorage.setItem('bo-rklg','1');localStorage.setItem('bo-nick','x');")
        print(await p.evaluate(JS))
        await p.evaluate("()=>{const ev=window.__T.ev;const d=document.createElement('div');d.style.cssText='position:fixed;inset:0;z-index:9999;background:#111;padding:10px';d.innerHTML=ev('pzBoardSVG')(ev('pzMake')('2026-11-27')).replace('<svg ','<svg width=\"600\" height=\"600\" ');document.body.appendChild(d)}")
        await asyncio.sleep(.5);await p.screenshot(path='/tmp/bt/pz27.png',clip={'x':0,'y':0,'width':640,'height':640})
        # 랭크 AI 분포: 내 점수 근처 150 안 6명
        print(await p.evaluate("""()=>{const ev=window.__T.ev;ev('rankCompute()');const B=ev('BOTS').map(b=>({lv:b.k,r:Math.round(ev('rkP')('bot:'+b.id).r)}));const res={};
          for(const my of [900,1000,1100,1150,1200,1250,1300,1350]){const c=B.map(x=>({...x,d:Math.abs(x.r-my)})).sort((a,b)=>a.d-b.d).filter(x=>x.d<=150).slice(0,6);const cnt=[0,0,0,0];c.forEach(x=>cnt[x.lv]++);res[my]=cnt.join('/')}
          const band=[0,0,0,0,0,0];return {res,top:B.sort((a,b)=>b.r-a.r).slice(0,20).map(x=>x.lv+':'+x.r).join(' ')}}"""))
        print('errors',errs);await b.close()
asyncio.run(main())
