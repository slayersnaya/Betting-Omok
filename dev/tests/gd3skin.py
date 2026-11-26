# 돌 무늬·판 테마 공개 시험(두 폰): A가 자개 돌·청자 판, B가 비취 돌 → 양쪽 화면에서 각자 돌에 각자 무늬, 판은 같은 것
import asyncio, os, json, time
os.environ.setdefault('WEBDIR','/home/claude/eval/gd3/web');os.environ.setdefault('FPORT','8873')
src=open('/home/claude/eval/friend/friendtest.py').read().split('# ===== 친구 기능 시나리오')[0]
exec(src)
RES=[]
def chk(name,ok,info=''):
    RES.append((name,bool(ok)));print(('PASS ' if ok else 'FAIL ')+name+(' | '+str(info)[:220] if info!='' else ''),flush=True)
async def ev(p,c): return await p.evaluate("c=>window.__T.ev(c)",c)
async def wal(u): return STORE.get('wal/'+u)
async def push(path,d):
    STORE[path]=d
    for p in PAGES: await send(p,json.dumps({'t':'w','op':'set','p':path,'d':d}))
async def reload_w(p):
    await p.evaluate("()=>window.__T.ev(`(async()=>{const x=await db.doc('wal/'+SEAT).get();ECO.w=ecoNorm(x.data());ecoLook();ecoPaint();ecoSyncPub()})()`)");await asyncio.sleep(0.5)
LOOK="""()=>{const T=window.__T,vs=T.ev('vstate()');if(!vs)return null;const o={};T.ev('ecoBoardLook')(o,vs);
 const bd=Array.from({length:19},()=>Array(19).fill(0));bd[9][9]=1;bd[9][10]=2;const svg=T.ev('boardSVG')(bd,o);
 return {A:vs.A,B:vs.B,skB:o.skB,skW:o.skW,cls:document.querySelector('#board').getAttribute('class')||'',useB:(svg.match(/#sB[_a-z0-9]*/)||[''])[0],useW:(svg.match(/#sW[_a-z0-9]*/)||[''])[0],gid:T.ev('G.gid')}}"""
