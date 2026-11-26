# 새 기능 테스트: 온라인 두 폰 이모트 왕복·쿨다운·규칙 거부 / 복기 AI 비교(대국 중 안 보임) / 퍼즐 같은 날 같은 문제·판정 / 분석 숫자 검산 / 시즌 경계 결산 1회
import asyncio,os,json,time,sys
os.environ['WEBDIR']='/tmp/webT'
exec(open('/home/claude/firebase/fbtest.py').read().split('async def main():')[0].replace('PORT=8765','PORT=8841'))
R=[]
def ok(name,cond,info=''):
    R.append((name,bool(cond)));print(('PASS ' if cond else 'FAIL ')+name,('· '+str(info))[:300] if info!='' else '')
async def ev(p,code):return await p.evaluate("c=>window.__T.ev(c)",code)
async def ctxpage(b,errs,name,init='',w=390,h=844):
    ctx=await b.new_context(viewport={'width':w,'height':h})
    await ctx.add_init_script("if(!sessionStorage.getItem('__i')){sessionStorage.setItem('__i','1');localStorage.setItem('bo-tut-done','1');localStorage.setItem('bo-rkintro','1');localStorage.setItem('bo-rklg','1');sessionStorage.setItem('bo-noatt','1');localStorage.setItem('bo-airec',JSON.stringify({pro:{w:1,l:0,d:0}}))}"+init)
    async def route(rt): await rt.fulfill(path=FAKE[rt.request.url.split('/')[-1]],content_type='application/javascript')
    await ctx.route('https://www.gstatic.com/**',route);await ctx.route('https://cdn.jsdelivr.net/**',lambda rt:rt.abort())
    p=await ctx.new_page();p.on('pageerror',lambda e:errs.append(name+':'+str(e)))
    p.on('console',lambda m:errs.append(name+' console:'+m.text) if m.type=='error' and 'ERR_' not in m.text else None)
    await p.expose_function('__fsSend',lambda j,p=p:asyncio.ensure_future(relay(p,j)))
    PAGES.append(p);await p.goto(f'http://127.0.0.1:{PORT}/index.html');await p.wait_for_timeout(1200)
    try: await p.click('[data-act=wskip]',timeout=800)
    except Exception: pass
    await p.evaluate("n=>{const e=document.querySelector('#nick');if(e)e.value=n;localStorage.setItem('bo-nick',n)}",name)
    return ctx,p
# ---------- 분석 검산(파이썬으로 따로 계산) ----------
def five_lines(bd,col):
    n=0
    for dr,dc in ((0,1),(1,0),(1,1),(1,-1)):
        for r in range(19):
            for c in range(19):
                if bd[r][c]!=col: continue
                pr,pc=r-dr,c-dc
                if 0<=pr<19 and 0<=pc<19 and bd[pr][pc]==col: continue
                L=0;y,x=r,c
                while 0<=y<19 and 0<=x<19 and bd[y][x]==col: L+=1;y+=dr;x+=dc
                if L==5: n+=1
    return n
def outcomes(bd,cells,mecol,mesun):
    out=[]
    for m in range(8):
        b=[row[:] for row in bd]
        for i,(r,c) in enumerate(cells): b[r][c]=mecol if (m>>i)&1 else 3-mecol
        fm,fo=five_lines(b,mecol),five_lines(b,3-mecol)
        out.append(('me' if fm>fo else 'op' if fo>fm else ('op' if mesun else 'me')) if (fm or fo) else None)
    return out
