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
async def main():
    errs=[]
    async with async_playwright() as pw:
        b=await pw.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
        a=await adminpage(b,errs);await asyncio.sleep(2);sa=await ev(a,'SEAT')
        st=STORE.get('cfg/start');chk('관리자가 cfg/start 기록',st and st.get('s',{}).get(sa)==1250,st)
        chk('관리자 시작 1250',await ev(a,f"rkStart('{sa}')")==1250,await ev(a,f"rkStart('{sa}')"))
        p=await newpage(b,errs,'일반');await asyncio.sleep(3)
        chk('다른 폰도 관리자 1250',await ev(p,f"rkStart('{sa}')")==1250)
        chk('일반 사용자 1000',await ev(p,"rkStart(SEAT)")==1000)
        r=await p.evaluate("async()=>{try{await window.__T.ev('db').doc('cfg/start').set({s:{x:3000},at:1});return 'ok'}catch(e){return 'denied'}}");chk('일반 사용자 쓰기 거부',r=='denied',r)
        chk('랭크 점검 해제',await ev(p,'RANK_MAINT')==False)
        top=await ev(p,"JSON.stringify(RK.list.filter(x=>x.bot).slice(0,3).map(x=>[x.nick,Math.round(x.r)]))");chk('AI 최고 1300 근처',json.loads(top)[0][1]<=1310,top)
        print('errors',[e for e in errs if 'ERR_' not in e]);print('RESULT',sum(1 for _,o in RES if o),'/',len(RES));await b.close()
asyncio.run(main())