async def main():
    errs=[]
    async with async_playwright() as pw:
        b=await pw.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
        p1=await newpage(b,errs,'성민');p2=await newpage(b,errs,'하율');await asyncio.sleep(3.5)
        u1=await ev(p1,'SEAT');u2=await ev(p2,'SEAT')
        w=dict(await wal(u1));w.update({'own':['w1','b1','t2'],'eq':{'w':'w1','b':'b1','t':'t2'}});await push('wal/'+u1,w);await reload_w(p1)
        w=dict(await wal(u2));w.update({'own':['w2'],'eq':{'w':'w2'}});await push('wal/'+u2,w);await reload_w(p2)
        pe1=await ev(p1,'ecoPe()');chk('공개 장착 문자열에 돌·판 포함',set(pe1.split('.'))>={'w1','b1','t2'},pe1)
        chk('상점 설명: 돌·판 양쪽 화면',await ev(p1,"ECO_SEE.w+'|'+ECO_SEE.b")=='양쪽 화면 내 돌에 보여요|양쪽 화면 판에 보여요')
        # 규칙: 돌·판이 든 공개 문자열을 대국 접속에 싣기(보유) 허용 · 없는 것 거부
        r=await p2.evaluate("""()=>new Promise(res=>{const T=window.__T,db=T.ev('db'),S=T.ev('SEAT');db.doc('on/'+S).set({at:{__st:1},st:'on',eq:'w2'},{merge:true}).then(()=>res('ok'),()=>res('denied'))})""")
        chk('규칙: 보유한 돌 무늬 공개 허용',r=='ok',r)
        r=await p2.evaluate("""()=>new Promise(res=>{const T=window.__T,db=T.ev('db'),S=T.ev('SEAT');db.doc('on/'+S).set({at:{__st:1},st:'on',eq:'w2.b1'},{merge:true}).then(()=>res('ok'),()=>res('denied'))})""")
        chk('규칙: 없는 판 테마 공개 거부',r=='denied',r)
        # 일반 게임 방: 성민이 만들고 하율이 코드로 입장
        await ev(p1,"dialogClose();closeSheet();setTab('home')");await ev(p2,"dialogClose();closeSheet();setTab('home')");await asyncio.sleep(0.3)
        await p1.click('#gameCard [data-act=sheet][data-k=friend]');await asyncio.sleep(0.3);await p1.click('#createBtn');await asyncio.sleep(1.5)
        gid=await ev(p1,'G.gid');await p2.click('#gameCard [data-act=sheet][data-k=friend][data-v=code]');await asyncio.sleep(0.3)
        await p2.fill('#roomCode',gid[1:]);await p2.click('#joinBtn');await asyncio.sleep(1.5)
        try: await p2.click('[data-act=join]',timeout=5000)
        except Exception as e: print('join btn',e)
        await asyncio.sleep(3)
        for p in PAGES:
            try: await p.click('#coin',timeout=500)
            except Exception: pass
        await asyncio.sleep(2.5)
        L1=await p1.evaluate(LOOK);L2=await p2.evaluate(LOOK);print('p1',L1);print('p2',L2)
        def want(L):
            sk={u1:'_w1',u2:'_w2'};return sk.get(L['A']),sk.get(L['B'])
        if L1 and L2:
            b1,w1=want(L1)
            chk('성민 화면: 흑·백 돌 각자 무늬',L1['skB']==b1 and L1['skW']==w1 and L1['useB']=='#sB'+b1 and L1['useW']=='#sW'+w1,L1)
            chk('하율 화면: 흑·백 돌 각자 무늬(상대 무늬 보임)',L2['skB']==b1 and L2['skW']==w1 and L2['useB']=='#sB'+b1 and L2['useW']=='#sW'+w1,L2)
            chk('판 테마: 한 사람만 장착 → 두 화면 모두 청자 판','bt-b1' in L1['cls'] and 'bt-b1' in L2['cls'],(L1['cls'],L2['cls']))
            await p2.evaluate("""()=>{const T=window.__T,vs=T.ev('vstate()'),o={};T.ev('ecoBoardLook')(o,vs);const bd=Array.from({length:19},()=>Array(19).fill(0));[[9,9],[8,10],[10,8],[7,11]].forEach(([r,c])=>bd[r][c]=1);[[9,10],[8,9],[10,10],[9,8]].forEach(([r,c])=>bd[r][c]=2);document.querySelector('#bov').innerHTML=T.ev('boardSVG')(bd,o)}""")
            await p2.screenshot(path='/home/claude/eval/gd3/shots/after/t_skin_p2_board.png')
            # 둘 다 판 장착: 하율이 흰 비자 판 → 대국 번호로 고른 한 사람 것을 두 화면이 똑같이
            w=dict(await wal(u2));w.update({'own':['w2','b2'],'eq':{'w':'w2','b':'b2'}});await push('wal/'+u2,w);await reload_w(p2);await asyncio.sleep(2.5)
            L1=await p1.evaluate(LOOK);L2=await p2.evaluate(LOOK)
            pick=await ev(p1,f"ecoBoardPick(cosOf(vstate().A).b,cosOf(vstate().B).b,G.gid)")
            same=[c for c in ('bt-b1','bt-b2') if c in L1['cls']]==[c for c in ('bt-b1','bt-b2') if c in L2['cls']]
            chk('판 테마: 둘 다 장착 → 두 화면 같은 판(대국 번호로 한 사람)',same and ('bt-'+pick) in L1['cls'],(pick,L1['cls'],L2['cls']))
            ok=True
            for g in ['g1a2b3c4d','gffffffff','g00000000']: ok=ok and (await ev(p1,f"ecoBoardPick('b1','b2','{g}')"))==(await ev(p2,f"ecoBoardPick('b1','b2','{g}')"))
            picks=[await ev(p1,f"ecoBoardPick('b1','b2','g{i:08x}')") for i in range(40)]
            chk('판 고르기: 두 폰 같은 답 · 판마다 반반에 가까움',ok and 10<=picks.count('b1')<=30,picks.count('b1'))
        else: chk('대국 화면 열림',False,(L1,L2))
        # AI 대국: 내 돌(흑)만 내 무늬, AI 돌은 기본
        await ev(p1,"(()=>{leaveGame();UI.mode='local';L.start('A','mid');show('game');renderAll()})()");await asyncio.sleep(1)
        La=await p1.evaluate(LOOK);chk('AI 대국: 내 돌만 내 무늬·내 판',La and La['skB']=='_w1' and La['skW']=='' and 'bt-b1' in La['cls'],La)
        bad=[e for e in errs if 'denied' not in e and 'permission' not in e.lower() and 'ERR_' not in e and 'Failed to load resource' not in e]
        chk('콘솔 오류 0',not bad,bad[:4])
        print(f'== {sum(o for _,o in RES)}/{len(RES)} PASS');await b.close()
asyncio.run(main())
