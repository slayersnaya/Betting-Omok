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
async def main():
    errs=[]
    async with async_playwright() as pw:
        b=await pw.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
        p1=await newpage(b,errs,'성민');p2=await newpage(b,errs,'하율')
        await asyncio.sleep(2)
        print('fbmode',await p1.evaluate("()=>document.body.classList.contains('fbmode')"),await p2.evaluate("()=>document.body.classList.contains('fbmode')"))
        # 친구 대국
        await p1.click('[data-act=sheet][data-k=friend]');await asyncio.sleep(0.3)
        print('online note p1:',await txt(p1,'#onlineNote'))
        await p1.click('#createBtn');await asyncio.sleep(1.5)
        print('p1 after create ingame',await ingame(p1),await txt(p1,'#panel'))
        print('DENIED',await p1.evaluate("()=>window.__deniedList||[]"),errs[:5])
        await p2.click('[data-act=sheet][data-k=friend]');await asyncio.sleep(1)
        print('p2 rooms:',await txt(p2,'#rooms'))
        await p2.click('#rooms [data-act=enter]');
        print('both in game',await waitfor(lambda: ingame(p2),50))
        await p2.screenshot(path='/tmp/p2join.png')
        print('P2 inert', await p2.evaluate("()=>[...document.querySelectorAll('[inert]')].map(e=>e.id||e.className).join(',')+' | open:'+[...document.querySelectorAll('.sheet:not(.hide),.dlg:not(.hide),#welcome:not(.hide)')].map(e=>e.id||e.className).join(',')"))
        await p2.click('[data-act=join]');await asyncio.sleep(1.5)
        print('after join p1:',await txt(p1,'#panel'),'| p2:',await txt(p2,'#panel'))
        print('mid-round p1:',await play_round(p1,p2))
        print('p1 over:',await txt(p1,'#panel'));print('p2 over:',await txt(p2,'#panel'))
        if await p1.locator('[data-act=again]').count() and await p2.locator('[data-act=again]').count():
            await p1.click('[data-act=again]');await p2.click('[data-act=again]');await asyncio.sleep(3)
            print('rematch p1:',await txt(p1,'#panel'),'| p2:',await txt(p2,'#panel'))
        else: print('again btn missing')
        print('res docs',[k for k in STORE if k.startswith('res/')])
        for p in (p1,p2):
            try:
                await p.click('[data-act=leave]',timeout=1500)
            except Exception:
                try: await p.click('[data-act=lobby]',timeout=1500)
                except Exception as e: print('no leave',e)
        await asyncio.sleep(1)
        await asyncio.sleep(1.5);print('rank p1',await txt(p1,'#rkMe'),'| p2',await txt(p2,'#rkMe'))
        for p in (p1,p2):
            await p.evaluate("()=>document.querySelector('#shbg').click()")
        await asyncio.sleep(0.3)
        for p in (p1,p2): await p.evaluate("()=>document.querySelector('.tabbar:not(.tbw) [data-k=rank]').click()")
        await asyncio.sleep(0.3);print('rank tab p1:',await txt(p1,'#tab-rank'))
        # 랭크 게임 관문
        await p1.click('#mmBtn');await asyncio.sleep(0.4)
        print('gate dlg:',await txt(p1,'#dlg'))
        await p1.click('[data-act=dlgok]');await asyncio.sleep(0.4);await p1.click('#sh-acc [data-act=glink]');await asyncio.sleep(0.6)
        print('acct p1 after link:',await txt(p1,'#acct'))
        await p2.evaluate("()=>{window.__fakeGoogleInUse=false}")
        await p2.click('#mmBtn');await asyncio.sleep(0.3)
        try:
            await p2.click('[data-act=dlgok]',timeout=800);await asyncio.sleep(0.4);await p2.click('#sh-acc [data-act=glink]',timeout=1500)
        except Exception: pass
        await asyncio.sleep(0.6)
        await p1.click('#mmBtn');await asyncio.sleep(0.3);await p2.click('#mmBtn')
        ok=await waitfor(lambda: ingame(p1),80);ok2=await waitfor(lambda: ingame(p2),80)
        print('ranked both in game',ok,ok2,'| mm:',await txt(p1,'#mmSt'),await txt(p2,'#mmSt'))
        if ok and ok2:
            print('ranked mid:',await play_round(p1,p2));print('ranked over p1:',await txt(p1,'#panel'))
        print('lob docs',[k for k in STORE if k.startswith('lob/')])
        print('store prefixes',sorted({k.split('/')[0] for k in STORE}),'mm left',[k for k in STORE if k.startswith('mm/')])
        print('denied p1',await p1.evaluate("()=>window.__deniedList||[]"));print('denied p2',await p2.evaluate("()=>window.__deniedList||[]"))
        print('errors',errs[:12]);await b.close()
asyncio.run(main())
