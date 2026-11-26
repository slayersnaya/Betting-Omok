import asyncio,json,threading,http.server,socketserver,functools,time
from playwright.async_api import async_playwright
PORT=8765
class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self,*a):pass
def serve():
    socketserver.TCPServer.allow_reuse_address=True
    with socketserver.TCPServer(('127.0.0.1',PORT),functools.partial(Q,directory=__import__('os').environ.get('WEBDIR','/home/claude/web'))) as s:s.serve_forever()
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
async def newpage(b,errs,name):
    ctx=await b.new_context(viewport={'width':390,'height':844})
    await ctx.add_init_script("localStorage.setItem('bo-tut-done','1');localStorage.setItem('bo-rkintro','1');localStorage.setItem('bo-rklg','1');sessionStorage.setItem('bo-noatt','1');localStorage.setItem('bo-airec',JSON.stringify({pro:{w:1,l:0,d:0}}))")
    async def route(rt): await rt.fulfill(path=FAKE[rt.request.url.split('/')[-1]],content_type='application/javascript')
    await ctx.route('https://www.gstatic.com/**',route)
    p=await ctx.new_page();p.on('pageerror',lambda e:errs.append(name+':'+str(e)))
    p.on('console',lambda m:errs.append(name+' console:'+m.text) if m.type=='error' else None)
    await p.expose_function('__fsSend',lambda j,p=p:asyncio.ensure_future(relay(p,j)))
    PAGES.append(p);await p.goto(f'http://127.0.0.1:{PORT}/index.html')
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

async def play_bot(p,turns=40):
    """사람 쪽: 선이면 아무 데나 확정, 베팅은 첫 칸에 몰아 걸기. 끝날 때까지"""
    for _ in range(turns*30):
        await asyncio.sleep(0.25)
        try: await p.click('#coin',timeout=200)
        except Exception: pass
        st=await p.evaluate("()=>__T.L.s?__T.L.s.phase:''")
        if st=='over': return True
        if await p.locator('[data-act=dconfirm]').count():
            await p.evaluate("()=>{const c=__T.legalTriples(__T.L.s.bd)[0];__T.L.s.cells=c;__T.L.startBet();__T.renderAll()}")
        elif await p.locator('#bsub').count():
            await p.evaluate("()=>{__T.UI.bet=[Math.max(1,__T.L.s.pts.A-2),1,1];__T.L.submit()}")
    return False
async def main():
    errs=[]
    async with async_playwright() as pw:
        b=await pw.chromium.launch()
        p=await newpage(b,errs,'성민')
        await p.evaluate("()=>{sessionStorage.setItem('fake-g','1')}")
        await p.reload();await asyncio.sleep(1.5)
        await p.evaluate("n=>{document.querySelector('#nick').value=n}",'성민')
        print('acct',await txt(p,'#acct'))
        print('tabs',await txt(p,'.tabbar:not(.tbw)'),'lock?',await p.evaluate("()=>document.querySelector('.tabbar [data-k=rank]').className"))
        await p.evaluate("()=>document.querySelector('.tabbar:not(.tbw) [data-k=rank]').click()");await asyncio.sleep(0.3)
        print('pod',await txt(p,'#rkPod'))
        r0=await p.evaluate("()=>Math.round((__T.RK.map.get(__T.seat())||{r:1000}).r)")
        await p.click('#mmBtn');await asyncio.sleep(0.5);print('mm',await txt(p,'#mmSt'))
        await p.evaluate("()=>{__T.MM.botAt=Date.now()}");ok=await waitfor(lambda: ingame(p),60)
        print('bot game',ok,await txt(p,'#gttl'),'|',await txt(p,'#oppbar'),'| lv',await p.evaluate("()=>__T.L.s.ai+' '+__T.L.s.bot.nick+' '+__T.L.s.bot.r"))
        t0=time.time();done=await play_bot(p);print('over',done,round(time.time()-t0,1),'s',await txt(p,'#panel'))
        await asyncio.sleep(1.5)
        print('bres',[ (k,STORE[k]['w']) for k in STORE if k.startswith('bres/')])
        await p.click('[data-act=lobby]');await asyncio.sleep(1)
        r1=await p.evaluate("()=>{__T.rankCompute();return Math.round((__T.RK.map.get(__T.seat())||{r:1000}).r)+' g'+(__T.RK.map.get(__T.seat())||{}).g}")
        print('rating',r0,'->',r1,'| tab',await p.evaluate("()=>__T.UI.tab"))
        print('archive',await txt(p,'#archive'))
        # 중간에 나가면 기권패
        await p.click('#mmBtn');await asyncio.sleep(0.3);await p.evaluate("()=>{__T.MM.botAt=Date.now()}");await waitfor(lambda: ingame(p),60)
        await asyncio.sleep(3);await p.click('[data-act=lobby]');await asyncio.sleep(0.3);print('leave dlg',await txt(p,'#dlg'));await p.click('[data-act=dlgok]');await asyncio.sleep(1.5)
        print('bres2',[ (k,STORE[k]['w'],STORE[k]['why']) for k in STORE if k.startswith('bres/')])
        # 앱을 닫으면(새로고침) 패
        await p.click('#mmBtn');await asyncio.sleep(0.3);await p.evaluate("()=>{__T.MM.botAt=Date.now()}");await waitfor(lambda: ingame(p),60)
        await asyncio.sleep(2);await p.reload();await asyncio.sleep(4)
        print('bres3',[ (k,STORE[k]['w'],STORE[k]['why']) for k in STORE if k.startswith('bres/')])
        # 관리자 마스터
        p2=await newpage(b,errs,'admin')
        await p2.evaluate("()=>{sessionStorage.setItem('fake-g','1')}")
        await p2.add_init_script("window.__fakeEmail='slayersnaya@gmail.com';window.__fakeAdmin=true")
        await p2.reload();await asyncio.sleep(3)
        print('cfg',STORE.get('cfg/master'))
        print('admin rating',await p2.evaluate("()=>{const p=__T.RK.map.get(__T.seat());return p&&Math.round(p.r)+' '+(__T.tierOf(p)||{}).n}"),'| p1 sees',await p.evaluate("()=>{const s=(__T.RK.master||[])[0];const q=s&&__T.RK.map.get(s);return q&&Math.round(q.r)}"))
        print('denied',await p.evaluate("()=>window.__deniedList||[]"),await p2.evaluate("()=>window.__deniedList||[]"))
        print('errors',[e for e in errs if 'TUNNEL' not in e][:10]);await b.close()
asyncio.run(main())
