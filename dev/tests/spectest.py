# 관전 기능 시험: 두 폰 대국 + 세 번째 폰(친구) 관전 / 네 번째 폰(모르는 사람) 규칙 거부
#  ① 접속 상태 종류(AI 대전·랭크 AI·일반·랭크 사람) → 친구 목록 글·끝나면 '접속 중'
#  ② AI 대전 실시간 중계(관전자 있을 때만 씀) ③ 일반 게임 실시간 관전·관전 n명(두 사람 모두)·봉인 비공개
#  ④ 랭크 사람끼리 2턴 지연·끝나면 전체 ⑤ 랭크 AI전 지연·AI 티 안 남 ⑥ 관전 끄기(버튼·규칙) ⑦ 규칙 거부 모음
# 사용: WEBDIR=/home/claude/eval/spec/web FPORT=9391 python3 spectest.py
import asyncio,os,json,time
os.environ.setdefault('WEBDIR','/home/claude/eval/spec/web');os.environ.setdefault('FPORT','9391')
exec(open('/home/claude/eval/spec/tests/friendtest.py').read().split('# ===== 친구 기능 시나리오')[0])
RES=[]
def chk(name,ok,info=''):
    RES.append((name,bool(ok)));print(('PASS ' if ok else 'FAIL ')+name+(' | '+str(info)[:260] if info!='' else ''),flush=True)
async def ev(p,c): return await p.evaluate("c=>window.__T.ev(c)",c)
async def tab(p,k): await p.evaluate(f"()=>document.querySelector('.tabbar:not(.tbw) [data-k={k}]').click()");await asyncio.sleep(0.3)
UID={'성민':'uSpecSeongmin000001','하율':'uSpecHayul000000002','지수':'uSpecJisu0000000003','낯선':'uSpecStranger000004'}
def pidf(x,y): return x+'_'+y if x<y else y+'_'+x
def seed_friend(x,y,nx,ny):
    a,b=sorted([x,y]);na,nb=(nx,ny) if a==x else (ny,nx);now=int(time.time()*1000)
    STORE['fp/'+a+'_'+b]={'a':a,'b':b,'by':a,'st':'ok','at':now,'sa':now,'na':na,'nb':nb,'m':[],'q':0,'ra':0,'rb':0}
async def page(b,errs,name,vp=(390,844)):
    ctx=await b.new_context(viewport={'width':vp[0],'height':vp[1]})
    await ctx.add_init_script(f"sessionStorage.setItem('fake-uid','{UID[name]}');sessionStorage.setItem('fake-g','1');localStorage.setItem('bo-nick','{name}');"
        "localStorage.setItem('bo-tut-done','1');localStorage.setItem('bo-rkintro','1');localStorage.setItem('bo-rklg','1');sessionStorage.setItem('bo-noatt','1');localStorage.setItem('bo-airec',JSON.stringify({pro:{w:1,l:0,d:0},mid:{w:1,l:0,d:0}}))")
    async def route(rt): await rt.fulfill(path=FAKE[rt.request.url.split('/')[-1]],content_type='application/javascript')
    await ctx.route('https://www.gstatic.com/**',route)
    p=await ctx.new_page();p.on('pageerror',lambda e:errs.append(name+':'+str(e)))
    p.on('console',lambda m:errs.append(name+' console:'+m.text) if m.type=='error' and 'ERR_TUNNEL_CONNECTION_FAILED' not in m.text and 'ERR_PROXY' not in m.text else None)
    await p.expose_function('__fsSend',lambda j,p=p:asyncio.ensure_future(relay(p,j)))
    PAGES.append(p);await p.goto(f'http://127.0.0.1:{PORT}/index.html')
    try: await p.click('[data-act=wskip]',timeout=1500)
    except Exception: pass
    return p
async def frtxt(p,u): return await p.evaluate(f"()=>(document.querySelector('#palFr [data-u=\"{u}\"]')?.closest('.frow')?.innerText||'').replace(/\\s+/g,' ')")
async def has_watch(p,u): return await p.evaluate(f"()=>!!document.querySelector('#palFr [data-act=frwatch][data-u=\"{u}\"]')")
async def golobby(p):
    await ev(p,"(leaveRoom&&UI.mode==='online'?leaveRoom():goLobby(),0)");await asyncio.sleep(0.6)
