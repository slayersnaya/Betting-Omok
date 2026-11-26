# 단계별 묘수 풀이 시험: 화면 흐름(목록·지도·문제·오답 풀이·정답·다시 풀기)·옥돌 지급·지갑 반영 간격·20번째 큰 보상·다음 단계 열림
#  ·규칙 거부(한 번에 두 칸·금액 위조·잠긴 단계·10초 안·다른 종류로 sp 바꾸기·줄이기·21번째·처음 만들 때 sp)·관리자 간격 예외·다른 기기에서 이어 하기·게스트·오늘의 묘수 풀이 그대로
# 사용: WEBDIR=/home/claude/eval/stage/web FPORT=9711 python3 stgtest.py
import asyncio, os, json, time
os.environ.setdefault('WEBDIR','/home/claude/eval/stage/web');os.environ.setdefault('FPORT','9711')
exec(open('/home/claude/eval/stage/tests/friendtest.py').read().split('# ===== 친구 기능 시나리오')[0])
RES=[]
def chk(name,ok,info=''):
    RES.append((name,bool(ok)));print(('PASS ' if ok else 'FAIL ')+name+(' | '+str(info)[:240] if info else ''),flush=True)
async def ev(p,c): return await p.evaluate("c=>window.__T.ev(c)",c)
async def push(path,d):
    STORE[path]=d
    for p in PAGES: await send(p,json.dumps({'t':'w','op':'set','p':path,'d':d}))
async def reload_w(p):
    await p.evaluate("()=>window.__T.ev(`(async()=>{const x=await db.doc('wal/'+SEAT).get();ECO.w=ecoNorm(x.data());ecoPaint()})()`)");await asyncio.sleep(0.4)
# 지갑 직접 쓰기(위조 시도). 서버 시각 표시는 앱과 같은 SRV_TS
async def forge(p,js):
    return await p.evaluate("""js=>new Promise(res=>{const T=window.__T,w=T.ev('ECO.w');const n=JSON.parse(JSON.stringify(w));const t=Math.floor((Date.now()+324e5)/864e5);if(n.d!==t){n.d=t;n.dc=0;n.dq=[]}
      try{(new Function('n',js))(n)}catch(e){return res('js '+e.message)}T.ev('db').doc('wal/'+T.ev('SEAT')).set(Object.assign({},n,{at:T.ev('SRV_TS')})).then(()=>{T.ev('ECO.w=ecoNorm('+JSON.stringify(n)+')');res('ok')},e=>res('denied'))})""",js)
async def body(p): return await p.evaluate("()=>(document.querySelector('#stgBody')?.innerText||'').replace(/\\s+/g,' ')")
async def old(u,sec=30):
    w=dict(STORE['wal/'+u]);w['at']=int(time.time()*1000)-sec*1000;await push('wal/'+u,w)
    for q in PAGES:
        try: await q.evaluate("()=>window.__T.ev('ECO.lastW=0')")
        except Exception: pass
# 정답을 화면 버튼(+5·+1·−)으로 넣고 제출
async def enter(p,bet):
    cur=await ev(p,'STG.bet.slice()')
    for j in range(3):
        d=bet[j]-cur[j]
        while d>=5: await p.click(f'#stgBody [data-act=stgb][data-i="{j}"][data-v="5"]');d-=5
        while d>0: await p.click(f'#stgBody [data-act=stgb][data-i="{j}"][data-v="1"]');d-=1
        while d<0: await p.click(f'#stgBody [data-act=stgb][data-i="{j}"][data-v="-1"]');d+=1
    await p.click('#stgBody [data-act=stggo]');await asyncio.sleep(0.4)
