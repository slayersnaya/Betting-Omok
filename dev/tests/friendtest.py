import asyncio,json,threading,http.server,socketserver,functools,time
from playwright.async_api import async_playwright
PORT=int(__import__("os").environ.get("FPORT","8931"))
class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self,*a):pass
def serve():
    socketserver.TCPServer.allow_reuse_address=True
    with socketserver.TCPServer(('127.0.0.1',PORT),functools.partial(Q,directory=__import__('os').environ.get('WEBDIR','/home/claude/eval/gd2/web'))) as s:s.serve_forever()
threading.Thread(target=serve,daemon=True).start()
FAKE={'firebase-app.js':'/home/claude/firebase/fake/app.js','firebase-auth.js':'/home/claude/firebase/fake/auth.js','firebase-firestore.js':'/home/claude/firebase/fake/fs.js'}
STORE={};PAGES=[]
def deep(t,s):
    for k,v in s.items():
        if isinstance(v,dict):
            if not isinstance(t.get(k),dict): t[k]={}
            deep(t[k],v)
        else: t[k]=v
async def send(p,j):
    try: await p.evaluate("j=>window.__fsRecv(j)",j)
    except Exception: pass
async def relay(src,j):
    m=json.loads(j)
    if m['t']=='sync?': await send(src,json.dumps({'t':'sync','store':STORE}));return
    if m['t']=='sync': return
    # 서버 흉내(친구 대화): 실제 Firestore는 쓰기를 한 줄로 세워 규칙을 검사함 → 낡은 목록으로 쓴 메시지는 거부되고 보낸 폰 사본은 되돌아감
    if m.get('op')!='del' and m['p'].startswith('fp/') and isinstance(m.get('d'),dict) and 'm' in m['d'] and m['p'] in STORE:
        cur=STORE[m['p']].get('m',[]);nw=m['d']['m'];q0=STORE[m['p']].get('q',0)
        ok=m['d'].get('q')==q0+1 and ((len(cur)<50 and len(nw)==len(cur)+1 and nw[:len(cur)]==cur) or (len(cur)>=50 and len(nw)==50 and nw[:49]==cur[-49:]))
        if not ok:
            await send(src,json.dumps({'t':'w','op':'set','p':m['p'],'d':STORE[m['p']]}));return
    if m['op']=='del': STORE.pop(m['p'],None)
    elif m.get('merge'): STORE.setdefault(m['p'],{});deep(STORE[m['p']],m['d'])
    else: STORE[m['p']]=m['d']
    for p in PAGES:
        if p is not src: await send(p,j)
CELL,M=32,30
async def tap(p,r,c):
    vb=await p.evaluate("()=>document.querySelector('#board').getAttribute('viewBox').split(' ').map(Number)")
    box=await p.locator('#board').bounding_box()
    await p.mouse.click(box['x']+(M+c*CELL-vb[0])/vb[2]*box['width'],box['y']+(M+r*CELL-vb[1])/vb[3]*box['height'])
async def txt(p,sel): return await p.evaluate(f"()=>(document.querySelector('{sel}')?.innerText||'').replace(/\\s+/g,' ').slice(0,140)")
async def waitfor(cond,tries=80):
    for _ in range(tries):
        await asyncio.sleep(0.1)
        if await cond(): return True
    return False
async def sunpage():
    for p in PAGES:
        if await p.locator('[data-act=dconfirm]').count(): return p
async def ingame(p): return await p.evaluate("()=>!document.querySelector('#game').classList.contains('hide')")
async def newpage(b,errs,name,google=True,vp=(390,844),hash=''):
    ctx=await b.new_context(viewport={'width':vp[0],'height':vp[1]})
    await ctx.add_init_script(("sessionStorage.setItem('fake-g','1');" if google else "")+f"localStorage.setItem('bo-nick','{name}');"+"localStorage.setItem('bo-tut-done','1');localStorage.setItem('bo-rkintro','1');localStorage.setItem('bo-rklg','1');sessionStorage.setItem('bo-noatt','1');localStorage.setItem('bo-airec',JSON.stringify({pro:{w:1,l:0,d:0}}))")
    async def route(rt): await rt.fulfill(path=FAKE[rt.request.url.split('/')[-1]],content_type='application/javascript')
    await ctx.route('https://www.gstatic.com/**',route)
    p=await ctx.new_page();p.on('pageerror',lambda e:errs.append(name+':'+str(e)))
    p.on('console',lambda m:errs.append(name+' console:'+m.text) if m.type=='error' else None)
    await p.expose_function('__fsSend',lambda j,p=p:asyncio.ensure_future(relay(p,j)))
    PAGES.append(p);await p.goto(f'http://127.0.0.1:{PORT}/index.html'+hash)
    try: await p.click('[data-act=wskip]',timeout=1500)
    except Exception: pass
    await p.evaluate("n=>{const e=document.querySelector('#nick');if(e)e.value=n}",name)
    return p
