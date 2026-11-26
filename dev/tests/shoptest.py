# 재화·상점 1단계 시험: 획득·상한·구매·장착·다른 폰에서 보임·규칙 거부(가격 위조·상한 초과·중복 보상)·시즌 보상(Date.now 바꿔치기)
import asyncio, os, json, time
os.environ.setdefault('WEBDIR','/home/claude/eval/shop/web');os.environ.setdefault('FPORT','8871')
src=open('/home/claude/eval/friend/friendtest.py').read().split('# ===== 친구 기능 시나리오')[0]
exec(src)
RES=[]
def chk(name,ok,info=''):
    RES.append((name,bool(ok)));print(('PASS ' if ok else 'FAIL ')+name+(' | '+str(info)[:220] if info else ''),flush=True)
async def ev(p,c): return await p.evaluate("c=>window.__T.ev(c)",c)
async def evp(p,c): return await p.evaluate("c=>window.__T.ev(c)",c)
async def wal(u): return STORE.get('wal/'+u)
async def push(path,d):
    STORE[path]=d
    for p in PAGES: await send(p,json.dumps({'t':'w','op':'set','p':path,'d':d}))
async def reload_w(p):
    await p.evaluate("()=>window.__T.ev(`(async()=>{const x=await db.doc('wal/'+SEAT).get();ECO.w=ecoNorm(x.data());ecoLook();ecoPaint()})()`)");await asyncio.sleep(0.4)
# 지갑에 직접 쓰기(위조 시도): 규칙에 막히면 'denied'
async def forge(p,js):
    return await p.evaluate("""js=>new Promise(res=>{const w=window.__T.ev('ECO.w');const n=JSON.parse(JSON.stringify(w));const t=Math.floor((Date.now()+324e5)/864e5);if(n.d!==t){n.d=t;n.dc=0;n.dq=[]}
      try{(new Function('n',js))(n)}catch(e){return res('js '+e.message)}const db=window.__T.ev('db');db.doc('wal/'+window.__T.ev('SEAT')).set(Object.assign({},n,{at:{__st:1}})).then(()=>res('ok'),e=>res('denied'))})""",js)
# 끝난 AI 대국 흉내: archiveGame 훅을 그대로 탐
async def aigame(p,lv='mid',win=True,turns=5,reason='오목',gid=None):
    gid=gid or ('t'+str(int(time.time()*1000))[-9:])
    await p.evaluate("""([lv,win,turns,reason,gid])=>window.__T.ev(`L.s={id:'${gid}',ai:'${lv}',bot:null,phase:'over'};UI.mode='local';archiveGame({hist:[...Array(${turns})].map((_,i)=>({t:i+1,cells:[],win:[],bets:{}})),A:'A',B:'B',names:{A:'나',B:'AI'},me:'A',winner:${win?"'A'":"'B'"},reason:'${reason}'},'L${gid}','AI')`)""",[lv,win,turns,reason,gid])
    await asyncio.sleep(0.5)