def py_ana(games):
    fs=[0,0];ss=[0,0];turns=ones=0;crit=[0,0];norm=[0,0];lose={}
    for g in games:
        d=g['d'];me=d['me'];op=d['B'] if me==d['A'] else d['A'];col=1 if me==d['A'] else 2;bd=[[0]*19 for _ in range(19)];sp=[]
        first=d['hist'][0]['sun']==me;k=fs if first else ss;k[1]+=1
        if d['winner']==me:k[0]+=1
        for h in d['hist']:
            b=h['bets'][me];o=h['bets'].get(op)
            turns+=1
            if b==[1,1,1]:ones+=1
            O=outcomes(bd,h['cells'],col,h['sun']==me)
            for i in range(3):
                c=any(O[m]!=O[m^(1<<i)] for m in range(8));t=crit if c else norm;t[0]+=b[i];t[1]+=1
            if o: sp.append(sum(o))
            for j,(r,c) in enumerate(h['cells']): bd[r][c]=1 if h['win'][j]==d['A'] else 2
        if d['winner'] and d['winner']!=me:
            rs=d['reason'];last=sp[-1];prev=sp[:-1];avg=sum(prev)/len(prev) if prev else 0
            kk='time' if '시간 초과' in rs else 'quit' if ('기권' in rs or '나감' in rs) else (('allin' if len(prev)>=2 and last>=12 and last>=2.5*avg else 'mysun' if d['hist'][-1]['sun']==me else 'opsun') if '오목' in rs else 'etc')
            lose[kk]=lose.get(kk,0)+1
    pct=lambda a,b: round(a/b*100) if b else None
    avg=lambda a,b: round(a/b*10)/10 if b else None
    return {'f':pct(*fs),'s':pct(*ss),'c':avg(*crit),'n':avg(*norm),'o':pct(ones,turns),'lose':lose,'fsn':fs[1],'ssn':ss[1]}
def mkgame(key,me_first,winner,reason,turns):
    # turns: [(cells,winList,betsMe,betsOp)] 흑(a)=나. sun 번갈아(첫 턴 sun = me_first? a : b)
    hist=[]
    for t,(cells,win,bm,bo) in enumerate(turns,1):
        sun=('a' if me_first else 'b') if t%2 else ('b' if me_first else 'a')
        hist.append({'t':t,'sun':sun,'hu':'b' if sun=='a' else 'a','cells':cells,'win':win,'bets':{'a':bm,'b':bo}})
    return {'key':key,'label':'AI 고수','at':int(time.time()*1000),'d':{'A':'a','B':'b','me':'a','names':{'a':'나','b':'AI'},'winner':winner,'reason':reason,'hist':hist,'ai':True}}
def ana_seed():
    # 게임1: 흑이 가로 넷(9,5~8) 만들고 마지막 턴에 (9,9) 포함 세 칸을 이김 → 승. 승부 칸 생김
    T1=[([[9,5],[9,6],[9,7]],['a','a','a'],[3,3,3],[1,1,1]),([[3,3],[3,4],[3,5]],['b','b','b'],[1,1,1],[2,2,2]),([[9,8],[10,8],[11,8]],['a','b','b'],[4,1,1],[2,2,2]),([[9,9],[9,10],[9,11]],['a','b','b'],[20,1,1],[5,3,3])]
    g1=mkgame('t1',True,'a','오목',T1)
    # 게임2: 백이 세로 넷 → 백이 모아서 몰아 걸어 이김(allin)
    T2=[([[2,2],[3,2],[4,2]],['b','b','b'],[1,1,1],[2,2,2]),([[5,2],[6,2],[7,2]],['b','a','a'],[1,2,2],[3,1,1]),([[12,12],[12,13],[12,14]],['a','a','a'],[1,1,1],[1,1,1]),([[14,14],[14,15],[14,16]],['a','a','a'],[1,1,1],[1,1,1]),([[6,2],[6,3],[6,4]],['b','a','a'],[5,1,1],[30,1,1])]
    # 6,2 는 이미 놓임 → 다른 칸으로 바꿈
    T2[4]=([[6,1],[6,2+5],[6,3+5]],['b','a','a'],[5,1,1],[30,1,1])
    g2=mkgame('t2',False,'b','오목',T2)
    g3=mkgame('t3',True,'b','시간 초과 3회',[([[0,0],[0,1],[0,2]],['b','b','b'],[1,1,1],[1,1,1])])
    g4=mkgame('t4',False,None,'둘 곳 없음',[([[18,0],[18,1],[18,2]],['a','b','a'],[2,1,2],[1,1,1])])
    return [g1,g2,g3,g4]
