# 디자인팀 2차: 새 메뉴 전체 스크린샷 + 줄바꿈·잘림 자동 점검(eval/ux/audit.js)
# 사용: OUT=/home/claude/eval/gd2/shots/after WEBDIR=/home/claude/eval/gd2/web python3 gshots.py [ph s360 pc w1024 fhd light]
import asyncio, os, sys, json, time
os.environ.setdefault('WEBDIR','/home/claude/eval/gd2/web')
src=open('/home/claude/eval/friend/friendtest.py').read().split('# ===== 친구 기능 시나리오')[0].replace('"8791"','"'+os.environ.get('GPORT','8833')+'"')
exec(src)
OUT=os.environ.get('OUT','/home/claude/eval/gd2/shots/after');os.makedirs(OUT,exist_ok=True)
AUDIT=open('/home/claude/eval/ux/audit.js').read();RESULTS={};ERRS=[]
ME='uMe00000000000000001';NOW=int(time.time()*1000)
F={'uF1aaaaaaaaaaaaaaaa1':'하율','uF2aaaaaaaaaaaaaaaa2':'새벽감자','uF3aaaaaaaaaaaaaaaa3':'mint_22','uF4aaaaaaaaaaaaaaaa4':'haru','uF5aaaaaaaaaaaaaaaa5':'오목초보'}
def pid(x,y): return x+'_'+y if x<y else y+'_'+x
def pair(u,nk,st='ok',by=None,m=None,extra=None):
    a,b=sorted([ME,u]);d={'a':a,'b':b,'by':by or u,'st':st,'at':NOW-864e5*3,'sa':NOW-864e5*2,'na':'성민' if a==ME else nk,'nb':'성민' if b==ME else nk,'m':m or [],'q':len(m or []),'ra':0,'rb':0}
    if extra: d.update(extra)
    return d
def seed():
    STORE.clear();me_s='a';o='b'
    t=NOW-40*60e3;msgs=[]
    conv=[(o,'오늘 저녁에 한 판?'),(me_s,'좋아요 9시쯤 어때요'),(o,'콜'),(o,'지난번 C칸에 몰아 건 거 진짜 놀랐어요'),(me_s,'그거 운이었어요 😂'),(o,'👍'),(me_s,'오늘은 제가 이길게요')]
    for i,(s,tx) in enumerate(conv,1):
        x={'i':i,'s':s,'t':tx,'a':int(t+i*90e3)}
        if tx=='👍': x['e']=5
        msgs.append(x)
    msgs.append({'i':8,'s':me_s,'t':'대국 신청','a':int(NOW-5*60e3),'k':'inv'});msgs.append({'i':9,'s':o,'t':'수락','a':int(NOW-4.8*60e3),'k':'acc'})
    msgs.append({'i':10,'s':o,'t':'한 판 더 해요','a':int(NOW-60e3)});msgs.append({'i':11,'s':o,'t':'이번엔 무제한으로','a':int(NOW-50e3)})
    STORE['fp/'+pid(ME,'uF1aaaaaaaaaaaaaaaa1')]=pair('uF1aaaaaaaaaaaaaaaa1','하율',m=msgs,extra={'ra':9,'rb':7})
    STORE['fp/'+pid(ME,'uF2aaaaaaaaaaaaaaaa2')]=pair('uF2aaaaaaaaaaaaaaaa2','새벽감자',m=[{'i':1,'s':'b','t':'ㅎㅇ','a':NOW-864e5}],extra={'ra':0,'rb':1})
    STORE['fp/'+pid(ME,'uF3aaaaaaaaaaaaaaaa3')]=pair('uF3aaaaaaaaaaaaaaaa3','mint_22')
    STORE['fp/'+pid(ME,'uF4aaaaaaaaaaaaaaaa4')]=pair('uF4aaaaaaaaaaaaaaaa4','haru')
    STORE['fp/'+pid(ME,'uF5aaaaaaaaaaaaaaaa5')]=pair('uF5aaaaaaaaaaaaaaaa5','오목초보')
    STORE['fp/'+pid(ME,'uR1aaaaaaaaaaaaaaaa6')]=pair('uR1aaaaaaaaaaaaaaaa6','luna07',st='req',by='uR1aaaaaaaaaaaaaaaa6')
    STORE['fp/'+pid(ME,'uR2aaaaaaaaaaaaaaaa7')]=pair('uR2aaaaaaaaaaaaaaaa7','teo_9',st='req',by=ME)
    STORE['on/uF1aaaaaaaaaaaaaaaa1']={'at':NOW-60e3,'st':'on'};STORE['on/uF2aaaaaaaaaaaaaaaa2']={'at':NOW-120e3,'st':'g'}
    STORE['on/uF3aaaaaaaaaaaaaaaa3']={'at':NOW-2*3600e3,'st':'off'};STORE['on/uF4aaaaaaaaaaaaaaaa4']={'at':NOW-26*3600e3,'st':'off'};STORE['on/uF5aaaaaaaaaaaaaaaa5']={'at':NOW,'st':'off','hs':True}
    STORE[f'on/{ME}']={'at':NOW,'st':'on','fc':'K7QM2XPA'};STORE['fc/K7QM2XPA']={'by':ME,'n':'성민'}
    for u,n in list(F.items())+[('uR1aaaaaaaaaaaaaaaa6','luna07'),('uR2aaaaaaaaaaaaaaaa7','teo_9'),('uS1aaaaaaaaaaaaaaaa8','오목장인99'),('uS2aaaaaaaaaaaaaaaa9','오목왕자')]:
        key='n'+n.lower().encode().hex();STORE['nicks/'+key]={'by':u,'g':True,'at':NOW,'n':n}