async def try_read(p,path,coll=False):
    m='collection' if coll else 'doc'
    return await ev(p,f"(async()=>{{try{{await db.{m}('{path}').get();return 'ok'}}catch(e){{return 'denied'}}}})()")
async def try_write(p,path,data):
    return await ev(p,f"(async()=>{{try{{await db.doc('{path}').set({data});return 'ok'}}catch(e){{return 'denied'}}}})()")
SPOTS=[(1,2),(1,9),(1,16),(5,2),(5,9),(5,16),(9,2),(9,16),(13,2),(13,9),(13,16),(17,2),(17,9),(17,16)]
async def online_turn(pA,pB,k):
    # 선이 세 칸 고르고(가로 방향) 둘 다 봉인 → 개봉까지
    h0=await ev(pA,"G.st?G.st.hist.length:-1")
    for p in (pA,pB):
        try: await p.click('#coin',timeout=300)
        except Exception: pass
    if not await waitfor(sunpage,90): return 'no sun'
    sp=await sunpage();r,c=SPOTS[k%len(SPOTS)];await tap(sp,r,c);await asyncio.sleep(0.25);await sp.click('[data-act=dconfirm]')
    for p in (pA,pB):
        if not await waitfor(lambda p=p: p.locator('#bsub').count(),60): return 'no bet'
        await p.click('[data-act=bp][data-i="0"]');await p.wait_for_timeout(700);await p.click('#bsub');await asyncio.sleep(0.3)
    ok=await waitfor(lambda: ev(pA,f"!!G.st&&(G.st.hist.length>{h0}||G.st.phase==='over')"),90)
    await asyncio.sleep(2.2)
    return 'ok' if ok else 'no reveal'
