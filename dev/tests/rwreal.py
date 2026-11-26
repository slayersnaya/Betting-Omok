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
        p=await newpage(b,errs,'성민',google=True) if 'google' in newpage.__code__.co_varnames else await newpage(b,errs,'성민')
        await asyncio.sleep(2.5)
        u=await ev(p,'SEAT');w0=await wal(u);print('wal0',json.dumps(w0)[:200] if w0 else None)
        await aigame(p,'beginner',True);await aigame(p,'mid',True);await asyncio.sleep(1.5)
        await ev(p,"goLobby()");await asyncio.sleep(0.5)
        print('count',await ev(p,'ecoRewardCount()'),'| bar:',await p.evaluate("()=>{const e=document.querySelector('#rwBar');return e.classList.contains('hide')?'(hidden)':e.innerText.replace(/\\s+/g,' ')}"))
        g1=(await wal(u) or {}).get('g');cl1=(await wal(u) or {}).get('cl')
        await p.screenshot(path='/tmp/bt/rw_before.png')
        await p.evaluate("()=>{const b=[...document.querySelectorAll('#rwBar button')].find(x=>/받기/.test(x.innerText));b&&b.click()}");await asyncio.sleep(2.5)
        w2=await wal(u) or {};print('g',g1,'->',w2.get('g'),'| cl',cl1,'->',w2.get('cl'))
        print('count after',await ev(p,'ecoRewardCount()'),'| bar:',await p.evaluate("()=>{const e=document.querySelector('#rwBar');return e.classList.contains('hide')?'(hidden)':e.innerText.replace(/\\s+/g,' ')}"))
        await p.screenshot(path='/tmp/bt/rw_after.png')
        print('denied',DENIED if 'DENIED' in globals() else '-','errors',[e for e in errs if 'ERR_' not in e]);await b.close()
asyncio.run(main())