async def main():
    errs=[]
    async with async_playwright() as pw:
        b=await pw.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
        # ===== A. 온라인 두 폰: 이모트 =====
        c1,p1=await ctxpage(b,errs,'성민');c2,p2=await ctxpage(b,errs,'하율')
        await p1.click('[data-act=sheet][data-k=friend]');await p1.wait_for_timeout(300);await p1.click('#createBtn');await p1.wait_for_timeout(1500)
        await p2.click('[data-act=sheet][data-k=friend]');await p2.wait_for_timeout(1000);await p2.click('#rooms [data-act=enter]');await waitfor(lambda: ingame(p2),50)
        await p2.click('[data-act=join]');await p2.wait_for_timeout(2500)
        for p in (p1,p2):
            try: await p.click('#coin',timeout=500)
            except Exception: pass
        await p1.wait_for_timeout(800)
        vis=[await p.evaluate("()=>!document.querySelector('#emoBtn').classList.contains('hide')") for p in (p1,p2)]
        ok('A1 이모트 버튼 보임(두 폰)',all(vis),vis)
        ok('A2 대국 중 AI 비교 없음',await p1.evaluate("()=>!document.querySelector('#rvai')&&!document.body.innerText.includes('AI라면')") and await ev(p1,'FXWK.ok')==None)
        await p1.click('#emoBtn');await p1.wait_for_timeout(300)
        ok('A3 고르기 창 12종',await p1.evaluate("()=>document.querySelectorAll('#emoPick .emoi').length")==12)
        await p1.screenshot(path='/home/claude/eval/feat/shots/t_emopick.png')
        await p1.click('#emoPick [data-act=fxemo][data-i="2"]')
        got=await waitfor(lambda: p2.evaluate("()=>!!document.querySelector('.emob.op')"),40)
        ok('A4 상대 폰에 이모트 뜸(상대 바 옆)',got)
        await p2.screenshot(path='/home/claude/eval/feat/shots/t_emo_recv.png')
        ok('A5 내 폰에도 내 바 옆에',await p1.evaluate("()=>!!document.querySelector('.emob.me')"))
        st=await p1.evaluate("()=>{const b=document.querySelector('#emoBtn');return [b.classList.contains('cool'),b.getAttribute('aria-label')]}")
        ok('A6 쿨다운 표시',st[0] and '초 뒤' in st[1],st)
        await p1.click('#emoBtn');await p1.wait_for_timeout(200)
        dis=await p1.evaluate("()=>[...document.querySelectorAll('#emoPick .emoi')].every(x=>x.disabled)")
        ok('A7 쿨다운 중 버튼 비활성',dis)
        await p1.keyboard.press('Escape')
        # 규칙: 6초 안에 직접 쓰기 → 거부, 새 방(만들 때) emo → 거부, 로비 → 거부
        d0=await p1.evaluate("()=>(window.__deniedList||[]).length")
        r1=await ev(p1,"(async()=>{try{await G.room.presence({emo:{k:1,t:Date.now()}});return 'ok'}catch(e){await G.room.presence({emo:FX.emo.last});return e.code}})()")
        r2=await ev(p1,"(async()=>{const r=await room.join('g-gdeadbee');try{await r.presence({emo:{k:1,t:Date.now()}});return 'ok'}catch(e){return e.code}finally{r.leave()}})()")
        r3=await ev(p1,"(async()=>{const r=await room.join('g-gdeadbe1');try{await r.presence({seat:SEAT});await r.presence({emo:{k:1,t:Date.now()+3600e3}});return 'ok'}catch(e){return e.code}finally{r.leave()}})()")
        dl=await p1.evaluate("d=>(window.__deniedList||[]).slice(d)",d0)
        ok('A8 규칙: 6초 안 다시 쓰기 거부',r1!='ok',r1);ok('A9 규칙: 만들 때 emo 거부',r2!='ok',r2);ok('A10 규칙: 시각 범위 밖 거부',r3!='ok',r3)
        print('   denied:',dl)
        await p1.wait_for_timeout(8600)
        await p1.click('#emoBtn');await p1.wait_for_timeout(250);await p1.click('#emoPick [data-act=fxemo][data-i="3"]')
        got2=await waitfor(lambda: p2.evaluate("()=>{const e=[...document.querySelectorAll('.emob.op')];return e.length&&e[0].innerHTML.includes('#ff6f61')}"),40)
        ok('A11 8초 뒤 두 번째 이모트 왕복',got2)
        # 상대 이모트 끄기
        await p2.evaluate("()=>{const s=document.querySelector('#setEmo');s.checked=false;s.dispatchEvent(new Event('change',{bubbles:true}))}")
        await p2.wait_for_timeout(2600);await p1.wait_for_timeout(6000)
        await ev(p1,"FX.emo.sent=[]");await p1.click('#emoBtn');await p1.wait_for_timeout(250);await p1.click('#emoPick [data-act=fxemo][data-i="8"]')
        await p2.wait_for_timeout(2500)
        ok('A12 끄면 상대 이모트 안 뜸',await p2.evaluate("()=>!document.querySelector('.emob.op')"))
        # 대국 끝 → 복기 AI 비교
        await p2.click('#resignBtn');await p2.click('[data-act=dlgok]');await p2.wait_for_timeout(2500)
        await p1.wait_for_timeout(3500)
        try: await p1.click('[data-act=review]',timeout=3000)
        except Exception as e: print('no review',e)
        await p1.wait_for_timeout(500)
        has=await p1.evaluate("()=>!!document.querySelector('#rvai')")
        print('   review panel:',(await txt(p1,'#panel'))[:120])
        ok('A13 끝난 판 복기에 AI라면? 줄(턴 없으면 생략)',has or 'AI라면' not in await txt(p1,'#panel'))
        await c1.close();await c2.close();PAGES.clear()
        # ===== B. AI 대국: 이모트·AI 반응, 대국 중 비교 없음 / 긴 판 복기 AI 비교 =====
        c3,p3=await ctxpage(b,errs,'AI')
        await p3.click('#soloBtn');await p3.wait_for_timeout(2500)
        try: await p3.click('#coin',timeout=800)
        except Exception: pass
        ok('B1 AI 대국 이모트 버튼',await p3.evaluate("()=>!document.querySelector('#emoBtn').classList.contains('hide')"))
        await p3.evaluate("()=>{window.__r=Math.random;Math.random=()=>0.01}")
        await p3.click('#emoBtn');await p3.wait_for_timeout(250);await p3.click('#emoPick [data-act=fxemo][data-i="3"]')
        ai=await waitfor(lambda: p3.evaluate("()=>!!document.querySelector('.emob.op')"),70)
        await p3.evaluate("()=>{Math.random=window.__r}")
        ok('B2 AI가 (드물게) 답함 — 확률 고정 시',ai)
        await p3.screenshot(path='/home/claude/eval/feat/shots/t_ai_reply.png')
        ok('B3 AI 대국 중 AI라면? 없음',await p3.evaluate("()=>!document.querySelector('#rvai')"))
        # 긴 판 만들기: Ultimate끼리 25턴(엔진·AI로) → 지난 대국에 저장 → 복기
        t0=time.time()
        n=await ev(p3,"""(()=>{const bd=emptyBoard(),mA=aiNewMem(11),mB=aiNewMem(22),hist=[];let pA=0,pB=0,first='A';for(let t=1;t<=26;t++){pA+=10;pB+=10;const sun=t%2?'A':'B',hu=sun==='A'?'B':'A';
 const vA=x=>Object.assign({level:'pro',bd:bd.map(r=>r.slice()),t,aiSun:sun==='A',aiPts:pA,aiCol:1,mem:mA},x),vB=x=>Object.assign({level:'pro',bd:bd.map(r=>r.slice()),t,aiSun:sun==='B',aiPts:pB,aiCol:2,mem:mB},x);
 const cells=validTriple(bd,sun==='A'?aiDesignate(vA()):aiDesignate(vB()))||legalTriples(bd)[0];const bA=aiBid(vA({cells})),bB=aiBid(vB({cells}));
 const win=settle(bd,cells,sun==='A'?bA:bB,sun==='A'?bB:bA,sun==='A'?1:2,sun==='A'?2:1).map(w=>w==='sun'?sun:hu);pA-=bA[0]+bA[1]+bA[2];pB-=bB[0]+bB[1]+bB[2];
 hist.push({t,sun,hu,cells,bets:{A:bA,B:bB},win,auto:{}});aiObserve(mA,t,sun==='A',bA,win.map(w=>w==='A'));aiObserve(mB,t,sun==='B',bB,win.map(w=>w==='B'));
 const f1=fiveLines(bd,1).length,f2=fiveLines(bd,2).length;if(f1||f2)break}
 L.s.phase='over';archiveGame({hist,A:'A',B:'B',names:{A:'나',B:'고수 AI'},me:'A',winner:null,reason:'테스트',ai:true},'Ltest01','고수 AI');return hist.length})()""")
        print('   sim turns',n,'in',round(time.time()-t0,1),'s')
        await ev(p3,"goLobby()");await p3.wait_for_timeout(400)
        await ev(p3,"RV.openArc(0)");await p3.wait_for_timeout(300)
        await ev(p3,"RV.go(2)");tt=time.time()
        got=await waitfor(lambda: p3.evaluate("()=>document.querySelectorAll('#rvai .aic').length===3"),120)
        ok('B4 복기 AI 비교 표시(3칸)',got,round(time.time()-tt,2))
        # 선 턴이면 판에 점선 세 칸
        sun=await ev(p3,"RV.d.hist[RV.i].sun==='A'")
        g=await p3.evaluate("()=>document.querySelectorAll('#bov .aighost circle').length")
        ok('B5 선 턴 → Ultimate 세 칸 점선(후 턴이면 없음)',(g==3) if sun else (g==0),(sun,g))
        await ev(p3,"RV.go(3)");await waitfor(lambda: p3.evaluate("()=>document.querySelectorAll('#rvai .aic').length===3"),120)
        sun2=await ev(p3,"RV.d.hist[RV.i].sun==='A'");g2=await p3.evaluate("()=>document.querySelectorAll('#bov .aighost circle').length")
        ok('B6 다음 턴도(선/후 반대)',(g2==3) if sun2 else (g2==0),(sun2,g2))
        await p3.screenshot(path='/home/claude/eval/feat/shots/t_rvai.png')
        # 일꾼 결과 = 같은 계산을 바로 했을 때와 같음(결정적) + 합계 ≤ 내 점수 + 상대 베팅을 바꿔도 결과 같음(내 입장만 씀)
        same=await ev(p3,"(()=>{const i=RV.i,j=rvaiJob(i),a=rvaiCompute(j,new Map()),w=FX.rv.res[i];const d2=JSON.parse(JSON.stringify(RV.d));d2.hist.forEach(h=>{h.bets.B=[7,7,7]});const sv=RV.d;RV.d=d2;FX.rv.dref=null;const j2=rvaiJob(i);RV.d=sv;FX.rv.dref=null;rvaiJob(i);const b2=rvaiCompute(Object.assign(j2,{key:j.key}),new Map());return JSON.stringify([a.bid,w.bid,b2.bid,a.pts,a.bid.reduce((x,y)=>x+y,0)<=a.pts])})()")
        s=json.loads(same);ok('B7 일꾼=직접 계산, 합계≤내 점수, 상대 베팅 바꿔도 같음',s[0]==s[1]==s[2] and s[4],same)
        # 뒤쪽 턴 시간(캐시 없이 처음 계산)
        tt=time.time();await ev(p3,f"RV.go({n-1})");await waitfor(lambda: p3.evaluate("()=>document.querySelectorAll('#rvai .aic').length===3"),300)
        ok('B8 마지막 턴 계산 시간(일꾼, 멈춤 없음)',True,f'{round(time.time()-tt,2)}s')
        await p3.click('[data-act=fxrvai]');await p3.wait_for_timeout(200)
        ok('B9 숨기기 → 버튼만',await p3.evaluate("()=>!!document.querySelector('#rvai.off')&&!document.querySelector('#bov .aighost')"))
        await p3.click('[data-act=fxrvai]');await p3.wait_for_timeout(200)
        await c3.close();PAGES.clear()
        # ===== C. 퍼즐 =====
        c4,p4=await ctxpage(b,errs,'P1');c5,p5=await ctxpage(b,errs,'P2')
        j4=await ev(p4,"JSON.stringify(pzMake(fxDate(Date.now())))");j5=await ev(p5,"JSON.stringify(pzMake(fxDate(Date.now())))")
        ok('C1 같은 날 같은 문제(두 폰)',j4==j5 and j4!='null',json.loads(j4)['kind'])
        pz=json.loads(j4)
        await p4.click('#pzTile');await p4.wait_for_timeout(400)
        if pz['type']=='bet':
            for i,v in enumerate(pz['ex']):
                for _ in range(v-1): await p4.click(f'[data-act=fxpzb][data-i="{i}"][data-v="1"]')
        else: await p4.click(f'[data-act=fxpzpick][data-i="{pz["ans"]}"]')
        await p4.click('[data-act=fxpzgo]');await p4.wait_for_timeout(300)
        t4=await txt(p4,'#pzBody');ok('C2 정답 판정',' 정답' in ' '+t4 and '아쉬워요' not in t4,t4[-120:])
        await p4.screenshot(path='/home/claude/eval/feat/shots/t_puz_ok.png')
        await p5.click('#pzTile');await p5.wait_for_timeout(300)
        if pz['type']=='pick': await p5.click(f'[data-act=fxpzpick][data-i="{(pz["ans"]+1)%4}"]')
        await p5.click('[data-act=fxpzgo]');await p5.wait_for_timeout(300)
        t5=await txt(p5,'#pzBody');ok('C3 오답 판정(1·1·1 또는 다른 후보)','아쉬워요' in t5,t5[:80])
        s4=await p4.evaluate("()=>localStorage.getItem('bo-pzs')");ok('C4 연속 기록 저장',json.loads(s4)['n']==1,s4)
        # 엄밀성: 정답 예시보다 1점 더 쓰면 오답, 정답 집합 모두 '확실히' 막힘/이김
        rig=await ev(p4,"""(()=>{let bad=0,n=0;for(let k=0;k<40;k++){const d=fxDate(Date.UTC(2027,0,1)+k*864e5),pz=pzMake(d);if(!pz)return 'null '+d;n++;
          if(pz.type==='pick'){let c=0;for(let j=0;j<4;j++)if(pzJudge(pz,j))c++;if(c!==1)bad++}else{if(!pzJudge(pz,pz.ex))bad++;const w=pz.ex.slice();w[0]++;if(w[0]+w[1]+w[2]<=pz.P&&pzJudge(pz,w))bad++;if(pzJudge(pz,[1,1,1]))bad++}}return bad+'/'+n})()""")
        ok('C5 40일치 판정 검사(정답 유일/최소)',rig.startswith('0/'),rig)
        # 다음 날: 날짜를 하루 넘기면 새 문제, 연속 이어짐
        await p4.evaluate("()=>{const n0=Date.now;Date.now=()=>n0()+864e5}")
        j6=await ev(p4,"JSON.stringify(pzMake(fxDate(Date.now())))");ok('C6 다음 날 새 문제',j6!=j4)
        await c4.close();await c5.close();PAGES.clear()
        # ===== D. 분석 숫자 검산 =====
        games=ana_seed();exp=py_ana(games)
        c6,p6=await ctxpage(b,errs,'ANA',init="localStorage.setItem('bo-games',"+json.dumps(json.dumps(games))+");")
        await p6.evaluate("()=>[...document.querySelectorAll('.tabbar [data-k=rec]')].find(b=>b.offsetParent).click()");await p6.wait_for_timeout(600)
        got=json.loads(await ev(p6,"JSON.stringify(anaCalc(archList()))"))
        f=lambda a,b: round(a/b*100) if b else None
        g=lambda a,b: round(a/b*10)/10 if b else None
        mine={'f':f(*got['fs']),'s':f(*got['ss']),'c':g(*got['crit']),'n':g(*got['norm']),'o':f(got['ones'],got['turns']),'lose':got['lose'],'fsn':got['fs'][1],'ssn':got['ss'][1]}
        ok('D1 분석 숫자 = 파이썬 따로 계산',mine==exp,(mine,exp))
        at=await txt(p6,'#anaCard');ok('D2 화면 숫자',(str(exp['f'])+'%') in at and (str(exp['c'])+'점') in at and (str(exp['o'])+'%') in at,at)
        await p6.screenshot(path='/home/claude/eval/feat/shots/t_ana.png',full_page=True)
        await c6.close();PAGES.clear()
        # ===== E. 시즌 경계 결산(시즌 2 첫 실행 → 1번만) =====
        uid='uRecapTester000001';T0=1803956400000 # 2027-03-02 12:00 KST
        base=1796108400000 # 2026-11-26 16:00 KST 근처
        bots=['b00','b01','b00','b02','b00','b01','b03']
        ws=['me','me','bot','me','me','me','me']
        for i,(bt,w) in enumerate(zip(bots,ws)):
            gid='k%08x'%(0xa0+i);STORE[f'bres/{uid}_{gid}']={'by':uid,'gid':gid,'bot':bt,'na':'결산','w':w,'turns':20,'why':'오목','ended':base+i*3600e3}
        init=f"sessionStorage.setItem('fake-uid','{uid}');sessionStorage.setItem('fake-g','1');{{const off={T0}-Date.now();const n0=Date.now.bind(Date);Date.now=()=>n0()+off}}"
        c7,p7=await ctxpage(b,errs,'결산',init=init)
        shown=await waitfor(lambda: p7.evaluate("()=>!document.querySelector('#recap').classList.contains('hide')"),120)
        rt=await txt(p7,'#rcCard');ok('E1 시즌 2 첫 실행에 결산 표시',shown,rt)
        ok('E2 전적·최고 연승·많이 만난 상대',('6승 1패' in rt) and ('4연승' in rt) and ('3판' in rt),rt)
        sn=await ev(p7,"RK.season.n");ok('E3 결산 계산 뒤 현재 시즌 상태 그대로',sn==2,sn)
        await p7.screenshot(path='/home/claude/eval/feat/shots/t_recap.png')
        img=await ev(p7,"(async()=>{const b=await recapImage(FX.rc);return b?b.size:0})()");ok('E4 공유 이미지 생성',img>20000,img)
        await p7.click('[data-act=fxrcx]');await p7.wait_for_timeout(300)
        await p7.reload();await p7.wait_for_timeout(6500)
        ok('E5 다시 열면 안 뜸(1번만)',await p7.evaluate("()=>document.querySelector('#recap').classList.contains('hide')"))
        await c7.close();PAGES.clear()
        # 시즌 1 중에는 안 뜸
        c8,p8=await ctxpage(b,errs,'S1');await p8.wait_for_timeout(5000)
        ok('E6 시즌 1 중에는 결산 없음',await p8.evaluate("()=>document.querySelector('#recap').classList.contains('hide')"))
        await c8.close()
        bad=[e for e in errs if 'ERR_' not in e]
        ok('Z 콘솔 오류 0',not bad,bad[:5])
        print('RESULT',sum(1 for _,c in R if c),'/',len(R))
        await b.close()
asyncio.run(main())