RKP="""(()=>{const rc=rankCompute,X={uF1aaaaaaaaaaaaaaaa1:[1342,24,15,8,1,3,0],uF2aaaaaaaaaaaaaaaa2:[1121,12,7,5,0,0,2],uF3aaaaaaaaaaaaaaaa3:[958,9,4,5,0,0,1],uF4aaaaaaaaaaaaaaaa4:[1000,2,1,1,0,1,0],uR1aaaaaaaaaaaaaaaa6:[1544,40,28,11,1,0,0],uS1aaaaaaaaaaaaaaaa8:[1188,15,9,6,0,2,0],uMe00000000000000001:[1236,18,11,7,0,2,0]};
 rankCompute=function(){rc();for(const [s,[r,g,w,l,d,ws,ls]] of Object.entries(X)){const p={seat:s,nick:'',r,g,w,l,d,ws,ls,t:0};RK.map.set(s,p)}RK.list=[...RK.map.values()].filter(p=>p.g>=PLACE).sort((x,y)=>y.r-x.r||x.seat.localeCompare(y.seat))};
 rankCompute();renderRank();frRender();return 1})()"""
GAMES="""()=>{const H=(t,sun,a,b,w)=>({t,sun,cells:[[9,8+t%3],[9,9+t%3],[9,10+t%3]],win:w,bets:{a,b}});
const g=(w,l,t,first)=>({key:'k'+l+t,label:l,at:Date.now()-t*60e3,d:{A:'a',B:'b',me:'a',names:{a:'나',b:l},winner:w,reason:'오목',
 hist:[H(1,first?'a':'b',[4,3,3],[3,3,4],['a','a','b']),H(2,first?'b':'a',[1,1,1],[5,2,3],['b','b','b']),H(3,first?'a':'b',[2,6,2],[4,4,4],['b','a','b']),H(4,first?'b':'a',[3,3,8],[6,6,2],['b','b','a'])]}});
localStorage.setItem('bo-games',JSON.stringify([g('a','AI 고수',3,1),g('b','새벽감자',9,0),g('a','랭크 게임 · Dodo2',20,1),g(null,'한 폰',40,0),g('a','AI 중수',60,1),g('b','랭크 게임 · Teo9',90,0),g('b','AI 고수',120,1)]));return 1}"""
ROOMS="""lobbyRooms=[{id:'g1a2b3c4d',host:'x1',hostNick:'새벽감자',guest:null,guestNick:'',created:Date.now()-120e3,td:20,tb:30,status:'open',ranked:false},
{id:'g2a2b3c4d',host:'x2',hostNick:'민트초코',guest:null,guestNick:'',created:Date.now()-600e3,td:0,tb:0,status:'open',ranked:false}];lobbyState='ok';renderRooms()"""
RECAP="recapShow({n:1,start:Date.UTC(2026,8,1),end:Date.UTC(2026,11,1),r:1388,g:42,w:25,l:16,d:1,ix:3,rank:12,best:6,top:{nk:'새벽감자',n:7},next:1150})"
ADMR="""(()=>{const n=Date.now();ADM.rows=[{id:'uMe00000000000000001',at:n-1e4,pv:'g',nk:'성민',v:''},{id:'uF1aaaaaaaaaaaaaaaa1',at:n-2e5,pv:'g',nk:'하율',v:''},{id:'uF2aaaaaaaaaaaaaaaa2',at:n-36e5,pv:'e',nk:'새벽감자',v:''},{id:'uX3',at:n-5e6,pv:'n',nk:'',v:''},{id:'uX4',at:n-9e7,pv:'n',nk:'긴닉네임열두글자까지',v:''},{id:'uF3aaaaaaaaaaaaaaaa3',at:n-3e8,pv:'g',nk:'mint_22',v:''}];ADM.flt=ADM.flt||'all';openSheet('adm');admRender();return 1})()"""
async def ctxpage(b,w,h,theme='dark',google=True,name='성민',uid=ME,games=True):
    ctx=await b.new_context(viewport={'width':w,'height':h},device_scale_factor=1 if w>1500 else 2,has_touch=w<600,is_mobile=w<600)
    init=("sessionStorage.setItem('fake-g','1');" if google else "")+f"sessionStorage.setItem('fake-uid','{uid}');localStorage.setItem('bo-nick','{name}');localStorage.setItem('bo-tut-done','1');localStorage.setItem('bo-rkintro','1');sessionStorage.setItem('bo-noatt','1');localStorage.setItem('bo-airec',JSON.stringify({{pro:{{w:1,l:0,d:0}}}}));"+("localStorage.setItem('bo-theme','light');" if theme=='light' else "")
    await ctx.add_init_script("sessionStorage.setItem('bo-noatt','1');if(!sessionStorage.getItem('__i')){sessionStorage.setItem('__i','1');"+init+"}else{"+("sessionStorage.setItem('fake-g','1');" if google else "")+"}")
    async def route(rt): await rt.fulfill(path=FAKE[rt.request.url.split('/')[-1]],content_type='application/javascript')
    await ctx.route('https://www.gstatic.com/**',route);await ctx.route('https://cdn.jsdelivr.net/**',lambda rt:rt.abort());await ctx.route('https://hangeul.pstatic.net/**',lambda rt:rt.abort())
    p=await ctx.new_page();p.on('pageerror',lambda e:ERRS.append(str(e)));p.on('console',lambda m:ERRS.append('console:'+m.text) if m.type=='error' else None)
    await p.expose_function('__fsSend',lambda j,p=p:asyncio.ensure_future(relay(p,j)));PAGES.append(p)
    await p.goto(f'http://127.0.0.1:{PORT}/index.html');await p.wait_for_timeout(1500)
    if games: await p.evaluate(GAMES);await p.reload();await p.wait_for_timeout(2600)
    if google: await p.evaluate("c=>window.__T.ev(c)",RKP)
    await p.evaluate("c=>window.__T.ev(c)",ROOMS)
    return ctx,p
