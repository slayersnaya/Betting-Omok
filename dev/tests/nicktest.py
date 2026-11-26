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
async def adminpage(b,errs):
    ctx=await b.new_context(viewport={'width':390,'height':844})
    await ctx.add_init_script("localStorage.setItem('bo-tut-done','1');localStorage.setItem('bo-rkintro','1');localStorage.setItem('bo-rklg','1');sessionStorage.setItem('bo-noatt','1');localStorage.setItem('bo-nick','관리');window.__fakeAdmin=true;sessionStorage.setItem('fake-g','1');if(sessionStorage.getItem('adm'))window.__fakeEmail=sessionStorage.getItem('adm')")
    async def route(rt): await rt.fulfill(path=FAKE[rt.request.url.split('/')[-1]],content_type='application/javascript')
    await ctx.route('https://www.gstatic.com/**',route)
    p=await ctx.new_page();p.on('pageerror',lambda e:errs.append('adm:'+str(e)))
    await p.expose_function('__fsSend',lambda j,p=p:asyncio.ensure_future(relay(p,j)));PAGES.append(p)
    await p.goto(f'http://127.0.0.1:{PORT}/index.html');await asyncio.sleep(1.5)
    await p.evaluate("()=>sessionStorage.setItem('adm',window.__T.ev('ADMIN_EMAILS[0]'))");await p.reload();await asyncio.sleep(3);return p
async def dlg(p): return await p.evaluate("()=>{const d=document.querySelector('#dlg');return d.classList.contains('hide')?'':d.innerText.replace(/\\s+/g,' ')}")
async def nk(p,v):
    await ev(p,"openSheet('nick')");await asyncio.sleep(0.3)
    c=await p.evaluate("()=>[document.querySelector('#nickCost').innerText.replace(/\\s+/g,' '),document.querySelector('#nickOk').innerText]")
    await p.fill('#nick',v);await p.click('#nickOk');await asyncio.sleep(0.6);return c
async def main():
    errs=[]
    async with async_playwright() as pw:
        b=await pw.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
        p=await newpage(b,errs,'성민');await asyncio.sleep(2.5);await ev(p,"goLobby()");u=await ev(p,'SEAT')
        g0=(await wal(u)).get('g')
        c=await nk(p,'원이짱');chk('시트: 첫 변경 무료 안내','첫 변경은 무료' in c[0] and '500' in c[0],c)
        d=await dlg(p);chk('확인창: 다음부터 옥돌 500',('다음부터는 옥돌 500' in d),d);await p.screenshot(path='/tmp/bt/nk1.png')
        await p.evaluate("()=>document.querySelector('#dlg [data-act=dlgok]').click()");await asyncio.sleep(1.5)
        w=await wal(u);chk('첫 변경: 무료 · nc 1',await ev(p,"lget('bo-nick')")=='원이짱' and w.get('nc')==1 and w.get('g')==g0,json.dumps(w)[:160])
        c=await nk(p,'둘째이름');chk('시트: 변경 옥돌 500','변경 옥돌 500' in c[0] and '500' in c[1],c);await p.screenshot(path='/tmp/bt/nk2.png')
        e=await p.evaluate("()=>document.querySelector('#nickErr').innerText");chk('옥돌 부족 막힘','필요해요' in e and await ev(p,"lget('bo-nick')")=='원이짱',e)
        w=await wal(u);w2=dict(w);w2.update({'g':600});await push('wal/'+u,w2);await reload_w(p);await ev(p,"closeSheet()")
        await nk(p,'둘째이름');d=await dlg(p);chk('확인창: 옥돌 500개가 들어요','옥돌 500개가 들어요' in d,d)
        await p.evaluate("()=>document.querySelector('#dlg [data-act=dlgok]').click()");await asyncio.sleep(1.5)
        w=await wal(u);chk('두 번째 변경: 옥돌 −500 · nc 2',await ev(p,"lget('bo-nick')")=='둘째이름' and w.get('nc')==2 and w.get('g')==100,json.dumps(w)[:160])
        r=await forge(p,"n.nc=3;n.k='nick'");chk('서버: 두 번째부터 공짜 변경 거부',r=='denied',r)
        r=await forge(p,"n.nc=5;n.g-=500;n.k='nick'");chk('서버: 횟수 건너뛰기 거부',r=='denied',r)
        r=await forge(p,"n.nc=0;n.k='equip'");chk('서버: 다른 쓰기로 횟수 되돌리기 거부',r=='denied',r)
        await ev(p,"closeSheet()");c=await nk(p,'둘째이름 ');d=await dlg(p);ww=await wal(u);chk('같은 이름(공백만 다름)은 확인창 없이 무료',d=='' and ww.get('nc')==2,[d,ww.get('nc'),await ev(p,'shOpen')])
        print('errors',[e for e in errs if 'ERR_' not in e]);print('RESULT',sum(1 for _,o in RES if o),'/',len(RES));await b.close()
asyncio.run(main())