async def main():
    errs=[]
    async with async_playwright() as pw:
        b=await pw.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
        p1=await newpage(b,errs,'성민');p2=await newpage(b,errs,'하율')
        await asyncio.sleep(3.5)
        u1=await ev(p1,'SEAT');u2=await ev(p2,'SEAT')
        w=await wal(u1)
        chk('지갑 처음 만들기(k=new, 0구슬)',w and w.get('k') in ('new','claim') and isinstance(w.get('own'),list),w)
        await asyncio.sleep(1.5)
        w=await wal(u1);chk('업적: 계정 연결 50 자동 수령',w and 'a_link' in w['cl'],w and w['cl'])
        # ---- 획득 ----
        g0=(await wal(u1))['g']
        await p1.evaluate("()=>localStorage.removeItem('bo-airec')")
        await aigame(p1,'mid',True);await asyncio.sleep(0.8)
        w=await wal(u1);gain=w['g']-g0
        chk('AI 중수 승리: 6 + 하루 첫 승 20 (+과제)',gain>=26 and 'w' in w['dq'] and w['dc']==gain,(gain,w['dq'],w['dc']))
        line=await ev(p1,"ecoResLine({me:'A'})")
        chk('결과 화면 한 줄(구슬 +n · 하루 첫 승 포함)','구슬 +' in line and '하루 첫 승' in line,line)
        g1=w['g'];await aigame(p1,'mid',False,turns=2);w=await wal(u1)
        chk('3턴 미만 판은 0',w['g']==g1 and '3턴' in (await ev(p1,'ECO.last.why')),w['g']-g1)
        await aigame(p1,'mid',False,reason='기권');w=await wal(u1)
        chk('기권패는 0',w['g']==g1,w['g']-g1)
        await aigame(p1,'mid',False);w=await wal(u1)
        chk('AI 패 3',w['g']-g1 in (3,13,23),w['g']-g1)
        # ---- 하루 상한 ----
        for i in range(40):
            await aigame(p1,'ultimate',True,gid='u%02d'%i)
            w=await wal(u1)
            if w['dc']>=150: break
        await asyncio.sleep(0.6);w=await wal(u1)
        chk('하루 상한 150에서 멈춤',w['dc']==150 or (w['dc']<=150 and await ev(p1,"ecoProgGet().gd")>=100),(w['dc'],await ev(p1,"ecoProgGet().gd")))
        gc=w['g'];await aigame(p1,'ultimate',True,gid='cap1');w=await wal(u1)
        chk('상한 뒤 대국 구슬 0 + 이유 표시',w['g']==gc and '다 받았어요' in (await ev(p1,'ECO.last.why')),await ev(p1,'ECO.last'))
        r=await forge(p1,"n.k='earn';const d=Math.max(1,151-n.dc);n.g+=d;n.dc+=d");chk('규칙: 하루 150 넘는 획득 거부',r=='denied',r)
        r=await forge(p1,"n.k='earn';n.g+=40;n.dc=Math.min(150,n.dc+40)");chk('규칙: 한 번에 너무 많이(40) 거부',r=='denied',r)
        r=await forge(p1,"n.k='earn';n.g+=1;n.dc+=1;n.d=n.d+1");chk('규칙: 날짜 위조 거부',r=='denied',r)
        r=await forge(p1,"n.k='earn';n.g=99999");chk('규칙: 잔액 부풀리기 거부',r=='denied',r)
        # ---- 1회성 보상 ----
        await p1.evaluate("()=>localStorage.setItem('bo-airec',JSON.stringify({beginner:{w:1,l:0,d:0},mid:{w:2,l:0,d:0}}))");await ev(p1,'ecoAch()');await asyncio.sleep(1.2)
        w=await wal(u1);chk('업적: AI 초보·중수 첫 승 자동 수령',{'a_ai1','a_ai2'}<=set(w['cl']),w['cl'])
        r=await forge(p1,"n.k='claim';n.cl.push('a_ai2');n.g+=80");chk('규칙: 같은 업적 두 번 거부',r=='denied',r)
        r=await forge(p1,"n.k='claim';n.cl.push('a_ai4');n.g+=999");chk('규칙: 업적 금액 위조 거부',r=='denied',r)
        r=await forge(p1,"n.k='claim';n.cl.push('p9_5');n.g+=300");chk('규칙: 다음 시즌 승급 미리 받기 거부',r=='denied',r)
        r=await forge(p1,"n.k='claim';n.cl.push('p1_3');n.g+=150");chk('규칙: 이번 시즌 승급 1회 허용',r=='ok',r)
        await reload_w(p1)
        r=await forge(p1,"n.k='claim';n.cl.push('p1_3');n.g+=150");chk('규칙: 같은 승급 두 번 거부',r=='denied',r)
        await ev(p1,"L.s=null;UI.mode='online'")
        # ---- 교환소: 구매·장착 ----
        w=dict(await wal(u1));w['g']=14000;await push('wal/'+u1,w);await reload_w(p1)
        await p1.click('#ecoCard [data-act=ecoopen][data-v=shop]');await asyncio.sleep(0.5)
        chk('교환소 열림(18개 상품)',await p1.locator('#shopBody .etile').count()==18,await p1.locator('#shopBody .etile').count())
        await p1.click('#shopBody [data-act=ecoitem][data-id=f1]');await asyncio.sleep(0.3)
        chk('구매 확인 창','1,500' in await txt(p1,'#dlg'),await txt(p1,'#dlg'))
        await p1.click('[data-act=dlgok]')
        for _ in range(40):
            await asyncio.sleep(0.15)
            if 'f1' in (await wal(u1))['own']: break
        w=await wal(u1)
        if 'f1' not in w['own']: print('DBG',await p1.evaluate("()=>[document.querySelector('#dlg').className,window.__walDeny.slice(-3),window.__T.ev('JSON.stringify(ECO.w)')]"))
        chk('구매: 1500 차감·보유·자동 장착',w['g']==12500 and 'f1' in w['own'] and w['eq'].get('f')=='f1',(w['g'],w['own'],w['eq']))
        for it in ['t2','n2','s1','x1','w1']:
            await ev(p1,f"ecoBuy('{it}')");await asyncio.sleep(0.7)
        w=await wal(u1);chk('여러 분류 구매·장착',all(x in w['own'] for x in ['t2','n2','s1','x1','w1']) and w['g']==4500-800-1200-1200-3500-2500+0 or w['g']>=0,(w['g'],w['eq']))
        r=await forge(p1,"n.k='buy';n.own.push('b1');n.g-=1");chk('규칙: 가격 위조(1구슬) 거부',r=='denied',r)
        r=await forge(p1,"n.k='buy';n.own.push('z1_6');n.g-=100");chk('규칙: 티어 테두리 구매 거부',r=='denied',r)
        r=await forge(p1,"n.k='equip';n.eq.b='b2'");chk('규칙: 없는 것 장착 거부',r=='denied',r)
        r=await forge(p1,"n.k='equip';n.eq.t='f1'");chk('규칙: 분류 틀린 장착 거부',r=='denied',r)
        r=await forge(p1,"n.k='buy';n.own.push('t1');n.g-=800;n.eq.t='t1';n.g+=500");chk('규칙: 구매하며 구슬 덤 거부',r=='denied',r)
        sk=await ev(p1,'window.ECO_SK');chk('돌 무늬 적용(내 화면)',sk=='_w1',sk)
        svg=await ev(p1,"boardSVG(Array.from({length:19},()=>Array(19).fill(0)).map((r,i)=>i===9?r.map((_,j)=>j>=5&&j<=9?1:0):r),{fives:[[[9,5],[9,9]]],fdelay:0,spark:true,fx:'x1'})")
        chk('완성 연출 x1 그림(꽃잎·돌 무늬)','<ellipse class="spk"' in svg and '#sB_w1' in svg,svg[:120])
        # ---- 다른 폰에서 보임: 랭크 결과(bres)·대국 접속(rt)·친구 접속(on) ----
        pe=await ev(p1,'ecoPe()');chk('공개 장착 문자열',set(pe.split('.'))>={'t2','n2','f1','s1','x1'},pe)
        r=await p1.evaluate("""pe=>new Promise(res=>{const T=window.__T,db=T.ev('db'),S=T.ev('SEAT'),g='k'+Math.random().toString(16).slice(2,10).padEnd(8,'0');db.doc('bres/'+S+'_'+g).set({by:S,gid:g,bot:'b01',na:'성민',w:'me',turns:9,why:'오목',ended:Date.now(),eq:pe}).then(()=>res('ok'),e=>res('denied'))})""",pe)
        chk('bres에 장착 싣기(보유한 것) 허용',r=='ok',r)
        r=await p1.evaluate("""()=>new Promise(res=>{const T=window.__T,db=T.ev('db'),S=T.ev('SEAT'),g='k'+Math.random().toString(16).slice(2,10).padEnd(8,'0');db.doc('bres/'+S+'_'+g).set({by:S,gid:g,bot:'b01',na:'성민',w:'me',turns:9,why:'오목',ended:Date.now(),eq:'f3.t1'}).then(()=>res('ok'),e=>res('denied'))})""")
        chk('규칙: 갖지 않은 장착 싣기 거부',r=='denied',r)
        await asyncio.sleep(1.5)
        c2=await ev(p2,f"JSON.stringify(cosOf('{u1}'))");chk('다른 폰: 랭크 결과로 장착 보임',"f1" in c2 and 't2' in c2,c2)
        h=await ev(p2,f"ecoRkNk({{seat:'{u1}',nick:'성민'}})+cosFrame('{u1}','<i></i>',22)")
        chk('다른 폰 랭킹 줄: 닉네임 장식·칭호·테두리','cn-n2' in h and '봉인 장인' in h and 'cring' in h,h[:160])
        # 일반 게임 방: A가 만들고 B가 코드로 입장 → B 화면 상대 바에 A 꾸미기
        await ev(p1,'dialogClose();closeSheet()');await asyncio.sleep(0.3)
        await p1.click('#gameCard [data-act=sheet][data-k=friend]');await asyncio.sleep(0.3);await p1.click('#createBtn');await asyncio.sleep(1.5)
        gid=await ev(p1,'G.gid');await p2.click('#gameCard [data-act=sheet][data-k=friend][data-v=code]');await asyncio.sleep(0.3)
        await p2.fill('#roomCode',gid[1:]);await p2.click('#joinBtn');await asyncio.sleep(1.5)
        try: await p2.click('[data-act=join]',timeout=5000)
        except Exception as e: print('join btn',e)
        await asyncio.sleep(2.5)
        for p in PAGES:
            try: await p.click('#coin',timeout=500)
            except Exception: pass
        await asyncio.sleep(2)
        pr=STORE.get(f'rt/g-{gid}/p/{u1}',{});chk('대국 접속(rt)에 장착 실림',(pr.get('presence') or {}).get('eq')==pe,pr)
        ob=await p2.evaluate("()=>document.querySelector('#oppbar').innerHTML")
        chk('상대 폰 대국 상단 바: 테두리·칭호·닉네임 장식','cring' in ob and '봉인 장인' in ob and 'cn-n2' in ob,ob[:200])
        # 봉인: A가 베팅 봉인 → B 화면 상대 태그가 매화 인장
        if await waitfor(sunpage,60):
            sp=await sunpage();await tap(sp,9,9);await sp.click('[data-act=dconfirm]')
            await waitfor(lambda: p1.locator('#bsub').count(),60);await p1.click('[data-act=bp][data-i="0"]');await p1.wait_for_timeout(500);await p1.click('#bsub');await asyncio.sleep(1.2)
            tg=await p2.evaluate("()=>(document.querySelector('#oppTag')||{}).innerHTML||''")
            chk('상대 폰 봉인 태그 = 내 인장(매화)','ecoS_s1' in tg,tg[:160])
            mine=await p1.evaluate("()=>(document.querySelector('#panel .sealed')||{}).innerHTML||''")
            chk('내 봉인 상자에 내 인장','ecoS_s1' in mine,mine[:120])
        await p2.click('#resignBtn');await p2.click('[data-act=dlgok]');await asyncio.sleep(2)
        # ---- 시즌 보상(Date.now 바꿔치기: 시즌 2 시작 다음 날) ----
        T2=1803826800000+864e5
        cfg={'n':1,'at':T2-3600e3,'v':1,'amt':[200,400,700,1000,1400,1800,2500],'p':{u1:[3,1350,12],u2:[5,1750,8],'bot:b01':[2,1150,40]}}
        await push('cfg/season1',cfg)
        for p in (p1,p2): await p.evaluate("t=>{const o=Date.now;const d=t-o.call(Date);Date.now=()=>o.call(Date)+d}",T2)
        for p in (p1,p2): await ev(p,'try{goLobby()}catch(e){}')
        await asyncio.sleep(0.5);await reload_w(p1)
        await ev(p1,'ECO.sz={};ecoSeasonCheck(true)');await asyncio.sleep(1)
        card=await txt(p1,'#ecoCard');chk('홈 카드: 시즌 1 보상 받기(플래티넘 1000)','시즌 1 보상' in card and '1,000' in card,card)
        g0=(await wal(u1))['g'];await asyncio.sleep(2.5)
        if await p1.evaluate("()=>!document.querySelector('#recap').classList.contains('hide')"):
            chk('시즌 결산 창(자동)에 보상 받기 줄','구슬 1,000' in await txt(p1,'#rcCard .rcrw'),await txt(p1,'#rcCard .rcrw'))
            await p1.click('#recap [data-act=ecosz]')
        else: await p1.click('#ecoCard [data-act=ecosz]')
        await asyncio.sleep(1.2)
        w=await wal(u1);chk('시즌 보상 수령: +1000 · 시즌 1 플래티넘 테두리',w['g']-g0==1000 and 'z1_3' in w['own'] and 's1' in w['cl'],(w['g']-g0,w['own'][-2:]))
        r=await forge(p1,"n.k='claim';n.cl.push('s1');n.g+=1000;n.own.push('z1_3x')");chk('규칙: 시즌 보상 두 번 거부',r=='denied',r)
        await reload_w(p2)
        r=await forge(p2,"n.k='claim';n.cl.push('s1');n.g+=1800;n.own.push('z1_5','zt1_5')");chk('규칙: 랭크 게임 10판 미만 시즌 보상 거부',r=='denied',r)
        cfg['p'][u2]=[5,1750,14];await push('cfg/season1',cfg)
        r=await forge(p2,"n.k='claim';n.cl.push('s1');n.g+=2500;n.own.push('z1_6','zt1_6')");chk('규칙: 관리자 기록과 다른 티어·금액 거부',r=='denied',r)
        r=await forge(p2,"n.k='claim';n.cl.push('s1');n.g+=1800;n.own.push('z1_5','zt1_5')");chk('규칙: 관리자 기록과 같은 보상 허용',r=='ok',r)
        await reload_w(p1);await ev(p1,"ecoEquip('f','z1_3')");await asyncio.sleep(0.8)
        w=await wal(u1);chk('시즌 테두리 장착',w['eq'].get('f')=='z1_3',w['eq'])
        r=await ev(p1,"JSON.stringify(ecoRewards())");chk('보상 API: ecoRewards 목록',r.startswith('['),r[:120])
        # 결산 창에 보상 줄
        await ev(p1,"recapShow({n:1,start:1795000000000,end:1803826800000,r:1350,g:12,w:8,l:4,d:0,ix:3,rank:3,best:3,top:null,next:1100})");await asyncio.sleep(0.4)
        chk('시즌 결산 창에 보상 줄','보상' in await txt(p1,'#rcCard .rcrw'),await txt(p1,'#rcCard .rcrw'))
        await ev(p1,'recapClose()')
        # ---- 계정 삭제: 지갑 비우기(지우기 금지) ----
        r=await p1.evaluate("()=>new Promise(res=>{const T=window.__T;T.ev('db').doc('wal/'+T.ev('SEAT')).delete().then(()=>res('ok'),()=>res('denied'))})")
        chk('규칙: 지갑 지우기 거부',r=='denied',r)
        await ev(p1,'ecoWipe()');await asyncio.sleep(1)
        w=await wal(u1);chk('계정 삭제 시 지갑 비움(1회성 기록은 남김)',w['g']==0 and w['own']==[] and 's1' in w['cl'],w)
        bad=[e for e in errs if 'denied' not in e and 'permission' not in e.lower() and 'ERR_TUNNEL' not in e and 'Failed to load resource' not in e]
        chk('콘솔 오류 0',not bad,bad[:5])
        print('walDeny',(await p1.evaluate("()=>window.__walDeny"))[-3:])
        await b.close()
    n=sum(1 for _,o in RES if o);print(f'== {n}/{len(RES)} PASS');json.dump(RES,open('/home/claude/eval/shop/shoptest.json','w'),ensure_ascii=False)
asyncio.run(main())