async def shot(p,name,full=False):
    await p.wait_for_timeout(500);await p.screenshot(path=f'{OUT}/{name}.png',full_page=full)
    r=await p.evaluate(AUDIT);RESULTS[name]=r;fl=[]
    if r.get('sw',0)>r.get('w',0):fl.append(f"HSCROLL {r['sw']}>{r['w']}")
    for k in ('orphans','split','clip','offR'):
        if r.get(k):fl.append(f'{k}:{len(r[k])}')
    print(name,' '.join(fl),flush=True)
async def tab(p,k): await p.evaluate(f"()=>[...document.querySelectorAll('.tabbar [data-k={k}]')].find(b=>b.offsetParent).click()");await p.wait_for_timeout(500)
async def ev(p,c): return await p.evaluate("c=>window.__T.ev(c)",c)
async def closeall(p): await p.evaluate("()=>{const d=document.querySelector('#dlg');if(!d.classList.contains('hide'))window.__T.ev('dialogClose()');window.__T.ev('closeSheet()');window.__T.ev('recapClose()');const t=document.querySelector('#tup');if(t){t.remove();window.__T.ev('TUPC.el=null')}}");await p.wait_for_timeout(250)
async def has(p,sel): return await p.evaluate(f"()=>!!document.querySelector('{sel}')")
async def scene_all(b,tag,w,h,th):
    seed();ctx,p=await ctxpage(b,w,h,th);n=f'{tag}_{th}';ph=w<600
    await ev(p,"lrm('bo-pz')");await ev(p,"renderPzTile();typeof rwPaint==='function'&&rwPaint()")
    await shot(p,n+'_home',full=ph)
    await tab(p,'rank');await shot(p,n+'_rank',full=ph)
    await tab(p,'pal');await shot(p,n+'_pal',full=ph)
    if await has(p,'#sh-fadd'):
        await ev(p,"openSheet('fadd')");await shot(p,n+'_fadd')
        await p.fill('#palQ','오목');await p.wait_for_timeout(1300);await shot(p,n+'_fadd_search');await p.fill('#palQ','');await closeall(p)
        await ev(p,"openSheet('fset')");await shot(p,n+'_fset');await closeall(p)
    else:
        await p.fill('#palQ','오목');await p.wait_for_timeout(1300);await shot(p,n+'_pal_search');await p.fill('#palQ','')
    await ev(p,"frOpenProf('uF1aaaaaaaaaaaaaaaa1')");await shot(p,n+'_prof')
    await closeall(p);await ev(p,"frOpenProf('uR1aaaaaaaaaaaaaaaa6')");await shot(p,n+'_prof_req')
    await closeall(p);await ev(p,"frOpenChat('uF1aaaaaaaaaaaaaaaa1')");await shot(p,n+'_chat')
    await closeall(p);await tab(p,'home');await ev(p,"pzOpen()");await shot(p,n+'_puz')
    await ev(p,"(()=>{const pz=pzMake(fxDate(Date.now()));pzRecord(false,pz.type==='pick'?(pz.ans+1)%4:[1,1,1]);renderPz();renderPzTile();typeof rwPaint==='function'&&rwPaint()})()");await shot(p,n+'_puz_done')
    await closeall(p);await shot(p,n+'_home_pzdone')
    await tab(p,'rec');await p.evaluate("()=>document.querySelector('#anaCard').scrollIntoView({block:'start'})");await shot(p,n+'_ana')
    await closeall(p);await ev(p,RECAP);await shot(p,n+'_recap')
    await closeall(p);await ev(p,"tupShow(TIERS[2],TIERS[3])");await p.wait_for_timeout(3500);await shot(p,n+'_tup')
    await closeall(p);await ev(p,"tupShow(TIERS[TIERS.length-1],CHAL)");await p.wait_for_timeout(4000);await shot(p,n+'_chal')
    await closeall(p);await ev(p,"openSheet('acc')");await shot(p,n+'_acc')
    await closeall(p);await ev(p,ADMR);await shot(p,n+'_adm')
    await closeall(p)
    # 복기 AI 비교(지난 대국 복기)
    await tab(p,'rec');await p.evaluate("()=>document.querySelector('#archive [data-act=arc]').click()");await p.wait_for_timeout(4500);await shot(p,n+'_rvai')
    # 대국 이모트
    await ev(p,"(()=>{const x=BOTS[7];closeSheet();goLobby();UI.mode='local';L.start('A',x.lv,{bot:{id:x.id,nick:x.nick,r:x.base}});show('game');renderAll()})()")
    await p.wait_for_timeout(1500)
    try: await p.click('#coin',timeout=600)
    except Exception: pass
    await p.wait_for_timeout(900);await ev(p,"emoPick(true)");await shot(p,n+'_emo')
    await ev(p,"emoPick(false)");await ev(p,"emoShow(L.s&&'B'||'B',2,false)");await p.wait_for_timeout(600);await shot(p,n+'_emo_show')
    await ctx.close()
async def main():
    async with async_playwright() as pw:
        b=await pw.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
        sizes=[('ph',390,844,'dark'),('ph',390,844,'light'),('s360',360,740,'dark'),('pc',1280,800,'dark'),('w1024',1024,768,'dark'),('fhd',1920,1080,'dark')]
        only=sys.argv[1:]
        for tag,w,h,th in sizes:
            k=tag if th=='dark' else 'light'
            if only and k not in only: continue
            try: await scene_all(b,tag,w,h,th)
            except Exception as e: print('SCENE FAIL',tag,th,e)
        if not only or 'guest' in only:
            seed();ctx,p=await ctxpage(b,390,844,google=False,uid='uGuest00000000000001',name='손님',games=False);await tab(p,'pal');await shot(p,'ph_dark_guest');await ctx.close()
        json.dump(RESULTS,open(OUT+'/audit.json','w'),ensure_ascii=False,indent=1)
        print('errors',[e for e in ERRS if 'TUNNEL' not in e and 'ERR_' not in e][:10]);await b.close()
asyncio.run(main())
