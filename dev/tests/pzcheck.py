# 묘수 해설 검산: 여러 날 문제를 만들어, 해설의 '상대 필요 칩'이 상대 칩보다 크고(막기) 정답 예시가 판정을 통과하는지
import asyncio,os
os.environ.setdefault('WEBDIR','/home/claude/eval/gd3/web');os.environ.setdefault('GPORT','8867')
exec(open('/home/claude/eval/gd3/tests/gshots.py').read().split('async def main():')[0])
JS="""()=>{const T=window.__T,out=[];const d0=Date.UTC(2026,10,1);for(let k=0;k<70;k++){const day=new Date(d0+k*864e5).toISOString().slice(0,10);T.ev('PZ.cache=null');const pz=T.ev('pzMake')(day);if(!pz)continue;
 const ex=T.ev('pzExplain')(pz);let ok=true,why='';
 if(pz.type!=='pick'){if(!T.ev('pzJudge')(pz,pz.ex)){ok=false;why='ex 판정 실패'}
  if(pz.goal!=='win'){const m=ex.find(x=>/ = \\d+/.test(x));const t=m&&+(/= (\\d+)/.exec(m)||[])[1];if(!(t>pz.X)){ok=false;why='필요<=X '+m}}
  if(!ex.some(x=>x.includes('합 '+pz.best))){ok=false;why='합 없음'}}
 out.push({day,type:pz.type,goal:pz.goal,meSun:pz.meSun,X:pz.X,P:pz.P,best:pz.best,exa:pz.ex,ok,why,ex})}return out}"""
async def main():
    async with async_playwright() as pw:
        b=await pw.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
        seed();ctx,p=await ctxpage(b,390,844,games=False);await asyncio.sleep(1)
        r=await p.evaluate(JS);bad=[x for x in r if not x['ok']]
        print('문제',len(r),'실패',len(bad))
        for x in bad[:5]: print(x)
        seen=set()
        for x in r:
            k=(x['type'],x['goal'],x['meSun'])
            if k in seen: continue
            seen.add(k);print(k,x['day'],'X',x['X'],'best',x['best'],x['exa']);[print('   ',l) for l in x['ex']]
        await b.close()
asyncio.run(main())
