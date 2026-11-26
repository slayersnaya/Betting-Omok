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
        p3=await page(b,errs,'지수',(360,740));await asyncio.sleep(3)
        await ev(p3,"(setTab('rank'),0)")
        ok=await waitfor(lambda: ev(p3,"lxItems(Date.now()).some(x=>x.g)"),300)
        bk=await ev(p3,"(lxItems(Date.now()).find(x=>x.g)||{}).k");await ev(p3,"(LX.more=true,lxRender(),0)");await asyncio.sleep(.3)
        await p3.click(f'[data-act=lxwatch][data-k="{bk}"]')
        await waitfor(lambda: ev(p3,"!!(G.watch&&G.watch.rl)"),100);await asyncio.sleep(1)
        h=await ev(p3,"vstate().hist.length");print('hist now',h)
        await ev(p3,"(window.__wsFast=false,G.watch.shown=Math.max(0,G.watch.shown-2),clearTimeout(G.watch.tm),G.watch.tm=null,G.watch.stg=null,wStep(),0)")
        seq=[]
        for i in range(60):
            r=await p3.evaluate("()=>{const v=window.__T.ev('vstate()');return [v.hist.length,v.phase,!!document.querySelector('#panel .rvcards'),document.querySelectorAll('#panel .rvcards .wbp').length]}")
            seq.append(r);await asyncio.sleep(.2)
        prev=None
        for i,r in enumerate(seq):
            if r!=prev:print(f'{i*0.2:.1f}s',r);prev=r
        print('errors',errs);await b.close()
asyncio.run(main())