async def main():
    errs=[]
    async with async_playwright() as pw:
        b=await pw.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
        p=await newpage(b,errs,'성민');await asyncio.sleep(3)
        u=await ev(p,'SEAT');chk('규칙 흉내 켜짐(stage 규칙)',await ev(p,'1')==1 and await p.evaluate("()=>typeof window.__stgRulesOn==='function'&&window.__stgRulesOn()"))
        t=await p.evaluate("()=>document.querySelector('#stgTile')?.innerText.replace(/\\s+/g,' ')");chk('홈 타일: 단계별 묘수 풀이 · Easy 0 / 20','단계별 묘수 풀이' in t and 'Easy 0 / 20' in t,t)
        pz=await p.evaluate("()=>!!document.querySelector('#pzTile')");chk('오늘의 묘수 풀이 타일 그대로',pz)
        await p.click('#stgTile');await asyncio.sleep(0.5)
        chk('시트 열림 · 제목',await ev(p,'shOpen')=='stg' and (await p.inner_text('#stgT'))=='단계별 묘수 풀이')
        bt=await body(p);chk('목록: 네 단계 · 보상 안내 · 잠금 안내',all(x in bt for x in ['Easy','Normal','Hard','Godlike','문제당 5 · 20번째 50','Easy 10문제 깨면 열려요']),bt)
        lk=await p.get_attribute('[data-act=stgmap][data-s="1"]','aria-disabled');chk('Normal 잠김(aria-disabled)',lk=='true')
        await p.click('[data-act=stgmap][data-s="1"]',force=True);await asyncio.sleep(0.3);chk('잠긴 단계 누르면 그대로 목록',await ev(p,'STG.v')=='list')
        await p.click('[data-act=stgmap][data-s="0"]');await asyncio.sleep(0.3)
        chk('지도: 20칸 · 1번만 지금',await p.locator('#stgBody .stgq').count()==20 and await p.locator('#stgBody .stgq.cur').count()==1 and await p.locator('#stgBody .stgq.lock').count()==19)
        await p.click('#stgBody .stgq[data-i="3"]',force=True);await asyncio.sleep(0.2);chk('잠긴 문제는 안 열림',await ev(p,'STG.v')=='map')
        await p.click('#stgBody .btn.wide');await asyncio.sleep(0.3);chk('1번 열림 · 제목 Easy 1',(await p.inner_text('#stgT'))=='Easy 1')
        await p.click('#stgBody [data-act=stggo]');await asyncio.sleep(0.4);bt=await body(p)
        chk('오답(1·1·1): 아쉬워요 + 상대가 뚫는 방법','아쉬워요' in bt and '걸면' in bt and '상대 돌' in bt,bt[:200])
        w=STORE.get('wal/'+u,{});chk('오답은 지갑 안 바뀜',w.get('g',0)==0 and 'sp' not in w,w)
        ex=await ev(p,'stgPz(0,0).ex');best=await ev(p,'stgPz(0,0).best')
        # 확실하지만 최소가 아님(한 칸 +1)
        more=list(ex);more[0]+=1;await enter(p,more);bt=await body(p);chk('확실하지만 더 큼: 더 적은 합 안내','더 적은 합' in bt,bt[:160])
        await enter(p,ex);bt=await body(p);chk('정답 · 옥돌 +5 · 설명','정답' in bt and '옥돌 +5' in bt and '모두 막힘' in bt and f'합 {best-1}칩 이하는' in bt,bt[:260])
        await waitfor(lambda:asyncio.sleep(0,STORE.get('wal/'+u,{}).get('sp')==[1,0,0,0]),160);w=STORE.get('wal/'+u,{});chk('지갑 반영(새 지갑은 만든 뒤 10초 지나서): sp [1,0,0,0] · 옥돌 5',w.get('sp')==[1,0,0,0] and w.get('g')==5,w)
        loc=await p.evaluate("u=>localStorage.getItem('bo-stg:'+u)",u);chk('이 기기 기록',loc=='[1,0,0,0]',loc)
        # 바로 다음 문제: 이 기기에서는 바로 열리고, 지갑은 10초 간격 뒤 반영
        await p.click('#stgBody [data-act=stgpz][data-i="1"]');await asyncio.sleep(0.3);ex=await ev(p,'stgPz(0,1).ex');await enter(p,ex)
        await asyncio.sleep(2);w=STORE.get('wal/'+u,{});chk('10초 안: 지갑은 아직 1(간격 지킴)',w.get('sp')==[1,0,0,0],w.get('sp'))
        dn=await p.evaluate("()=>window.__stgDeny.length");chk('간격 기다림(규칙 거부 없이)',dn==0,dn)
        await p.click('#stgBody [data-act=stgmap]');await asyncio.sleep(0.2);await p.click('#stgBk');await asyncio.sleep(0.2);bt=await body(p);chk('목록: 반영 중 안내','옥돌 반영 중' in bt,bt[-60:])
        for _ in range(30):
            await asyncio.sleep(0.5)
            if STORE.get('wal/'+u,{}).get('sp')==[2,0,0,0]: break
        w=STORE.get('wal/'+u,{});chk('10초 뒤 반영: sp 2 · 옥돌 10',w.get('sp')==[2,0,0,0] and w.get('g')==10,w)
        await asyncio.sleep(0.6);bt=await body(p);chk('반영 끝나면 안내 사라짐','옥돌 반영 중' not in bt)
        # 다시 풀기: 보상 없음
        await p.click('[data-act=stgmap][data-s="0"]');await asyncio.sleep(0.2);await p.click('#stgBody .stgq[data-i="0"]');await asyncio.sleep(0.2)
        bt=await body(p);chk('푼 문제: 보상 받음 표시','보상 받음' in bt,bt[:80])
        await enter(p,await ev(p,'stgPz(0,0).ex'));bt=await body(p);chk('다시 풀기 정답: 이미 받은 문제','이미 받은 문제' in bt,bt[:120])
        await asyncio.sleep(1);chk('다시 풀기는 옥돌 그대로',STORE['wal/'+u].get('g')==10)
        # ----- 규칙 거부 -----
        await old(u);await reload_w(p)
        r=await forge(p,"n.sp=[(n.sp||[0,0,0,0])[0]+2,0,0,0];n.g+=10;n.k='stg'");chk('규칙: 한 번에 두 문제 거부',r=='denied',r)
        r=await forge(p,"n.sp=[3,0,0,0];n.g+=6;n.k='stg'");chk('규칙: 옥돌 금액 위조 거부',r=='denied',r)
        r=await forge(p,"n.sp=[2,1,0,0];n.g+=10;n.k='stg'");chk('규칙: 잠긴 단계(Easy 10 미만) 거부',r=='denied',r)
        r=await forge(p,"n.sp=[3,0,0,0];n.g+=10;n.k='earn';n.dc=(n.dc||0)+10");chk('규칙: 다른 종류(earn)로 sp 바꾸기 거부',r=='denied',r)
        r=await forge(p,"n.sp=[1,0,0,0];n.k='equip'");chk('규칙: 줄이기 거부',r=='denied',r)
        r=await forge(p,"delete n.sp;n.k='equip'");chk('규칙: sp 지우기 거부',r=='denied',r)
        r=await forge(p,"n.sp=[3,0,0,0];n.g+=5;n.k='stg'");chk('규칙: 정상 한 칸(+5) 허용',r=='ok',r)
        r=await forge(p,"n.sp=[4,0,0,0];n.g+=5;n.k='stg'");chk('규칙: 10초 안 다음 칸 거부',r=='denied',r)
        r=await forge(p,"n.k='equip'");chk('규칙: sp 그대로인 다른 쓰기 허용',r=='ok',r)
        await old(u);await reload_w(p)
        r=await forge(p,"n.sp=[4,0,0,0];n.g+=5;n.k='stg';n.own=n.own.concat(['t1'])");chk('규칙: stg에 꾸미기 끼우기 거부',r=='denied',r)
        w=dict(STORE['wal/'+u]);w.update({'sp':[20,9,0,0]});await push('wal/'+u,w);await old(u);await reload_w(p)
        r=await forge(p,"n.sp=[21,9,0,0];n.g+=5;n.k='stg'");chk('규칙: 21번째 거부',r=='denied',r)
        r=await forge(p,"n.sp=[20,9,1,0];n.g+=20;n.k='stg'");chk('규칙: Normal 9일 때 Hard 거부',r=='denied',r)
        r=await forge(p,"n.sp=[20,10,0,0];n.g+=10;n.k='stg'");chk('규칙: Normal 10번째 +10 허용',r=='ok',r)
        await old(u);await reload_w(p)
        r=await forge(p,"n.sp=[20,10,1,0];n.g+=20;n.k='stg'");chk('규칙: Normal 10이면 Hard 1번 +20 허용',r=='ok',r)
        sd=await p.evaluate("()=>window.__stgDeny.slice()");chk('거부 이유 기록(단계·금액·잠금·간격·종류)',all(any(k in x for x in sd) for k in ['step','amount','lock','interval','sp changed']),sd)
        # ----- 20번째 큰 보상(화면) -----
        w=dict(STORE['wal/'+u]);w.update({'sp':[19,0,0,0],'g':100});await push('wal/'+u,w);await old(u);await reload_w(p)
        await p.evaluate("u=>localStorage.setItem('bo-stg:'+u,'[19,0,0,0]')",u)
        await ev(p,"stgGo('list')");await asyncio.sleep(0.2);await p.click('[data-act=stgmap][data-s="0"]');await asyncio.sleep(0.2)
        chk('지도: 20번이 지금 문제',await p.locator('#stgBody .stgq.cur[data-i="19"]').count()==1)
        await p.click('#stgBody .btn.wide');await asyncio.sleep(0.3);bt=await body(p);chk('20번째: 옥돌 50 표시','50' in bt[:60],bt[:60])
        await enter(p,await ev(p,'stgPz(0,19).ex'));bt=await body(p);chk('20번째 정답: Easy 완료 · 옥돌 +50','Easy 완료' in bt and '옥돌 +50' in bt,bt[:120])
        await asyncio.sleep(1.5);w=STORE['wal/'+u];chk('지갑: sp 20 · 옥돌 +50',w.get('sp')[0]==20 and w.get('g')==150,[w.get('sp'),w.get('g')])
        await p.click('#stgBody [data-act=stgmap]');await asyncio.sleep(0.2);bt=await body(p);chk('지도: Easy 완료 문구','Easy 완료' in bt)
        await p.click('#stgBk');await asyncio.sleep(0.2);lk=await p.get_attribute('[data-act=stgmap][data-s="1"]','aria-disabled');chk('목록: Normal 열림',lk is None)
        bt=await body(p);chk('목록: Easy 완료 표시','완료' in bt)
        # 10번째에 다음 단계 열림 안내
        w=dict(STORE['wal/'+u]);w.update({'sp':[20,9,0,0]});await push('wal/'+u,w);await old(u);await reload_w(p);await p.evaluate("u=>localStorage.setItem('bo-stg:'+u,'[20,9,0,0]')",u)
        await ev(p,"stgGo('map',1)");await p.click('#stgBody .btn.wide');await asyncio.sleep(0.2);await enter(p,await ev(p,'stgPz(1,9).ex'))
        bt=await body(p);chk('Normal 10번째 정답: Hard 열림 안내','Hard 열림' in bt and '옥돌 +10' in bt,bt[:120])
        await asyncio.sleep(1.5);chk('지갑: Normal 10',STORE['wal/'+u].get('sp')[1]==10,STORE['wal/'+u].get('sp'))
        t=await p.evaluate("()=>document.querySelector('#stgTile .tsub').textContent");chk('홈 타일: 지금 단계 Normal 10 / 20',t=='Normal 10 / 20',t)
        # 보상 탭 '보상 기준' 한 줄
        await ev(p,"closeSheet()");await p.locator('.tabbar [data-k=rwd]:visible').first.click();await asyncio.sleep(0.5)
        rt=await p.evaluate("()=>document.querySelector('#rwdBody .rwinfo')?.textContent.replace(/\\s+/g,' ')");chk('보상 탭 보상 기준에 단계별 묘수 풀이','단계별 묘수 풀이' in rt and '5 · 10 · 20 · 30' in rt and '50 · 100 · 250 · 600' in rt,rt[-120:])
        await p.locator('.tabbar [data-k=home]:visible').first.click();await asyncio.sleep(0.3)
        # ----- 다른 기기(같은 계정): 서버 진행을 이어 받음 -----
        ctx2=await b.new_context(viewport={'width':1280,'height':800})
        await ctx2.add_init_script(f"sessionStorage.setItem('fake-g','1');sessionStorage.setItem('fake-uid','{u}');localStorage.setItem('bo-nick','성민');localStorage.setItem('bo-tut-done','1');localStorage.setItem('bo-rkintro','1');localStorage.setItem('bo-rklg','1');sessionStorage.setItem('bo-noatt','1')")
        async def route(rt): await rt.fulfill(path=FAKE[rt.request.url.split('/')[-1]],content_type='application/javascript')
        await ctx2.route('https://www.gstatic.com/**',route);p2=await ctx2.new_page();p2.on('pageerror',lambda e:errs.append('p2:'+str(e)));p2.on('console',lambda m:errs.append('p2 console:'+m.text) if m.type=='error' else None)
        await p2.expose_function('__fsSend',lambda j,p=p2:asyncio.ensure_future(relay(p,j)));PAGES.append(p2);await p2.goto(f'http://127.0.0.1:{PORT}/index.html');await asyncio.sleep(4)
        u2=await ev(p2,'SEAT');t=await p2.evaluate("()=>document.querySelector('#stgTile .tsub')?.textContent");chk('다른 기기: 같은 계정 진행 이어 받음',u2==u and t=='Normal 10 / 20',[u2==u,t])
        # ----- 게스트(구글 연결 없음): 같은 방식(지갑)으로 지급 -----
        g=await newpage(b,errs,'손님',google=False);await asyncio.sleep(3);gu=await ev(g,'SEAT')
        await ev(g,"stgOpenSheet()");await asyncio.sleep(0.2);await ev(g,"stgGo('pz',0,0)");await enter(g,await ev(g,'stgPz(0,0).ex'))
        await waitfor(lambda:asyncio.sleep(0,STORE.get('wal/'+gu,{}).get('sp')==[1,0,0,0]),160);gw=STORE.get('wal/'+gu,{});chk('게스트: 지갑에 옥돌 5 · sp 1(출석 등과 같은 방식)',gw.get('g')==5 and gw.get('sp')==[1,0,0,0],gw)
        # ----- 관리자: 규칙 간격 예외 -----
        await p.evaluate("()=>{window.__fakeAdmin=true}")
        w=dict(STORE['wal/'+u]);w.update({'sp':[20,10,0,0],'at':int(time.time()*1000)});await push('wal/'+u,w);await reload_w(p)
        r=await forge(p,"n.sp=[20,10,1,0];n.g+=20;n.k='stg'");chk('관리자: 10초 간격 예외',r=='ok',r)
        r=await forge(p,"n.sp=[20,10,2,0];n.g+=99;n.k='stg'");chk('관리자도 금액 위조는 거부',r=='denied',r)
        await p.evaluate("()=>{window.__fakeAdmin=false}")
        # 오늘의 묘수 풀이 그대로 열림
        await ev(p,"closeSheet()");await p.click('#pzTile');await asyncio.sleep(0.4);chk('오늘의 묘수 풀이 시트 그대로',await ev(p,'shOpen')=='puz' and len(await p.inner_text('#pzBody'))>10)
        # 모든 문제가 화면 함수로 풀리는지(정답 예시 통과·합-1은 뚫림 예시 있음·설명 그림)
        r=await ev(p,"(()=>{let bad=[];for(let s=0;s<4;s++)for(let i=0;i<20;i++){const z=stgPz(s,i);if(!z||!pzJudge(z,z.ex)){bad.push(s+':'+i+' judge');continue}if(stgBreak(z,z.ex))bad.push(s+':'+i+' break');const lo=z.ex.slice();const k=lo.indexOf(Math.max(...lo));lo[k]--;if(lo[k]>=1&&!stgBreak(z,lo))bad.push(s+':'+i+' lo');const h=stgExplain(z);if(!/모두 막힘/.test(h))bad.push(s+':'+i+' ex')}return bad})()")
        chk('화면 함수로 80문제: 정답 통과·하나 줄이면 뚫림 예시·설명',r==[],r)
        e2=[e for e in errs if 'ERR_TUNNEL' not in e and 'ERR_' not in e];chk('페이지·콘솔 오류 0',not e2,e2)
        print('RESULT',sum(1 for _,o in RES if o),'/',len(RES));await b.close()
asyncio.run(main())