async def play_round(p1,p2):
    await asyncio.sleep(2.5)
    for p in PAGES:
        try: await p.click('#coin',timeout=500)
        except Exception: pass
    if not await waitfor(sunpage,60): return 'no sun'
    sp=await sunpage();await tap(sp,9,9);await sp.click('[data-act=dconfirm]')
    if not await waitfor(lambda: p1.locator('#bsub').count(),60): return 'no bet p1'
    await p1.click('[data-act=bp][data-i="0"]');await p1.wait_for_timeout(650);await p1.click('#bsub')
    await waitfor(lambda: p2.locator('#bsub').count(),60)
    await p2.click('[data-act=bp][data-i="1"]');await p2.wait_for_timeout(650);await p2.click('#bsub')
    await asyncio.sleep(1.5)
    st=await txt(p1,'#panel')
    await p2.click('#resignBtn');await p2.click('[data-act=dlgok]');await asyncio.sleep(1.2)
    return st
# ===== 친구 기능 시나리오 (가짜 Firebase로 폰 여러 대) =====
RES=[]
def chk(name,ok,info=''):
    RES.append((name,bool(ok)));print(('PASS ' if ok else 'FAIL ')+name+(' | '+str(info)[:200] if info else ''))
async def ev(p,c): return await p.evaluate("c=>window.__T.ev(c)",c)
async def den(p): return await p.evaluate("()=>(window.__deniedList||[]).slice()")
async def tab(p,k): await p.evaluate(f"()=>document.querySelector('.tabbar:not(.tbw) [data-k={k}]').click()");await asyncio.sleep(0.3)
async def main():
    errs=[]
    async with async_playwright() as pw:
        b=await pw.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
        p1=await newpage(b,errs,'성민');p2=await newpage(b,errs,'하율')
        await asyncio.sleep(3)
        u1=await ev(p1,'SEAT');u2=await ev(p2,'SEAT')
        nk=[(k,v) for k,v in STORE.items() if k.startswith('nicks/')]
        chk('nicks 문서에 표시용 n',all(v.get('n') for k,v in nk) and len(nk)>=2,nk)
        # 1) 닉네임 앞부분 검색 → 요청
        await tab(p1,'pal')
        chk('친구 탭 보임(구글)',await p1.evaluate("()=>!document.querySelector('#tab-pal').classList.contains('hide')&&document.querySelector('#palGate').classList.contains('hide')"))
        await p1.click('#palAdd');await asyncio.sleep(0.4)
        chk('친구 탭은 목록만(찾기·코드는 시트)',await p1.evaluate("()=>!document.querySelector('#tab-pal #palQ')&&!!document.querySelector('#sh-fadd:not(.hide) #palQ')&&!!document.querySelector('#sh-fadd #palCode')"))
        await p1.fill('#palQ','하');await asyncio.sleep(0.8)
        chk('1글자는 검색 안 함',await txt(p1,'#palQn')=='2글자 이상 입력하면 찾아요')
        await p1.fill('#palQ','하율');await asyncio.sleep(1.2)
        r=await txt(p1,'#palRes');chk('검색 결과에 하율',('하율' in r),r)
        await p1.click(f'#palRes [data-act=fradd][data-u="{u2}"]');await asyncio.sleep(0.8)
        await p1.evaluate("()=>document.querySelector('#shbg').click()");await asyncio.sleep(0.2)
        pid=u1+'_'+u2 if u1<u2 else u2+'_'+u1
        chk('요청 문서 st=req',STORE.get('fp/'+pid,{}).get('st')=='req',STORE.get('fp/'+pid))
        await asyncio.sleep(0.5)
        chk('받는 쪽 탭 배지 1',await p2.evaluate("()=>document.querySelector('.tabbar:not(.tbw) [data-k=pal] .tbn').textContent")=='1')
        await tab(p2,'pal');await asyncio.sleep(0.3)
        chk('탭 목록 위 받은 요청 줄',('성민' in await txt(p2,'#palReqLine')) and await p2.evaluate("()=>!document.querySelector('#palReqLine').classList.contains('hide')"),await txt(p2,'#palReqLine'))
        await p2.click('#palReqLine');await asyncio.sleep(0.4)
        chk('받은 요청 표시',('성민' in await txt(p2,'#palReq')),await txt(p2,'#palReq'))
        await p2.click(f'#palReq [data-act=frok][data-u="{u1}"]');await asyncio.sleep(1)
        await p2.evaluate("()=>document.querySelector('#shbg').click()");await asyncio.sleep(0.2)
        chk('수락 → st=ok',STORE.get('fp/'+pid,{}).get('st')=='ok')
        await asyncio.sleep(1.5)
        chk('친구 목록에 서로',('하율' in await txt(p1,'#palFr')) and ('성민' in await txt(p2,'#palFr')),(await txt(p1,'#palFr'),await txt(p2,'#palFr')))
        chk('접속 문서 on 작성',STORE.get('on/'+u1,{}).get('st')=='on' and STORE.get('on/'+u2,{}).get('st')=='on',(STORE.get('on/'+u1),STORE.get('on/'+u2)))
        await asyncio.sleep(1)
        chk('접속 중 표시',('접속 중' in await txt(p1,'#palFr')),await txt(p1,'#palFr'))
        # 2) 대화 왕복·안 읽은 수·읽음
        await p1.click(f'#palFr [data-act=frchat][data-u="{u2}"]');await asyncio.sleep(0.4)
        await p1.fill('#chIn','안녕 하율');await p1.press('#chIn','Enter');await asyncio.sleep(1.2)
        chk('메시지 저장',[m['t'] for m in STORE['fp/'+pid].get('m',[])]==['안녕 하율'],STORE['fp/'+pid].get('m'))
        chk('받는 쪽 안 읽은 수 1',await p2.evaluate(f"()=>document.querySelector('#palFr [data-u=\"{u1}\"] .fbd')?.textContent")=='1')
        await p2.click(f'#palFr [data-act=frchat][data-u="{u1}"]');await asyncio.sleep(1.2)
        s=STORE['fp/'+pid];side2='a' if u2<u1 else 'b'
        chk('읽음 위치 갱신',s.get('r'+side2)==1,s)
        await asyncio.sleep(0.6)
        chk('보낸 쪽 읽음 표시',('읽음' in await txt(p1,'#chLog')),await txt(p1,'#chLog'))
        # 연속 3개(1초 제한은 앱이 차례로 보냄)
        for t in ['하나','둘','셋']:
            await p1.fill('#chIn',t);await p1.press('#chIn','Enter')
        await asyncio.sleep(5)
        chk('연속 3개 모두 전달',[m['t'] for m in STORE['fp/'+pid]['m']][-3:]==['하나','둘','셋'],[m['t'] for m in STORE['fp/'+pid]['m']])
        # 동시에 보내기(앞부분 불일치 → 거부 → 재시도)
        await p1.fill('#chIn','동시1');await p2.fill('#chIn','동시2')
        await asyncio.gather(p1.press('#chIn','Enter'),p2.press('#chIn','Enter'))
        for _ in range(16):
            await asyncio.sleep(0.5)
            ts=[m['t'] for m in STORE['fp/'+pid]['m']]
            if '동시1' in ts and '동시2' in ts: break
        ts=[m['t'] for m in STORE['fp/'+pid]['m']]
        dbg='' if ('동시1' in ts and '동시2' in ts) else await p2.evaluate("()=>window.__T.ev('JSON.stringify({out:FR.out,sent:FR.sent.map(x=>({t:x.t,i:x.i,a:x.a})),q:[...FR.pairs.values()][0].q,m:[...FR.pairs.values()][0].m.map(x=>x.t)})')")
        chk('동시 전송 둘 다 전달',('동시1' in ts) and ('동시2' in ts),(ts,dbg))
        # 링크·전화번호 막기, 욕설 가림
        await p1.fill('#chIn','www.abc.com 들어와');await p1.press('#chIn','Enter');await asyncio.sleep(0.4)
        chk('링크 막음',await p1.input_value('#chIn')=='www.abc.com 들어와' and 'www.abc' not in str(STORE['fp/'+pid]['m']))
        await p1.fill('#chIn','010-1234-5678');await p1.press('#chIn','Enter');await asyncio.sleep(0.3)
        chk('전화번호 막음','010-1234' not in str(STORE['fp/'+pid]['m']))
        await p1.fill('#chIn','');await asyncio.sleep(1.2)
        await p1.fill('#chIn','아 시발 졌다');await p1.press('#chIn','Enter');await asyncio.sleep(1.5)
        chk('욕설 가림',STORE['fp/'+pid]['m'][-1]['t']=='아 ** 졌다',STORE['fp/'+pid]['m'][-1])
        # 반응
        await asyncio.sleep(0.5)
        last=STORE['fp/'+pid]['m'][-1]['i']
        await p2.click(f'#chLog [data-act=frrx][data-i="{last}"]');await asyncio.sleep(0.2)
        await p2.click('#chLog [data-act=frrxs][data-v="0"]');await asyncio.sleep(1.8)
        chk('반응 저장',STORE['fp/'+pid]['m'][-1].get('e')==last,STORE['fp/'+pid]['m'][-1])
        chk('반응 표시',await p1.evaluate("()=>!!document.querySelector('#chLog .rxs')"))
        # 서버 규칙: 1초 안에 직접 두 번 쓰기 거부, 남의 칸으로 쓰기 거부
        r=await ev(p1,f"""(async()=>{{const p=FR.pairs.get('{pid}'),s=frS(p),q=p.q+1,m=frMsgs(p).concat([{{i:q,s,t:'x',a:Date.now()}}]).slice(-50);
          try{{await db.doc('fp/{pid}').update({{m,q,['w'+s]:SRV_TS,['r'+s]:q}})}}catch(e){{return 'first denied '+e.code}}
          const m2=m.concat([{{i:q+1,s,t:'y',a:Date.now()}}]).slice(-50);try{{await db.doc('fp/{pid}').update({{m:m2,q:q+1,['w'+s]:SRV_TS,['r'+s]:q+1}});return 'second ok'}}catch(e){{return 'second denied'}}}})()""")
        chk('규칙: 1초 안 연속 쓰기 거부',r=='second denied',r)
        await asyncio.sleep(1.2)
        r=await ev(p1,f"""(async()=>{{const p=FR.pairs.get('{pid}'),o=frO(p),q=p.q+1,m=frMsgs(p).concat([{{i:q,s:o,t:'사칭',a:Date.now()}}]).slice(-50);
          try{{await db.doc('fp/{pid}').update({{m,q,['w'+frS(p)]:SRV_TS,['r'+frS(p)]:q}});return 'ok'}}catch(e){{return 'denied'}}}})()""")
        chk('규칙: 상대 이름으로 쓰기 거부',r=='denied',r)
        r=await ev(p1,f"""(async()=>{{const p=FR.pairs.get('{pid}'),s=frS(p),q=p.q+1,m=frMsgs(p).slice(1).concat([{{i:q,s,t:'z',a:Date.now()}}]);
          try{{await db.doc('fp/{pid}').update({{m,q,['w'+s]:SRV_TS,['r'+s]:q}});return 'ok'}}catch(e){{return 'denied'}}}})()""")
        chk('규칙: 지난 메시지 지우기 거부',r=='denied',r)
        r=await ev(p1,f"""(async()=>{{const p=FR.pairs.get('{pid}'),s=frS(p),q=p.q+1,m=frMsgs(p).concat([{{i:q,s,t:'가'.repeat(201),a:Date.now()}}]);
          try{{await db.doc('fp/{pid}').update({{m,q,['w'+s]:SRV_TS,['r'+s]:q}});return 'ok'}}catch(e){{return 'denied'}}}})()""")
        chk('규칙: 200자 넘는 글 거부',r=='denied',r)
        await p1.evaluate("()=>document.querySelector('#shbg').click()");await p2.evaluate("()=>document.querySelector('#shbg').click()");await asyncio.sleep(0.3)
        # 3) 대국 신청 → 수락 → 같은 방 → 대국 → 끝
        await p1.click(f'#palFr [data-act=frprof][data-u="{u2}"]');await asyncio.sleep(0.4)
        pf=await txt(p1,'#pfBody');chk('친구 프로필(티어·전적·나와의 전적·대국 신청)',all(x in pf for x in ['티어','점수','순위','랭크전','나와의 전적','대국 신청']),pf)
        await p1.click('#pfBody [data-act=frinv]');await asyncio.sleep(0.4)
        chk('신청 전 시간 고르기',('제한 시간' in await txt(p1,'#dlg')),await txt(p1,'#dlg'))
        await p1.click('#dlg [data-act=frinvp][data-i="0"]');await asyncio.sleep(1.8)
        chk('신청한 쪽 대국 화면',await ingame(p1))
        sa='a' if u1<u2 else 'b'
        inv=STORE['fp/'+pid].get('g'+sa)
        chk('신청 기록 {gid,at,t}',bool(inv and inv.get('gid')) and inv.get('t')==0,inv)
        await asyncio.sleep(1.2)
        chk('보낸 쪽 기다리는 중·취소',('기다리는 중' in await txt(p1,'#frInv')) and await p1.locator('#frInv [data-act=frinvcan]').count()==1,await txt(p1,'#frInv'))
        chk('받는 쪽 위 알림 "대국을 신청했어요"',('대국을 신청했어요' in await txt(p2,'#frInv')),await txt(p2,'#frInv'))
        # 방 링크 공유(공유 창 없는 PC → 링크 복사 상자)
        await p1.evaluate("()=>{navigator.share=undefined;const b=document.querySelector('[data-act=invite]');if(b)b.click()}");await asyncio.sleep(0.3)
        d=await txt(p1,'#dlg');lv=await p1.evaluate("()=>document.querySelector('#dlg .fshare input')?.value||''");chk('방 링크 공유 → 링크 복사 상자(#g-)',('링크 복사' in d) and ('#g-'+inv['gid'] in lv),(d,lv))
        try: await p1.click('#dlg [data-act=dlgno]',timeout=800)
        except Exception: pass
        await p2.click('#frInv [data-act=frinvok]')
        ok=await waitfor(lambda: ingame(p2),60);await asyncio.sleep(4)
        g=STORE.get('g/'+inv['gid'],{})
        chk('수락 → 같은 방 입장·자동 참가(진행 중)',ok and g.get('status')=='playing' and g.get('guest')==u2,g)
        chk('대국 시작 후 신청 정리',not STORE['fp/'+pid].get('g'+sa),STORE['fp/'+pid].get('g'+sa))
        ks=[m.get('k') for m in STORE['fp/'+pid]['m'] if m.get('k')]
        chk('대화에 신청·수락 기록',ks[-2:]==['inv','acc'],ks)
        await asyncio.sleep(13)
        chk('대국 중 접속 상태 g',STORE.get('on/'+u1,{}).get('st')=='g',STORE.get('on/'+u1))
        await ev(p2,f"(FR.chat='{u1}',frSend('대국 중 메시지'))");await asyncio.sleep(2.5)
        chk('대국 중에는 배지만(토스트 없음)',await p1.evaluate("()=>!document.querySelector('#frBadge').classList.contains('hide')"))
        st=await play_round(p1,p2);await asyncio.sleep(1.5)
        chk('친구 대국 한 턴 진행 → 끝',('승' in await txt(p1,'#panel')) or ('기권' in await txt(p1,'#panel')),(st,await txt(p1,'#panel')))
        for p in (p1,p2):
            try: await p.click('[data-act=lobby]',timeout=2000)
            except Exception: pass
        await asyncio.sleep(2)
        vs=await ev(p1,f"JSON.stringify(frH2H('{u2}'))");chk('나와의 전적 반영',('"n":1' in vs),vs)
        # 거절 흐름
        await tab(p1,'pal');await p1.click(f'#palFr [data-act=frinv][data-u="{u2}"]');await asyncio.sleep(0.3)
        d=await txt(p1,'#dlg')
        if '그래도 신청' in d:
            chk('상대가 대국 중이면 먼저 안내',('대국 중' in d),d);await p1.click('#dlg [data-act=dlgok]');await asyncio.sleep(0.3)
        await p1.click('#dlg [data-act=frinvp][data-i="1"]');await asyncio.sleep(2.5)
        inv2=STORE['fp/'+pid].get('g'+sa)
        await p2.click('#frInv [data-act=frinvno]');await asyncio.sleep(2.5)
        chk('거절 → 보낸 쪽 로비로·방 정리',(not await ingame(p1)) and ('g/'+inv2['gid'] not in STORE),(await ingame(p1),inv2))
        ks=[m.get('k') for m in STORE['fp/'+pid]['m'] if m.get('k')]
        chk('대화에 거절 기록',ks[-1]=='dec',ks)
        await asyncio.sleep(1.5)
        # 취소 흐름
        await ev(p1,f"frInviteGo('{u2}',0)");await asyncio.sleep(2.5)
        await p1.click('#frInv [data-act=frinvcan]');await asyncio.sleep(2.5)
        chk('취소 → 신청 지움·로비',(not STORE['fp/'+pid].get('g'+sa)) and not await ingame(p1),STORE['fp/'+pid].get('g'+sa))
        await asyncio.sleep(1.5)
        # 만료 흐름(보낸 폰 시계를 3분 앞으로)
        await ev(p1,f"frInviteGo('{u2}',0)");await asyncio.sleep(2.5)
        inv3=STORE['fp/'+pid].get('g'+sa)
        await p1.evaluate("()=>{const o=Date.now.bind(Date);Date.now=()=>o()+185e3}");await asyncio.sleep(3)
        await p1.evaluate("()=>{location.reload}")
        chk('3분 지나면 닫고 방 정리',(not STORE['fp/'+pid].get('g'+sa)) and ('g/'+inv3['gid'] not in STORE) and not await ingame(p1),(STORE['fp/'+pid].get('g'+sa),inv3))
        ks=[m.get('k') for m in STORE['fp/'+pid]['m'] if m.get('k')]
        chk('대화에 만료 기록',ks[-1]=='exp',ks)
        await p1.reload();await asyncio.sleep(3.5)
        # 연속 신청 제한(10분 3번)
        r=await ev(p1,f"(FR.invLog.set('{u2}',[Date.now(),Date.now(),Date.now()]),frInvite('{u2}'),document.querySelector('#toast').textContent)")
        chk('같은 친구 연속 신청 제한',('잠시 뒤' in r),r)
        r=await ev(p1,f"""(async()=>{{const p=FR.pairs.get('{pid}'),s=frS(p);try{{await db.doc('fp/{pid}').update({{['g'+s]:{{gid:'g12345678',at:Date.now()}}}});return 'ok'}}catch(e){{return 'denied'}}}})()""")
        chk('규칙: 내 방 아닌 곳으로 신청 거부',r=='denied',r)
        # 4) AI 이름 검색·요청
        bn=await ev(p1,'BOTS[0].nick');bid=await ev(p1,"BOTPRE+BOTS[0].id")
        await tab(p1,'pal');await p1.click('#palAdd');await asyncio.sleep(0.3);await p1.fill('#palQ',bn[:2]);await asyncio.sleep(1.2)
        r=await txt(p1,'#palRes');chk('AI 이름도 검색됨(같은 모양)',bn in r,(bn,r))
        await p1.click(f'#palRes [data-act=fradd][data-u="{bid}"]');await asyncio.sleep(0.4)
        chk('AI 요청 → 받지 않는 사용자 안내',('받지 않는 사용자' in await txt(p1,'#dlg')),await txt(p1,'#dlg'))
        await p1.click('[data-act=dlgok]');await asyncio.sleep(0.2)
        await p1.evaluate("()=>window.__T.ev('closeSheet()')");await asyncio.sleep(0.2)
        # 랭킹에서 프로필
        await tab(p1,'rank');await asyncio.sleep(0.5)
        await p1.evaluate("()=>document.querySelector('#rkBoard .rkrow[data-act=prof]').click()");await asyncio.sleep(0.4)
        pf=await txt(p1,'#pfBody');chk('랭킹 줄 → 프로필(친구 추가 버튼)',('친구 추가' in pf) and ('티어' in pf),pf)
        await p1.evaluate("()=>document.querySelector('#shbg').click()");await asyncio.sleep(0.2)
        # 5) 초대 링크(토큰) → 바로 친구
        await tab(p1,'pal')
        code=await ev(p1,"(async()=>{const o=navigator.share;navigator.share=undefined;await frShare();return FR.code+'.'+FR.mine.tk})()")
        await asyncio.sleep(0.5)
        chk('친구 코드·토큰 생성',bool(code) and '.' in code and len(code)==25,code)
        c8,tk=code.split('.');p3=await newpage(b,errs,'세번째',hash=f'?f={c8}&k={tk}');await asyncio.sleep(4)
        u3=await ev(p3,'SEAT')
        d=await txt(p3,'#dlg');chk('?f= 링크로 열면 "친구 할까요?" 확인',('성민' in d) and ('친구 할까요' in d),d)
        chk('링크 열고 주소에서 코드 지움',('?f=' not in p3.url),p3.url)
        await p3.click('[data-act=dlgok]');await asyncio.sleep(1.2)
        pid13=u1+'_'+u3 if u1<u3 else u3+'_'+u1
        chk('토큰 링크 → 바로 친구(st ok)',STORE.get('fp/'+pid13,{}).get('st')=='ok',STORE.get('fp/'+pid13))
        await asyncio.sleep(1)
        chk('초대한 쪽 목록에 새 친구',('세번째' in await txt(p1,'#palFr')),await txt(p1,'#palFr'))
        # 친구 코드로 검색
        await tab(p2,'pal');await p2.click('#palAdd');await asyncio.sleep(0.3);await p2.fill('#palQ',code[:4]+'-'+code[4:8]);await asyncio.sleep(1.2)
        chk('친구 코드로 찾기',('성민' in await txt(p2,'#palRes')),await txt(p2,'#palRes'))
        # 잘못된 토큰은 바로 친구 불가(규칙)
        r=await ev(p3,f"""(async()=>{{const u='{u2}',a=SEAT<u?SEAT:u,b=SEAT<u?u:SEAT;try{{await db.doc('fp/'+frPid(SEAT,u)).set({{a,b,by:SEAT,st:'ok',tk:'0123456789abcdef',at:SRV_TS,sa:SRV_TS,na:'',nb:'',m:[],q:0,ra:0,rb:0}});return 'ok'}}catch(e){{return 'denied'}}}})()""")
        chk('규칙: 틀린 토큰으로 바로 친구 거부',r=='denied',r)
        # 6) 거절 → 7일 재요청 금지
        await ev(p3,f"frRequest('{u2}','하율')");await asyncio.sleep(1)
        pid23=u2+'_'+u3 if u2<u3 else u3+'_'+u2
        await ev(p2,f"frDecline('{u3}')");await asyncio.sleep(1)
        chk('거절 → st no',STORE.get('fp/'+pid23,{}).get('st')=='no',STORE.get('fp/'+pid23))
        r=await ev(p3,f"(async()=>{{try{{await db.doc('fp/{pid23}').update({{st:'req',sa:SRV_TS}});return 'ok'}}catch(e){{return 'denied'}}}})()")
        chk('규칙: 거절 후 7일 안 재요청 거부',r=='denied',r)
        r=await ev(p3,f"(async()=>{{try{{await db.doc('fp/{pid23}').delete();return 'ok'}}catch(e){{return 'denied'}}}})()")
        chk('규칙: 거절당한 쪽이 기록 지우기 거부',r=='denied',r)
        r=await ev(p3,f"(async()=>{{try{{await db.doc('on/{u2}').get();return 'ok'}}catch(e){{return 'denied'}}}})()")
        chk('규칙: 친구 아닌 사람 접속 정보 읽기 거부',r=='denied',r)
        r=await ev(p3,f"(async()=>{{try{{await db.doc('on/{u1}').get();return 'ok'}}catch(e){{return 'denied'}}}})()")
        chk('친구 접속 정보는 읽힘',r=='ok',r)
        # 7) 요청 받지 않기
        await p2.evaluate("()=>window.__T.ev('closeSheet()')");await tab(p2,'pal');await p2.click('#tab-pal [data-k=fset]');await asyncio.sleep(0.3);await p2.click('#frSetReq');await asyncio.sleep(1)
        chk('요청 받지 않기 저장',STORE.get('on/'+u2,{}).get('nr') is True,STORE.get('on/'+u2))
        p4=await newpage(b,errs,'넷째');await asyncio.sleep(3);u4=await ev(p4,'SEAT')
        await ev(p4,f"frRequest('{u2}','하율')");await asyncio.sleep(1)
        chk('요청 받지 않는 사용자에게 요청 → 안내',('받지 않는 사용자' in await txt(p4,'#dlg')),await txt(p4,'#dlg'))
        await p4.click('[data-act=dlgok]')
        await p2.click('#frSetReq');await asyncio.sleep(0.8);await p2.evaluate("()=>window.__T.ev('closeSheet()')")
        # 8) 차단 → 요청·메시지·초대 거부
        await ev(p2,f"frBlock('{u1}','성민')");await asyncio.sleep(0.3);await p2.click('[data-act=dlgok]');await asyncio.sleep(1.2)
        chk('차단 → bk 생성·친구 문서 삭제',('bk/'+u2+'_'+u1 in STORE) and ('fp/'+pid not in STORE))
        await asyncio.sleep(0.5)
        chk('차단당한 쪽 목록에서 빠짐',('하율' not in await txt(p1,'#palFr')),await txt(p1,'#palFr'))
        d0=len(await den(p1))
        await ev(p1,f"frRequest('{u2}','하율')");await asyncio.sleep(1)
        chk('차단당한 쪽 요청 → 거부·같은 안내',('받지 않는 사용자' in await txt(p1,'#dlg')) and any('fp create' in x for x in (await den(p1))[d0:]),await txt(p1,'#dlg'))
        await p1.click('[data-act=dlgok]')
        a,bb=(u1,u2) if u1<u2 else (u2,u1)
        r=await ev(p1,f"""(async()=>{{try{{await db.doc('fp/{pid}').set({{a:'{a}',b:'{bb}',by:SEAT,st:'ok',tk:'x',at:SRV_TS,sa:SRV_TS,na:'',nb:'',m:[],q:0,ra:0,rb:0}});return 'ok'}}catch(e){{return 'denied'}}}})()""")
        chk('규칙: 차단당한 쪽 친구 문서 만들기 거부',r=='denied',r)
        r=await ev(p1,f"(async()=>{{try{{await db.doc('fp/{pid}').update({{m:[{{i:1,s:'a',t:'hi',a:Date.now()}}],q:1}});return 'ok'}}catch(e){{return 'denied'}}}})()")
        chk('규칙: 차단 후 메시지 거부',r=='denied',r)
        r=await ev(p1,f"(async()=>{{try{{await db.doc('bk/{u2}_{u1}').get();return 'ok'}}catch(e){{return 'denied'}}}})()")
        chk('규칙: 차단당한 쪽은 차단 문서 못 읽음',r=='denied',r)
        # 신고
        await ev(p3,f"frReport('{u1}','성민')");await asyncio.sleep(0.3)
        await p3.click('#dlg [data-act=frrep][data-v=abuse]');await asyncio.sleep(1)
        reps=[k for k in STORE if k.startswith('rep/')]
        chk('신고 저장',len(reps)==1 and STORE[reps[0]].get('why')=='abuse',reps)
        r=await ev(p3,"(async()=>{try{await db.collection('rep').get();return 'ok'}catch(e){return 'denied'}})()")
        chk('규칙: 관리자 아니면 신고 못 읽음',r=='denied',r)
        try: await p3.click('[data-act=dlgno]',timeout=800)
        except Exception: pass
        # 차단 해제 → 다시 요청 → 수락 → 친구 끊기
        await ev(p2,f"frUnblock('{u1}')");await asyncio.sleep(1)
        await ev(p1,f"frRequest('{u2}','하율')");await asyncio.sleep(1);await ev(p2,f"frAccept('{u1}')");await asyncio.sleep(1)
        chk('차단 해제 후 다시 친구',STORE.get('fp/'+pid,{}).get('st')=='ok')
        await ev(p1,f"frUnfriend('{u2}')");await asyncio.sleep(0.3);await p1.click('[data-act=dlgok]');await asyncio.sleep(1)
        chk('친구 끊기 → 문서 삭제','fp/'+pid not in STORE)
        # 9) 게스트
        p5=await newpage(b,errs,'게스트',google=False);await asyncio.sleep(3);await tab(p5,'pal')
        chk('게스트는 구글 연결 안내',('구글 계정을 연결하면' in await txt(p5,'#palGate')),await txt(p5,'#palGate'))
        r=await ev(p5,f"(async()=>{{const u='{u1}',a=SEAT<u?SEAT:u,b=SEAT<u?u:SEAT;try{{await db.doc('fp/'+frPid(SEAT,u)).set({{a,b,by:SEAT,st:'req',at:SRV_TS,sa:SRV_TS,na:'',nb:'',m:[],q:0,ra:0,rb:0}});return 'ok'}}catch(e){{return 'denied'}}}})()")
        chk('규칙: 게스트 요청 거부',r=='denied',r)
        # 닉네임 바꾸면 친구 문서 닉네임도
        await ev(p3,"(lset('bo-nick','세번째2'),syncNick(),frNickSync())");await asyncio.sleep(1.2)
        s13=STORE.get('fp/'+pid13,{});chk('닉네임 변경 → 친구 문서 반영','세번째2' in (s13.get('na'),s13.get('nb')),s13)
        print('denied p1',await den(p1));print('denied p2',await den(p2));print('denied p3',await den(p3))
        bad=[e for e in errs if 'TUNNEL' not in e and 'favicon' not in e]
        chk('콘솔 오류 0',not bad,bad[:6])
        await b.close()
    n=sum(1 for _,o in RES if o);print(f'\n결과 {n}/{len(RES)} 통과');
asyncio.run(main())