async def local_turn(p,k):
    # 내 폰 AI 대전 한 턴: 내 차례면 세 칸 고르고, 베팅 봉인 → 다음 턴까지
    t0=await ev(p,"L.s.hist.length")
    for _ in range(300):
        st=await ev(p,"JSON.stringify({ph:L.s.phase,sun:L.s.sun,st:L.s.stage,h:L.s.hist.length})");s=json.loads(st)
        if s['h']>t0 or s['ph']=='over': return 'ok'
        if os.environ.get('SDBG') and _%10==0: print('  lt',k,st,await p.locator('[data-act=dconfirm]').count(),await txt(p,'#panel'),await p.evaluate("()=>[...document.querySelectorAll('#dlg:not(.hide),.lsheet:not(.hide),#cover:not(.hide)')].map(e=>e.id)"),flush=True)
        if os.environ.get('SDBG') and _==20: await p.screenshot(path='/tmp/spec_lt.png')
        try: await p.click('#coin',timeout=200)
        except Exception: pass
        if s['ph']=='designate' and s['sun']=='A' and await p.locator('[data-act=dconfirm]').count():
            # 이미 고른 칸이 있으면 확정만(같은 칸을 다시 누르면 선택이 풀림)
            if not await ev(p,"!!(UI.sel&&UI.sel.cells)"):
                r,c=SPOTS[(k+_//10)%len(SPOTS)];await tap(p,r,c);await asyncio.sleep(0.3)
            try: await p.click('[data-act=dconfirm]',timeout=800)
            except Exception: pass
        elif s['ph']=='bet' and s['st']!=4 and await p.locator('#bsub').count():
            # 칩을 세 칸에 고루 많이 걸어 판이 너무 빨리 끝나지 않게
            try: await p.click('[data-act=bp][data-i="0"]',timeout=500);await ev(p,"(()=>{const t=L.s.pts.A,q=Math.max(1,Math.floor(t*0.3));UI.bet=[q,q,q];return 0})()");await p.wait_for_timeout(700);await p.click('#bsub',timeout=800)
            except Exception: pass
        await asyncio.sleep(0.3)
    return 'timeout'
async def main():
    errs=[]
    async with async_playwright() as pw:
        b=await pw.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
        A,B,C,D=UID['성민'],UID['하율'],UID['지수'],UID['낯선']
        seed_friend(A,B,'성민','하율');seed_friend(A,C,'성민','지수')
        p1=await page(b,errs,'성민');p2=await page(b,errs,'하율');p3=await page(b,errs,'지수',(360,740));p4=await page(b,errs,'낯선')
        await asyncio.sleep(3)
        chk('가짜 서버에 관전 규칙 켜짐',await p1.evaluate("()=>window.__specRulesOn&&window.__specRulesOn()"))
        for p in (p2,p3): await tab(p,'pal')
        await asyncio.sleep(1.5)
        chk('기본: 접속 중',('접속 중' in await frtxt(p2,A)) and STORE.get('on/'+A,{}).get('st')=='on',(await frtxt(p2,A),STORE.get('on/'+A)))
        # ===== ① AI 대전 → 상태 'AI 대전 중 · Normal', 관전자 없으면 중계 안 씀 =====
        await ev(p1,"(UI.aiLevel='mid',closeSheet(),leaveGame(),UI.mode='local',L.start(null,'mid'),show('game'),$('#cover').classList.add('hide'),renderAll(),0)")
        ok=await waitfor(lambda: p2.evaluate(f"()=>/AI 대전 중/.test(document.querySelector('#palFr [data-u=\"{A}\"]')?.closest('.frow')?.innerText||'')"),60)
        t=await frtxt(p2,A);on=STORE.get('on/'+A,{})
        chk('AI 대전 시작 → 친구 목록 "AI 대전 중 · Normal"(6초 안)',ok and 'AI 대전 중 · Normal' in t and on.get('st')=='a' and on.get('al')=='mid' and on.get('gi')=='',(t,on))
        chk('AI 대전 중 친구에게 관전 버튼',await has_watch(p3,A),await frtxt(p3,A))
        await local_turn(p1,0)
        chk('관전자 없으면 중계 문서 안 씀',('lv/'+A) not in STORE and await p1.evaluate("()=>window.__lvWrites")==0,STORE.get('lv/'+A))
        # 관전 시작(지수)
        await p3.click(f'#palFr [data-act=frwatch][data-u="{A}"]')
        ok=await waitfor(lambda: ev(p3,"!!(G.watch&&G.watch.rl)"),80)
        chk('관전 화면 입장(AI 대전 중계)',ok and await ingame(p3),await txt(p3,'#panel'))
        chk('관전자 표시 문서 lv/성민/w/지수',('lv/'+A+'/w/'+C) in STORE,[k for k in STORE if k.startswith('lv/')])
        await asyncio.sleep(1.2)
        chk('두는 사람 화면에 관전 1명',await p1.evaluate("()=>document.querySelector('#gmid .wcnt')?.getAttribute('aria-label')")=='관전 1명',await txt(p1,'#gmid'))
        h1=await ev(p1,"L.s.hist.length");h3=await ev(p3,"vstate().hist.length")
        chk('AI 대전 실시간: 판 기록 같음',h1==h3 and h1>=1,(h1,h3))
        lv=STORE.get('lv/'+A,{})
        chk('중계 문서: 공개 정보만(베팅·칩·봉인 칸 없음)',set(lv.keys())<= {'v','id','k','at','na','nb','me','al','t','ph','sun','c','h','w','why'} and lv.get('k')=='a' and lv.get('al')=='mid',lv)
        await local_turn(p1,1)
        await asyncio.sleep(1.5)
        b1=await ev(p1,"JSON.stringify(L.s.bd)");b3=await ev(p3,"JSON.stringify(vstate().board)")
        chk('2턴 뒤에도 판 같음(실시간)',b1==b3,(await ev(p1,"L.s.hist.length"),await ev(p3,"vstate().hist.length")))
        # 베팅 단계에서 세 칸이 보임(판이 일찍 끝났으면 새 판 → 중계도 새 판으로 바뀌는지 같이 확인)
        if await ev(p1,"L.s.phase")=='over':
            await ev(p1,"(L.start(null,'mid'),renderAll(),0)")
            ok=await waitfor(lambda: ev(p3,"!!(G.watch&&G.watch.rl&&G.watch.rl.ph!=='over')"),80)
            chk('새 AI 판 → 관전 화면도 새 판',ok,await txt(p3,'#panel'))
        ph=await ev(p1,"L.s.phase")
        if ph=='designate':
            for _ in range(60):
                if await ev(p1,"L.s.phase")=='bet': break
                if await ev(p1,"L.s.sun")=='A' and await p1.locator('[data-act=dconfirm]').count():
                    await tap(p1,*SPOTS[5]);await asyncio.sleep(0.25)
                    try: await p1.click('[data-act=dconfirm]',timeout=800)
                    except Exception: pass
                await asyncio.sleep(0.3)
        await asyncio.sleep(1.5)
        chk('베팅 중 세 칸이 관전 화면에 보임',await ev(p3,"vstate().phase")=='bet' and await ev(p3,"!!vstate().cells") and await p3.evaluate("()=>document.querySelectorAll('#bov .bchip').length")==3,(await ev(p3,"vstate().phase"),await txt(p3,'#panel')))
        chk('관전 화면엔 칩 숫자 없음(? 표시)',await p3.evaluate("()=>document.querySelectorAll('#oppbar .pp.q,#mebar .pp.q').length")==2,await txt(p3,'#game'))
        w1=await p1.evaluate("()=>window.__lvWrites")
        chk('중계 쓰기 수(턴당 2번 이하)',w1<=2*(await ev(p1,"L.s.t"))+1,w1)
        # 끝: 로비로 → '접속 중' 복귀, 관전 화면 안내(판이 끝나 있으면 새 판을 열고 나감)
        if await ev(p1,"L.s.phase")=='over':
            await ev(p1,"(L.start(null,'mid'),renderAll(),0)");await waitfor(lambda: ev(p3,"!!(G.watch&&G.watch.rl&&G.watch.rl.ph!=='over')"),80)
        await golobby(p1)
        ok=await waitfor(lambda: p2.evaluate(f"()=>/접속 중/.test(document.querySelector('#palFr [data-u=\"{A}\"]')?.closest('.frow')?.innerText||'')"),60)
        chk('AI 대전 나가면 "접속 중" 복귀(6초 안)',ok,await frtxt(p2,A))
        await asyncio.sleep(1)
        chk('관전 화면: 친구가 나감 안내',('나갔어요' in await txt(p3,'#panel')),await txt(p3,'#panel'))
        await p3.click('[data-act=lobby]');await asyncio.sleep(1.2)
        chk('관전 닫으면 관전자 표시 지움',('lv/'+A+'/w/'+C) not in STORE)
        await tab(p3,'pal')
        # ===== ⑤ 랭크 AI전: '랭크 게임 중'(사람과 같음), 지연 중계, AI 티 안 남 =====
        await ev(p1,"(mmBot(),0)")
        ok=await waitfor(lambda: p2.evaluate(f"()=>/랭크 게임 중/.test(document.querySelector('#palFr [data-u=\"{A}\"]')?.closest('.frow')?.innerText||'')"),80)
        on=STORE.get('on/'+A,{})
        chk('랭크 AI전 → "랭크 게임 중"(방 id·난이도 없음)',ok and on.get('st')=='r' and on.get('gi')=='' and on.get('al')=='',(await frtxt(p2,A),on))
        await p3.click(f'#palFr [data-act=frwatch][data-u="{A}"]')
        ok=await waitfor(lambda: ev(p3,"!!(G.watch&&G.watch.rl)"),80)
        chk('랭크 AI전 관전 입장',ok,await txt(p3,'#panel'))
        # 턴마다(끝나기 전까지) 관전 화면 = 2턴 전까지
        dl=[];lvl=None;pl=''
        for k in range(4):
            await local_turn(p1,k+3);await asyncio.sleep(1.8)
            if await ev(p1,"L.s.phase")=='over': break
            h1=await ev(p1,"L.s.hist.length");h3=await ev(p3,"vstate().hist.length");dl.append((h1,h3));lvl=dict(STORE.get('lv/'+A,{}))
            for _ in range(30):
                pl=await txt(p3,'#panel')
                if '2턴 늦게' in pl: break
                await asyncio.sleep(0.1)
        chk('랭크 AI전 2턴 지연(턴마다)',len(dl)>=1 and all(h3==max(0,h1-2) for h1,h3 in dl) and dl[-1][0]>=1,dl)
        lv=lvl or {}
        chk('랭크 중계에 지금 턴 정보(선·세 칸) 없음',lv.get('ph')=='live' and 'sun' not in lv and 'c' not in lv and 'al' not in lv,lv)
        bn=await ev(p1,"L.s.bot.nick");js=json.dumps(lv,ensure_ascii=False)
        chk('랭크 AI 상대: 사람 닉네임만(AI·봇 id 없음)',lv.get('nb')==bn and 'AI' not in js and 'bot' not in js and lv.get('k')=='r',js[:200])
        chk('관전 화면 안내 "2턴 늦게"',('2턴 늦게' in pl),pl)
        h1=await ev(p1,"L.s.hist.length")
        await ev(p1,"(L.resign(),0)");await asyncio.sleep(2.5)
        chk('랭크 AI전 끝 → 관전 화면에 전체 공개',await ev(p3,"vstate().phase")=='over' and await ev(p3,"vstate().hist.length")==h1,(await ev(p3,"vstate().phase"),await txt(p3,'#panel')))
        chk('끝난 화면에 복기 버튼 없음(베팅 비공개)',await p3.locator('#panel [data-act=review]').count()==0)
        ok=await waitfor(lambda: p2.evaluate(f"()=>/접속 중/.test(document.querySelector('#palFr [data-u=\"{A}\"]')?.closest('.frow')?.innerText||'')"),60)
        chk('랭크 AI전 끝 → "접속 중"',ok,await frtxt(p2,A))
        await p3.click('[data-act=lobby]');await asyncio.sleep(0.6);await golobby(p1)
        await tab(p3,'pal')
        # ===== ③ 일반 게임(사람끼리) 실시간 관전 =====
        gid=await ev(p1,"(async()=>{await createRoomInner();return G.gid})()")
        await asyncio.sleep(1.5)
        if not gid: gid=await ev(p1,"G.gid")
        await ev(p2,f"(enterGame('{gid}'),0)");await asyncio.sleep(1.5)
        try: await p2.click('[data-act=join]',timeout=3000)
        except Exception: pass
        ok=await waitfor(lambda: p3.evaluate(f"()=>/일반 게임 중/.test(document.querySelector('#palFr [data-u=\"{A}\"]')?.closest('.frow')?.innerText||'')"),80)
        on=STORE.get('on/'+A,{})
        chk('일반 게임 → "일반 게임 중"·방 id 실림',ok and on.get('st')=='g' and on.get('gi')==gid,(await frtxt(p3,A),on))
        chk('친구 목록 관전 버튼',await has_watch(p3,A))
        await p3.click(f'#palFr [data-act=frwatch][data-u="{A}"]')
        ok=await waitfor(lambda: ev(p3,f"G.gid==='{gid}'&&!!G.watch&&G.ready.p"),60)
        chk('일반 게임 관전 입장(봉인 기록 읽기 허용)',ok and await ev(p3,"vstate().spect")==True,await txt(p3,'#panel'))
        chk('관전자는 내 방 목록에 안 남음·대국 접속 표시(rt) 안 씀',not await ev(p3,f"myGames().some(x=>x.g==='{gid}')") and ('rt/g-'+gid+'/p/'+C) not in STORE)
        r=await online_turn(p1,p2,0)
        await asyncio.sleep(1)
        chk('한 턴 진행 → 관전 화면 실시간 반영',r=='ok' and await ev(p3,"vstate().hist.length")==await ev(p1,"vstate().hist.length")>=1,(r,await ev(p3,"vstate().hist.length")))
        await asyncio.sleep(1.5)
        chk('두는 사람(성민) 화면 관전 1명',await p1.evaluate("()=>document.querySelector('#gmid .wcnt')?.getAttribute('aria-label')")=='관전 1명',await txt(p1,'#gmid'))
        ok=await waitfor(lambda: p2.evaluate("()=>document.querySelector('#gmid .wcnt')?.getAttribute('aria-label')==='관전 1명'"),60)
        chk('상대(하율) 화면에도 관전 1명(rt wn)',ok,await txt(p2,'#gmid'))
        # 봉인 비공개: 성민만 봉인한 순간 관전자 기록에는 해시만
        for p in (p1,p2):
            try: await p.click('#coin',timeout=300)
            except Exception: pass
        if await waitfor(sunpage,90):
            sp=await sunpage();await tap(sp,*SPOTS[1]);await asyncio.sleep(0.25);await sp.click('[data-act=dconfirm]')
            await waitfor(lambda: p1.locator('#bsub').count(),60)
            await p1.click('[data-act=bp][data-i="2"]');await p1.wait_for_timeout(700);await p1.click('#bsub');await asyncio.sleep(1.5)
            n=await ev(p1,"vstate().t")
            d3=json.loads(await ev(p3,f"JSON.stringify(((G.docs['{A}']||{{}}).t||{{}})['{n}']||{{}})"))
            chk('봉인 뒤 개봉 전: 관전자에겐 해시뿐(칩 값 없음)',bool(d3.get('h')) and 'v' not in d3 and set(d3)<= {'h','k','a','ak','c','cl'},d3)
            chk('관전 화면 글에 봉인 칩 없음',('내 ' not in await txt(p3,'#panel')) and await p3.evaluate("()=>!document.querySelector('#panel .sealed')"),await txt(p3,'#panel'))
            await waitfor(lambda: p2.locator('#bsub').count(),60)
            await p2.click('[data-act=bp][data-i="0"]');await p2.wait_for_timeout(700);await p2.click('#bsub')
            await waitfor(lambda: ev(p1,f"G.st.hist.length>={n}"),60);await asyncio.sleep(2.5)
        # 규칙 거부: 모르는 사람(낯선)은 진행 중 방 기록을 못 읽음
        chk('규칙: 친구 아닌 사람은 진행 중 g/p 읽기 거부',await try_read(p4,f'g/{gid}/p',True)=='denied')
        chk('규칙: 친구 아닌 사람은 lv·관전자 등록 거부',await try_read(p4,'lv/'+A)=='denied' and await try_write(p4,f'lv/{A}/w/{D}','{at:SRV_TS}')=='denied')
        chk('규칙: 남의 중계 문서 쓰기 거부',await try_write(p3,'lv/'+A,"{v:1,id:'0000aaaa',k:'a',at:SRV_TS,na:'x',nb:'y',me:'A',t:1,ph:'bet',h:''}")=='denied')
        chk('규칙: 중계에 베팅 칸(b) 넣기 거부',await try_write(p1,'lv/'+A,"{v:1,id:'0000aaaa',k:'a',at:SRV_TS,na:'x',nb:'y',me:'A',t:1,ph:'bet',h:'',b:[3,1,1]}")=='denied')
        chk('규칙: 랭크 중계에 지금 세 칸 넣기 거부',await try_write(p1,'lv/'+A,"{v:1,id:'0000aaaa',k:'r',at:SRV_TS,na:'x',nb:'y',me:'A',t:1,ph:'live',h:'',c:'aaabac'}")=='denied')
        chk('규칙: 관전자 표시 30초 안 다시 쓰기 거부',await try_write(p3,f'lv/{A}/w/{C}','{at:SRV_TS}')=='denied')
        # ===== ⑥ 관전 끄기 =====
        await p1.evaluate("()=>{const e=document.querySelector('#frSetSp');e.checked=false;e.dispatchEvent(new Event('change',{bubbles:true}))}");await asyncio.sleep(1.5)
        chk('관전 끄기 저장 on.sp=false',STORE.get('on/'+A,{}).get('sp') is False,STORE.get('on/'+A))
        chk('규칙: 관전 끄면 친구도 g/p 읽기 거부',await try_read(p3,f'g/{gid}/p',True)=='denied')
        chk('규칙: 관전 끄면 lv 읽기·관전자 등록 거부',await try_read(p3,'lv/'+A)=='denied' and await try_write(p3,f'lv/{A}/w/{C}x','{at:SRV_TS}')=='denied')
        await p3.click('[data-act=lobby]');await asyncio.sleep(1);await tab(p3,'pal');await asyncio.sleep(1.2)
        chk('관전 끄면 친구 목록에 관전 버튼 없음(상태 글은 그대로)',(not await has_watch(p3,A)) and ('일반 게임 중' in await frtxt(p3,A)),await frtxt(p3,A))
        await p1.evaluate("()=>{const e=document.querySelector('#frSetSp');e.checked=true;e.dispatchEvent(new Event('change',{bubbles:true}))}");await asyncio.sleep(1.5)
        chk('다시 켜면 버튼 보임',await waitfor(lambda: has_watch(p3,A),40))
        # 끝: 기권 → 끝난 판은 누구나(복기·결과 확인)
        await p2.click('#resignBtn');await p2.click('[data-act=dlgok]');await asyncio.sleep(2.5)
        chk('끝난 판 기록은 공개(결과 확인)',await try_read(p4,f'g/{gid}/p',True)=='ok')
        ok=await waitfor(lambda: p3.evaluate(f"()=>/접속 중/.test(document.querySelector('#palFr [data-u=\"{A}\"]')?.closest('.frow')?.innerText||'')"),60)
        chk('일반 게임 끝 → "접속 중"',ok,await frtxt(p3,A))
        for p in (p1,p2): await golobby(p)
        # ===== ④ 랭크전(사람끼리) 2턴 지연 =====
        for p in (p1,p2): await tab(p,'rank')
        await p1.click('#mmBtn');await asyncio.sleep(0.3);await p2.click('#mmBtn')
        ok=await waitfor(lambda: ev(p1,"!!(UI.mode==='online'&&G.meta&&G.meta.ranked&&G.st&&G.st.A&&G.docs[G.meta.guest])"),120)
        ok2=await waitfor(lambda: ev(p2,"!!(UI.mode==='online'&&G.meta&&G.meta.ranked)"),60)
        chk('랭크전(사람끼리) 매칭',ok and ok2,(await txt(p1,'#mmSt'),await ev(p1,"UI.mode")))
        if ok and ok2:
            rg=await ev(p1,"G.gid")
            ok=await waitfor(lambda: p3.evaluate(f"()=>/랭크 게임 중/.test(document.querySelector('#palFr [data-u=\"{A}\"]')?.closest('.frow')?.innerText||'')"),80)
            on=STORE.get('on/'+A,{})
            chk('랭크 사람전도 같은 글 "랭크 게임 중"·방 id 없음',ok and on.get('st')=='r' and on.get('gi')=='',on)
            chk('규칙: 랭크 진행 중 g/p는 친구도 거부',await try_read(p3,f'g/{rg}/p',True)=='denied')
            await p3.click(f'#palFr [data-act=frwatch][data-u="{A}"]')
            ok=await waitfor(lambda: ev(p3,"!!(G.watch&&G.watch.rl)"),80)
            chk('랭크 사람전 관전 입장(중계)',ok,await txt(p3,'#panel'))
            res=[]
            for k in range(3): res.append(await online_turn(p1,p2,k+6))
            await asyncio.sleep(1.5)
            h1=await ev(p1,"G.st.hist.length");h3=await ev(p3,"vstate().hist.length")
            chk('랭크 사람전 2턴 지연',h1>=3 and h3==h1-2,(res,h1,h3))
            lv=STORE.get('lv/'+A,{})
            chk('랭크 중계 id는 방 id가 아님',lv.get('id')!=rg and rg[1:] not in json.dumps(lv),lv.get('id'))
            ok=await waitfor(lambda: p2.evaluate("()=>document.querySelector('#gmid .wcnt')?.getAttribute('aria-label')==='관전 1명'"),40)
            chk('랭크 상대 화면에도 관전 1명',ok,await txt(p2,'#gmid'))
            await p2.click('#resignBtn');await p2.click('[data-act=dlgok]');await asyncio.sleep(3)
            chk('랭크 끝 → 전체 공개',await ev(p3,"vstate().phase")=='over' and await ev(p3,"vstate().hist.length")==h1,(await ev(p3,"vstate().phase"),await ev(p3,"vstate().hist.length")))
        # ===== 마무리 =====
        dl={n:await p.evaluate("()=>(window.__deniedList||[]).filter(x=>!/^read (g\\/|lv\\/)/.test(x)&&!/^lv /.test(x))") for n,p in (('성민',p1),('하율',p2),('지수',p3))}
        chk('예상 밖 거부 없음(시험용 거부 제외)',all(len(v)==0 for v in dl.values()),dl)
        onw=await p1.evaluate("()=>window.__onWrites");chk('접속 표시 쓰기 수(성민) 적당',onw<=24,onw)
        chk('콘솔 오류 0',not errs,errs[:5])
        await b.close()
    n=sum(1 for _,o in RES if o);print(f'\n결과 {n}/{len(RES)} 통과')
asyncio.run(main())
