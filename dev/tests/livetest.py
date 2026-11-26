# AI 방·공개 랭크 관전 시험
#  ① AI 일반 방: 사람 방 없을 때만 보임·폰마다 같음·사람 방이 생기면 숨김·들어가면 일반 게임(랭크·AI 기록 영향 없음)·친구 상태/관전·한 판 더
#  ② AI끼리 랭크 게임: 목록·결과가 점수표와 일치·폰마다 같은 판·2턴 지연·끝 화면
#  ③ 공개 목록: 사람 대 AI(구글·게스트)·사람끼리(방장 색인, 상대 관전 끔이면 안 올림)·친구 아닌 사람·게스트 관전·관전 끄기·규칙 거부·쓰기 수
# 사용: WEBDIR=/home/claude/eval/live/web FPORT=9811 python3 livetest.py
import os;os.environ.setdefault('FPORT','9811')
exec(open('/home/claude/eval/live/tests/h.py').read())
UID={'성민':'uLiveSeongmin00001','하율':'uLiveHayul0000002','지수':'uLiveJisu00000003','손님':'uLiveGuest0000004','낯선':'uLiveStrange00005'}
def LB(u):
    h=str(int(time.time()*1000)//3600000);d=STORE.get('lvb/'+h,{}).get('p',{}) or {}
    return d.get(u)
def pidf(x,y): return x+'_'+y if x<y else y+'_'+x
def seed_friend(x,y,nx,ny):
    a,b=sorted([x,y]);na,nb=(nx,ny) if a==x else (ny,nx);now=int(time.time()*1000)
    STORE['fp/'+a+'_'+b]={'a':a,'b':b,'by':a,'st':'ok','at':now,'sa':now,'na':na,'nb':nb,'m':[],'q':0,'ra':0,'rb':0}
async def page(b,errs,name,vp=(390,844),google=True):
    ctx=await b.new_context(viewport={'width':vp[0],'height':vp[1]})
    await ctx.add_init_script(f"sessionStorage.setItem('fake-uid','{UID[name]}');"+("sessionStorage.setItem('fake-g','1');" if google else "")+f"localStorage.setItem('bo-nick','{name}');"
        "localStorage.setItem('bo-tut-done','1');localStorage.setItem('bo-rkintro','1');localStorage.setItem('bo-rklg','1');sessionStorage.setItem('bo-noatt','1');localStorage.setItem('bo-airec',JSON.stringify({pro:{w:1,l:0,d:0},mid:{w:1,l:0,d:0}}))")
    async def route(rt): await rt.fulfill(path=FAKE[rt.request.url.split('/')[-1]],content_type='application/javascript')
    await ctx.route('https://www.gstatic.com/**',route)
    p=await ctx.new_page();p.on('pageerror',lambda e:errs.append(name+':'+str(e)))
    p.on('console',lambda m:errs.append(name+' console:'+m.text) if m.type=='error' and 'ERR_TUNNEL' not in m.text and 'ERR_PROXY' not in m.text else None)
    await p.expose_function('__fsSend',lambda j,p=p:asyncio.ensure_future(relay(p,j)))
    PAGES.append(p);await p.goto(f'http://127.0.0.1:{PORT}/index.html')
    try: await p.click('[data-act=wskip]',timeout=1500)
    except Exception: pass
    return p
async def tab(p,k): await p.evaluate(f"()=>document.querySelector('.tabbar:not(.tbw) [data-k={k}]').click()");await asyncio.sleep(0.4)
async def frtxt(p,u): return await p.evaluate(f"()=>(document.querySelector('#palFr [data-u=\"{u}\"]')?.closest('.frow')?.innerText||'').replace(/\\s+/g,' ')")
async def try_read(p,path,coll=False):
    m='collection' if coll else 'doc'
    return await ev(p,f"(async()=>{{try{{await db.{m}('{path}').get();return 'ok'}}catch(e){{return 'denied'}}}})()")
async def try_write(p,path,data):
    return await ev(p,f"(async()=>{{try{{await db.doc('{path}').set({data});return 'ok'}}catch(e){{return 'denied'}}}})()")
SPOTS=[(1,2),(1,9),(1,16),(5,2),(5,9),(5,16),(9,2),(9,16),(13,2),(13,9),(13,16),(17,2),(17,9),(17,16)]
async def local_turn(p,k):
    t0=await ev(p,"L.s.hist.length")
    for _ in range(300):
        s=json.loads(await ev(p,"JSON.stringify({ph:L.s.phase,sun:L.s.sun,st:L.s.stage,h:L.s.hist.length})"))
        if s['h']>t0 or s['ph']=='over': return 'ok'
        try: await p.click('#coin',timeout=200)
        except Exception: pass
        if s['ph']=='designate' and s['sun']=='A' and await p.locator('[data-act=dconfirm]').count():
            if not await ev(p,"!!(UI.sel&&UI.sel.cells)"):
                r,c=SPOTS[(k+_//10)%len(SPOTS)];await tap(p,r,c);await asyncio.sleep(0.3)
            try: await p.click('[data-act=dconfirm]',timeout=800)
            except Exception: pass
        elif s['ph']=='bet' and s['st']!=4 and await p.locator('#bsub').count():
            try: await p.click('[data-act=bp][data-i="0"]',timeout=500);await ev(p,"(()=>{const t=L.s.pts.A,q=Math.max(1,Math.floor(t*0.3));UI.bet=[q,q,q];return 0})()");await p.wait_for_timeout(700);await p.click('#bsub',timeout=800)
            except Exception: pass
        await asyncio.sleep(0.3)
    return 'timeout'
async def golobby(p):
    await ev(p,"(UI.mode==='online'?leaveRoom():goLobby(),0)");await asyncio.sleep(0.6)
async def main():
    errs=[]
    async with async_playwright() as pw:
        b=await pw.chromium.launch()
        A,B,C,Gs,D=UID['성민'],UID['하율'],UID['지수'],UID['손님'],UID['낯선']
        seed_friend(A,B,'성민','하율')
        p1=await page(b,errs,'성민');p2=await page(b,errs,'하율');p3=await page(b,errs,'지수',(360,740));pg=await page(b,errs,'손님',google=False);p5=await page(b,errs,'낯선')
        await asyncio.sleep(3)
        chk('가짜 서버에 공개 관전 규칙 켜짐',await p1.evaluate("()=>window.__pubRulesOn&&window.__pubRulesOn()"))
        chk('공개 문구: 규칙 전문에만 한 번',await p1.evaluate("()=>{const h=document.body.innerHTML;const n=[...document.querySelectorAll('li,p,span,div')].filter(e=>e.children.length<=1&&e.textContent.split(String.fromCharCode(10)).join(' ').replace(/  +/g,' ').trim()==='일반 게임 방과 랭크 게임에 AI가 함께할 수 있어요.').length;return n===1&&document.querySelector('#tab-rule .rfull').textContent.includes('AI가 함께할 수 있어요')}"))
        # ===== ① AI 일반 방 =====
        ok=await waitfor(lambda: ev(p1,"fkRooms(Date.now()).some(r=>r.status==='open')"),1500)
        await asyncio.sleep(3.5)
        fk1=await ev(p1,"JSON.stringify(fkRooms(Date.now()).map(r=>[r.id,r.hostNick,r.status,r.td]))");fk5=await ev(p5,"JSON.stringify(fkRooms(Date.now()).map(r=>[r.id,r.hostNick,r.status,r.td]))")
        chk('AI 방: 지금 열린 방 있음',ok,fk1)
        chk('AI 방: 폰마다 같은 방(시각 씨앗)',fk1==fk5,(fk1,fk5))
        home=await txt(p1,'#roomsHome');hn=json.loads(fk1)[0][1] if json.loads(fk1) else '?'
        chk('로비 일반 게임 목록에 AI 방(방장 닉·참가 가능·입장)',hn in home and '참가 가능' in home and await p1.locator('#roomsHome [data-act=fkenter]').count()>=1,home)
        chk('AI 방 이름에 AI 티 없음',not any(w in home for w in ['AI','봇','bot']),home)
        st=await ev(p1,"(()=>{const c=[0,0,0];const t0=Date.now();for(let i=0;i<8640;i++){const o=fkRooms(t0+i*10e3).filter(x=>x.status==='open').length;c[Math.min(2,o)]++}return JSON.stringify(c.map(x=>Math.round(x/86.4)))})()")
        c=json.loads(st);chk('하루 동안 열린 AI 방 0개인 시간 15% 이하·2개 넘지 않음',c[0]<=15,st)
        nb=await ev(p1,"fkRooms(Date.now()).filter(r=>r.status==='open').map(r=>BOTMAP.get(r.fk.bot.id).k).every(k=>k<=2)")
        chk('AI 방 방장은 초보·중수·고수 AI',nb)
        # 사람이 방을 열면 AI 방 모두 숨김
        gid=await ev(p2,"(async()=>{await createRoomInner();return G.gid})()");await asyncio.sleep(2.5)
        home=await txt(p1,'#roomsHome')
        chk('사람 방이 열리면 AI 방은 모두 숨김',await p1.locator('#roomsHome [data-act=fkenter]').count()==0 and '하율' in home,home)
        await ev(p2,"(leaveRoom(),0)");await asyncio.sleep(3)
        ok=await waitfor(lambda: ev(p1,"document.querySelectorAll('#roomsHome [data-act=fkenter]').length>0||!fkRooms(Date.now()).some(r=>r.status==='open')"),80)
        chk('사람 방이 닫히면 AI 방 다시 보임',ok,await txt(p1,'#roomsHome'))
        # 들어가기
        ok=await waitfor(lambda: p1.evaluate("()=>document.querySelectorAll('#roomsHome [data-act=fkenter]').length>0"),1300)
        rk0=await ev(p1,"JSON.stringify([rkP(SEAT).g,rkP(SEAT).r])");ai0=await ev(p1,"localStorage.getItem('bo-airec')")
        fid=await p1.evaluate("()=>document.querySelector('#roomsHome [data-act=fkenter]').dataset.g")
        room=json.loads(await ev(p1,f"JSON.stringify(fkRooms(Date.now()).find(r=>r.id==='{fid}'))"))
        await p1.click(f'#roomsHome [data-act=fkenter][data-g="{fid}"]');await asyncio.sleep(1.5)
        s=json.loads(await ev(p1,"JSON.stringify({cas:!!L.s.cas,nick:L.s.bot&&L.s.bot.nick,td:L.s.td,tb:L.s.tb,ai:L.s.ai,ttl:document.querySelector('#gttl').textContent,mode:UI.mode,view:UI.view})"))
        chk('AI 방 입장 → 일반 게임(방장 닉·방 시간)',s['cas'] and s['nick']==room['hostNick'] and s['td']==room['td'] and s['tb']==room['tb'] and s['view']=='game',s)
        chk('AI 방 제목 "닉의 방"',s['ttl']==room['hostNick']+'의 방',s['ttl'])
        chk('AI 실력: 이긴 단계까지(Hard 이하)',s['ai'] in ('beginner','mid','pro'),s['ai'])
        await tab(p2,'pal')
        ok=await waitfor(lambda: p2.evaluate(f"()=>/일반 게임 중/.test(document.querySelector('#palFr [data-u=\"{A}\"]')?.closest('.frow')?.innerText||'')"),80)
        on=STORE.get('on/'+A,{})
        chk('친구 목록: "일반 게임 중"(AI 상대 티 없음)',ok and on.get('st')=='g' and on.get('gi')=='c',(await frtxt(p2,A),on))
        chk('친구 목록: 관전 버튼',await p2.evaluate(f"()=>!!document.querySelector('#palFr [data-act=frwatch][data-u=\"{A}\"]')"))
        await local_turn(p1,0)
        await p2.click(f'#palFr [data-act=frwatch][data-u="{A}"]')
        ok=await waitfor(lambda: ev(p2,"!!(G.watch&&G.watch.rl)"),80)
        await asyncio.sleep(1.5)
        lv=STORE.get('lv/'+A,{})
        chk('친구 관전: 중계 k "c"(실시간, AI 표시 없음)',ok and lv.get('k')=='c' and lv.get('nb')==room['hostNick'] and 'al' not in lv,lv)
        h1=await ev(p1,"L.s.hist.length");h2=await ev(p2,"vstate().hist.length")
        chk('친구 관전: 판 기록 같음(지연 없음)',h1==h2 and h1>=1,(h1,h2))
        chk('친구 관전 안내 "관전 중"',('관전 중' in await txt(p2,'#panel')),await txt(p2,'#panel'))
        await p2.click('[data-act=lobby]');await asyncio.sleep(0.8)
        # 나가기 → 이 판은 끝남(기권), 랭크·AI 기록 영향 없음
        await p1.click('[data-act=lobby]') if await p1.locator('#game [data-act=lobby]').count() else await ev(p1,"(document.querySelector('[data-act=leave]')||{click(){}}).click(),0")
        await asyncio.sleep(0.5)
        dl=await txt(p1,'#dlg')
        chk('AI 방 나가기 안내 "나가면 이 판은 끝나요"',('이 판은 끝나요' in dl),dl)
        try: await p1.click('[data-act=dlgok]',timeout=1500)
        except Exception: pass
        await asyncio.sleep(1)
        arch=await ev(p1,"JSON.stringify(archList()[0]&&archList()[0].label)")
        rk1=await ev(p1,"JSON.stringify([rkP(SEAT).g,rkP(SEAT).r])");ai1=await ev(p1,"localStorage.getItem('bo-airec')")
        chk('기록: "친구 대국 · 닉"',json.loads(arch)=='친구 대국 · '+room['hostNick'],arch)
        chk('랭크 점수·AI 대국 기록·서버 결과 영향 없음',rk0==rk1 and ai0==ai1 and not any(k.startswith('bres/') for k in STORE) and await ev(p1,"botQ().length")==0 and not await ev(p1,"localStorage.getItem('bo-bplay')"),(rk0,rk1,ai0,ai1))
        chk('같은 방은 이 폰 목록에서 숨김',await p1.locator(f'[data-act=fkenter][data-g="{fid}"]').count()==0)
        # 한 판 더
        await ev(p1,"(()=>{const b=FK_POOL[3];leaveGame();UI.mode='local';L.start(null,'mid',{bot:{id:b.id,nick:b.nick,r:1000},cas:{id:'fk0-1',td:20,tb:30}});show('game');$('#cover').classList.add('hide');renderAll();return 1})()");await asyncio.sleep(1)
        await ev(p1,"(L.resign(),renderAll(),0)");await asyncio.sleep(0.8)
        n0=await ev(p1,"L.s.bot&&L.s.bot.nick");id0=await ev(p1,"L.s.id")
        has=await p1.locator('#panel [data-act=fkagain]').count()
        await p1.screenshot(path='/home/claude/eval/live/shots/dbg_over.png')
        if has: await p1.click('#panel [data-act=fkagain]',timeout=5000)
        w=await txt(p1,'#panel')
        ok=await waitfor(lambda: ev(p1,f"L.s.id!=='{id0}'&&L.s.phase!=='over'"),80)
        chk('끝난 뒤 "한 판 더" → 상대 기다리는 중 → 같은 상대와 새 판',has and '기다리는' in w and ok and await ev(p1,"L.s.bot.nick")==n0 and await ev(p1,"!!L.s.cas"),(has,w))
        await ev(p1,"(L.resign(),0)");await golobby(p1)
        # ===== ② AI끼리 랭크 게임 =====
        for p in (p1,p3,p5): await tab(p,'rank')
        ok=await waitfor(lambda: ev(p3,"lxItems(Date.now()).some(x=>x.g)"),300)
        chk('랭크 탭 맨 위 "진행 중인 랭크 게임"(AI끼리 판 포함)',ok and await p3.evaluate("()=>{const c=document.querySelector('#lxCard');return !c.classList.contains('hide')&&c.previousElementSibling.id==='rkResume'}"),await txt(p3,'#lxCard'))
        chk('접힘: 처음엔 2줄 + 모두 보기',await p3.evaluate("()=>document.querySelectorAll('#lxList .lxrow').length")<=2,await txt(p3,'#lxCard'))
        await asyncio.sleep(10)
        res=json.loads(await ev(p3,"JSON.stringify([...BL.res.values()].filter(x=>x.S).map(x=>{const g=x.g,S=x.S,d=blSnap(g,S,g.t);const wn=d.w==='A'?d.na:d.nb;return{key:g.key,ok:wn===blNick(g.sa===1?g.a:g.b),sw:S.sw,T:S.r.H.length,ends:S.ln.ends[S.ln.ends.length-1]===g.t}}))"))
        chk('AI끼리 판: 끝난 화면의 승자 = 점수표 결과(모든 계산된 판)',len(res)>=3 and all(r['ok'] and r['ends'] for r in res),res[:6])
        sw=sum(1 for r in res if r['sw']);chk('이름 자리 바꿈은 일부만(실력대로 둔 판이 대부분)',sw<=len(res)*0.6,(sw,len(res)))
        rc=json.loads(await ev(p3,"(()=>{const out=[];for(const x of [...BL.res.values()].filter(x=>x.S).slice(0,4)){const g=x.g,SS=RK.season,LT=RK.lt;const a=rankCalc(SS,LT,RK.docs,RK.bdocs,null,g.t-1).M,b=rankCalc(SS,LT,RK.docs,RK.bdocs,null,g.t+1).M;const w=BOTPRE+(g.sa===1?g.a:g.b),l=BOTPRE+(g.sa===1?g.b:g.a);out.push([b.get(w).r-a.get(w).r,b.get(l).r-a.get(l).r,g.ra===a.get(BOTPRE+g.a).r])}return JSON.stringify(out)})()"))
        chk('점수표: 그 판 끝나는 시각에 승자 점수↑·패자 점수↓(같은 판)',len(rc)>=2 and all(x[0]>0 and x[1]<0 and x[2] for x in rc),rc)
        k3=await ev(p3,"JSON.stringify(BL.next.map(g=>g.key))");k5=await ev(p5,"JSON.stringify(BL.next.map(g=>g.key))")
        ks=[k for k in json.loads(k3) if k in json.loads(k5)]
        if ks:
            h3=await ev(p3,f"(async()=>{{const g=BL.next.find(x=>x.key==='{ks[0]}');const S=await blSim(g);return JSON.stringify(S.r.H)+S.sw}})()")
            h5=await ev(p5,f"(async()=>{{const g=BL.next.find(x=>x.key==='{ks[0]}');const S=await blSim(g);return JSON.stringify(S.r.H)+S.sw}})()")
        chk('다른 폰도 같은 AI끼리 판(일정·수·베팅)',len(ks)>=3 and h3==h5,(len(ks),len(json.loads(k3))))
        # 관전
        bk=await ev(p3,"(lxItems(Date.now()).find(x=>x.g)||{}).k")
        await ev(p3,"(LX.more=true,lxRender(),0)");await asyncio.sleep(0.3)
        await p3.click(f'[data-act=lxwatch][data-k="{bk}"]')
        ok=await waitfor(lambda: ev(p3,"!!(G.watch&&G.watch.rl)"),100)
        await asyncio.sleep(1.2)
        d=json.loads(await ev(p3,"JSON.stringify((()=>{const w=G.watch,S=w.S,now=Date.now();let done=0;while(done<S.r.H.length&&S.ln.ends[done]<=now)done++;return{done,h:vstate().hist.length,t:w.rl.t}})())"))
        pl=await txt(p3,'#panel')
        chk('AI끼리 판 관전: 2턴 늦게(지금 턴 표시)',ok and d['h']==max(0,d['done']-2) and d['t']==d['done']+1 and '2턴 늦게' in pl,(d,pl))
        chk('관전 화면: 턴마다 두 사람 칩',d['h']==0 or await p3.evaluate("()=>document.querySelectorAll('#panel .wbp').length")>=3,await txt(p3,'#panel'))
        await p3.screenshot(path='/home/claude/eval/live/shots/t_botwatch_360.png')
        # 끝 화면: 시각을 앞당겨 바로 끝나게 해서 승자 확인
        await ev(p3,"(()=>{const w=G.watch,g=w.bot;g.t=Date.now()+2500;w.S.ln=blLine(g,w.S.r);w.k2='';return 0})()")
        await asyncio.sleep(8)
        pl=await txt(p3,'#panel');d=json.loads(await ev(p3,"JSON.stringify({ph:vstate().phase,w:vstate().winner,na:G.meta.hostNick,nb:G.meta.guestNick,sw:G.watch.S.sw,exp:blNick(G.watch.bot.sa===1?G.watch.bot.a:G.watch.bot.b),n:vstate().hist.length,T:G.watch.S.r.H.length})"))
        chk('AI끼리 판 끝: 전체 공개·승자 이름 = 점수표 승자',d['ph']=='over' and d['n']==d['T'] and (d['na'] if d['w']=='A' else d['nb'])==d['exp'] and '랭크 게임' in pl,(d,pl))
        await p3.screenshot(path='/home/claude/eval/live/shots/t_botover_360.png')
        await p3.click('[data-act=lobby]');await asyncio.sleep(0.6)
        chk('AI끼리 판 관전은 서버 쓰기 0',not any(k.startswith('lv/') and k.endswith('/w/'+C) for k in STORE) and await p3.evaluate("()=>window.__lvwWrites||0")==0)
        # ===== ③ 공개 목록: 사람 대 AI(구글) =====
        await ev(p1,"(mmBot(),0)");await asyncio.sleep(2)
        x=LB(A) or {}
        chk('랭크 AI전 시작 → 공개 목록 칸 한 번 씀(지금 시간 문서)',x.get('na')=='성민' and x.get('nb')==await ev(p1,"L.s.bot.nick") and x.get('exp',0)>time.time()*1000+40*60e3 and await p1.evaluate("()=>window.__lxWrites")==1,x)
        chk('관전자 없으면 중계 안 씀(지난 중계 문서는 지움)',('lv/'+A) not in STORE,STORE.get('lv/'+A))
        await ev(p3,"(LX.at=0,lxLoad(true),0)");await asyncio.sleep(1)
        it=json.loads(await ev(p3,"JSON.stringify(lxItems(Date.now()).filter(x=>x.u).map(x=>[x.u,x.na,x.nb]))"))
        chk('친구 아닌 사람 목록에 성민의 랭크 게임(AI 상대 닉, 구분 없음)',[A,'성민',x.get('nb')] in it,it)
        chk('목록 읽기: 문서 1번',await p3.evaluate("()=>window.__lxReads")<=3,await p3.evaluate("()=>window.__lxReads"))
        await ev(p3,"(LX.more=true,lxRender(),0)");await asyncio.sleep(0.3)
        await p3.click(f'[data-act=lxwatch][data-k="u{A}"]')
        ok=await waitfor(lambda: ev(p3,"!!(G.watch&&G.watch.rl)"),100)
        chk('친구 아닌 사람 공개 관전 입장(관전자 표시 등록)',ok and ('lv/'+A+'/w/'+C) in STORE,await txt(p3,'#panel'))
        ok=await waitfor(lambda: p1.evaluate("()=>document.querySelector('#gmid .wcnt')?.getAttribute('aria-label')==='관전 1명'"),40)
        chk('두는 사람 화면 관전 1명(공개 관전자 포함)',ok,await txt(p1,'#gmid'))
        dl=[]
        for k in range(3):
            await local_turn(p1,k);await asyncio.sleep(2)
            if await ev(p1,"L.s.phase")=='over': break
            dl.append((await ev(p1,"L.s.hist.length"),await ev(p3,"vstate().hist.length")))
        lv=STORE.get('lv/'+A,{})
        chk('공개 관전 2턴 지연',len(dl)>=1 and all(h3==max(0,h1-2) for h1,h3 in dl),dl)
        chk('중계: 랭크(k r)·지금 턴 정보 없음',lv.get('k')=='r' and 'sun' not in lv and 'c' not in lv,lv)
        if await ev(p1,"L.s.phase")=='over':
            ok=await waitfor(lambda: ev(p3,"vstate()&&vstate().phase==='over'"),40)
            chk('끝난 판: 공개 관전 화면에 결과',ok,await txt(p3,'#panel'))
            await ev(p1,"(mmBot(),0)");await asyncio.sleep(2.5)
        # 게스트도 공개 관전
        await tab(pg,'rank');await ev(pg,"(LX.at=0,lxLoad(true),0)");await asyncio.sleep(1)
        await ev(pg,f"(lxWatch('u{A}'),0)")
        ok=await waitfor(lambda: ev(pg,"!!(G.watch&&G.watch.rl)"),100)
        chk('게스트도 공개 관전',ok and ('lv/'+A+'/w/'+Gs) in STORE,await txt(pg,'#panel'))
        await pg.click('[data-act=lobby]');await asyncio.sleep(0.5)
        # 관전 끄기(설정 시트) → 색인 지움·새 관전 거부
        await ev(p1,"(openSheet('set'),0)");await asyncio.sleep(0.3)
        chk('설정 시트에 "관전 허용"(켜짐)',await p1.evaluate("()=>document.querySelector('#setSp').checked"))
        await p1.click('#setSp');await asyncio.sleep(2.5);await ev(p1,"(closeSheet(),0)")
        chk('관전 끄면 목록 칸 비움·중계 지움',LB(A) is None and ('lv/'+A) not in STORE and STORE.get('on/'+A,{}).get('sp')==False,STORE.get('on/'+A))
        chk('규칙: 관전 끈 뒤 친구 아닌 사람 lv 읽기 거부',await try_read(p5,'lv/'+A)=='denied')
        await p1.click('#mebar') if False else None
        await ev(p1,"(openSheet('set'),0)");await asyncio.sleep(0.3);await p1.click('#setSp');await asyncio.sleep(2.5);await ev(p1,"(closeSheet(),0)")
        chk('다시 켜면 진행 중인 판 다시 올림',LB(A) is not None)
        await p3.click('[data-act=lobby]');await asyncio.sleep(0.5)
        # 대국 화면을 나가면 색인 지움
        await ev(p1,"(L.resign(),0)");await asyncio.sleep(1.5);await golobby(p1);await asyncio.sleep(1.5)
        chk('판이 끝나고 나가면 목록 칸 비움',LB(A) is None,LB(A))
        # ===== 게스트 랭크 AI전 =====
        await ev(pg,"(mmBot(),0)");await asyncio.sleep(2)
        chk('게스트 랭크 게임도 목록에',(LB(Gs) or {}).get('na')=='손님',LB(Gs))
        await tab(p5,'rank');await ev(p5,"(LX.at=0,lxLoad(true),0)");await asyncio.sleep(1)
        await ev(p5,f"(lxWatch('u{Gs}'),0)")
        ok=await waitfor(lambda: ev(p5,"!!(G.watch&&G.watch.rl)"),100)
        await local_turn(pg,0);await local_turn(pg,1);await asyncio.sleep(2)
        chk('게스트 판 공개 관전(게스트가 랭크 중계 씀)',ok and STORE.get('lv/'+Gs,{}).get('k')=='r',(await txt(p5,'#panel'),STORE.get('lv/'+Gs)))
        chk('규칙: 게스트는 AI 대전 중계(k a) 못 씀',await try_write(pg,'lv/'+Gs,"{v:1,id:'abcdef12',k:'a',at:SRV_TS,na:'a',nb:'b',me:'A',t:1,ph:'bet',h:''}")=='denied')
        await p5.click('[data-act=lobby]');await asyncio.sleep(0.4)
        await ev(pg,"(L.resign(),0)");await asyncio.sleep(1);await golobby(pg)
        await ev(pg,"(lset('bo-sp','0'),mmBot(),0)");await asyncio.sleep(2.5)
        chk('게스트가 관전 끄면 목록에 안 올림',LB(Gs) is None)
        await ev(pg,"(L.resign(),lset('bo-sp','1'),0)");await asyncio.sleep(1);await golobby(pg)
        # ===== 사람끼리 랭크: 방장만 색인, 상대가 관전 끄면 안 올림 =====
        for p in (p1,p2): await golobby(p);await tab(p,'rank')
        await p1.click('#mmBtn');await asyncio.sleep(0.3);await p2.click('#mmBtn')
        ok=await waitfor(lambda: ev(p1,"!!(UI.mode==='online'&&G.meta&&G.meta.ranked&&G.st&&G.st.A&&G.docs[G.meta.guest])"),150)
        ok2=await waitfor(lambda: ev(p2,"!!(UI.mode==='online'&&G.meta&&G.meta.ranked)"),60)
        host=await ev(p1,"G.meta&&G.meta.host");hp,gp=(p1,p2) if host==A else (p2,p1);hu,gu=(A,B) if host==A else (B,A)
        await asyncio.sleep(3)
        chk('사람끼리 랭크: 방장만 목록에 올림',ok and ok2 and LB(hu) is not None and LB(gu) is None,STORE.get('lvb/'+str(int(time.time()*1000)//3600000)))
        # 손님이 관전을 끄면 방장이 색인을 지움
        await ev(gp,"(openSheet('set'),0)");await asyncio.sleep(0.3);await gp.click('#setSp');await asyncio.sleep(4);await ev(gp,"(closeSheet(),0)")
        ok=await waitfor(lambda: ev(hp,"(G.oppNp===true)"),60)
        await asyncio.sleep(2)
        chk('상대가 관전 끄면(presence np) 방장이 목록에서 내림',ok and LB(hu) is None,(await ev(hp,"G.oppNp"),LB(hu)))
        await ev(gp,"(openSheet('set'),0)");await asyncio.sleep(0.3);await gp.click('#setSp');await asyncio.sleep(1);await ev(gp,"(closeSheet(),0)")
        await gp.click('#resignBtn');await gp.click('[data-act=dlgok]');await asyncio.sleep(2)
        for p in (p1,p2): await golobby(p)
        # ===== 규칙 거부 =====
        now=int(time.time()*1000)
        H=str(now//3600000);E=lambda u,exp,extra='':f"{{p:{{'{u}':{{v:1,id:'abcdef12',na:'x',nb:'y',ra:1000,rb:1000,at:{now},exp:{exp}{extra}}}}}}}"
        chk('규칙: 목록에 남의 칸 쓰기 거부',await ev(p5,f"(async()=>{{try{{await db.doc('lvb/{H}').update({E(A,now+600000)});return 'ok'}}catch(e){{return 'denied'}}}})()")=='denied')
        chk('규칙: 만료가 1시간 넘는 칸 거부',await ev(p5,f"(async()=>{{try{{await db.doc('lvb/{H}').update({E(D,now+7200000)});return 'ok'}}catch(e){{return 'denied'}}}})()")=='denied')
        chk('규칙: 칸에 다른 값 거부',await ev(p5,f"(async()=>{{try{{await db.doc('lvb/{H}').update({E(D,now+600000,",bets:'1'")});return 'ok'}}catch(e){{return 'denied'}}}})()")=='denied')
        chk('규칙: 다른 시간 문서(2시간 뒤) 거부',await ev(p5,f"(async()=>{{try{{await db.doc('lvb/{int(H)+2}').update({E(D,now+600000)});return 'ok'}}catch(e){{return 'denied'}}}})()")=='denied')
        chk('규칙: 정상 칸은 허용·비우기(null) 허용',await ev(p5,f"(async()=>{{try{{await db.doc('lvb/{H}').update({E(D,now+600000)});await db.doc('lvb/{H}').update({{p:{{'{D}':null}}}});return 'ok'}}catch(e){{return 'denied'}}}})()")=='ok')
        chk('규칙: 시간 문서 지우기는 관리자만',await ev(p5,f"(async()=>{{try{{await db.doc('lvb/{int(H)-30}').delete();return 'ok'}}catch(e){{return 'denied'}}}})()")=='denied')
        await asyncio.sleep(0.5)
        chk('규칙: 색인 없으면 친구 아닌 사람 lv 읽기 거부',await try_read(p3,'lv/'+A)=='denied')
        chk('규칙: 색인 없으면 친구 아닌 사람 관전자 등록 거부',await try_write(p3,f'lv/{A}/w/{C}',"{at:SRV_TS}")=='denied')
        chk('규칙: AI 방 중계(k c)는 구글 계정만(지금 턴 정보 허용)',await try_write(p1,'lv/'+A,"{v:1,id:'abcdef12',k:'c',at:SRV_TS,na:'a',nb:'b',me:'A',t:1,ph:'bet',sun:'A',c:'aabbcc',h:''}")=='ok' and await try_write(pg,'lv/'+Gs,"{v:1,id:'abcdef12',k:'c',at:SRV_TS,na:'a',nb:'b',me:'A',t:1,ph:'bet',sun:'A',c:'aabbcc',h:''}")=='denied')
        # 화면: 360 다크·라이트, PC
        await tab(p3,'rank');await ev(p3,"(LX.more=false,lxRender(),0)");await asyncio.sleep(0.5)
        await p3.screenshot(path='/home/claude/eval/live/shots/t_rank_360_dark.png')
        wrap=await p3.evaluate("()=>[...document.querySelectorAll('#lxCard .rt>span,#lxCard h2,#lxCard .lxn,#lxCard .lxgo')].filter(e=>e.getClientRects().length>1||e.scrollHeight>e.clientHeight+2).map(e=>e.textContent)")
        chk('360px: 목록 글 한 줄(줄바꿈 없음)',not wrap,wrap)
        await ev(p3,"(setTheme('light'),0)");await asyncio.sleep(0.3);await p3.screenshot(path='/home/claude/eval/live/shots/t_rank_360_light.png')
        await ev(p3,"(setTheme('dark'),0)")
        await tab(p3,'home');await asyncio.sleep(0.4);await p3.screenshot(path='/home/claude/eval/live/shots/t_home_360_dark.png')
        wrap=await p3.evaluate("()=>[...document.querySelectorAll('#roomsHome .rt>b,#roomsHome .rt>span')].filter(e=>e.getClientRects().length>1).map(e=>e.textContent)")
        chk('360px: 일반 게임 목록 한 줄',not wrap,wrap)
        dn={n:await p.evaluate("()=>(window.__deniedList||[]).filter(x=>!/^read (g\\/|lv\\/)/.test(x)&&!/^lv(b)? /.test(x)&&!/^lv w /.test(x))") for n,p in (('성민',p1),('하율',p2),('지수',p3),('손님',pg),('낯선',p5))}
        chk('예상 밖 거부 없음(시험용 거부 제외)',all(len(v)==0 for v in dn.values()),dn)
        chk('콘솔 오류 0',not errs,errs[:5])
        await b.close()
    n=sum(1 for _,o in RES if o);print(f'\n결과 {n}/{len(RES)} 통과')
asyncio.run(main())
