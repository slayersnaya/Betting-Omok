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

async def setnick(p,v):
    await p.evaluate("()=>document.querySelector('[data-act=sheet][data-k=nick]').click()");await asyncio.sleep(0.3)
    await p.fill('#nick',v);await p.click('#nickOk');await asyncio.sleep(1.2)
    if await p.evaluate("()=>!document.querySelector('#dlg').classList.contains('hide')&&/바꿀까요/.test(document.querySelector('#dlg').innerText)"):
        await p.evaluate("()=>document.querySelector('#dlg [data-act=dlgok]').click()");await asyncio.sleep(1.2)
    return await p.evaluate("()=>[localStorage.getItem('bo-nick'),document.querySelector('#nickErr').textContent,!document.querySelector('#sh-nick').classList.contains('hide')]")
async def main():
    errs=[]
    async with async_playwright() as pw:
        b=await pw.chromium.launch()
        p1=await newpage(b,errs,'');p2=await newpage(b,errs,'')
        for p in (p1,p2): await p.evaluate("()=>{document.querySelector('#nick').value='';localStorage.removeItem('bo-nick')}")
        await asyncio.sleep(1.5)
        print('p1 성민',await setnick(p1,'성민'))
        print('p2 성민',await setnick(p2,'성민'))
        await p2.evaluate("()=>document.querySelector('#shbg').click()");await asyncio.sleep(0.3);print('p2 after cancel',await p2.evaluate("()=>[localStorage.getItem('bo-nick'),document.querySelector('#nick').value,document.querySelector('#nickTxt').textContent]"))
        print('p2 " 성 민 "',await setnick(p2,' 성 민 '))
        await p2.evaluate("()=>document.querySelector('#shbg').click()");await asyncio.sleep(0.3)
        print('p2 묘수덕후(AI)',await setnick(p2,'묘수덕후'));await p2.evaluate("()=>document.querySelector('#shbg').click()");await asyncio.sleep(0.3)
        print('p2 하율',await setnick(p2,'하율'))
        print('p1 -> 성민2',await setnick(p1,'성민2'));await asyncio.sleep(1)
        print('p2 -> 성민 (released)',await setnick(p2,'성민'))
        print('nicks',sorted(k for k in STORE if k.startswith('nicks/')))
        # 시작 시 겹침 안내
        p3=await newpage(b,errs,'');await p3.evaluate("()=>{localStorage.setItem('bo-nick','성민');}");await p3.reload();await asyncio.sleep(4)
        print('p3 dlg',await txt(p3,'#dlg'))
        print('denied',await p1.evaluate("()=>window.__deniedList||[]"),await p2.evaluate("()=>window.__deniedList||[]"))
        print('errors',[e for e in errs if 'TUNNEL' not in e][:10]);await b.close()
asyncio.run(main())
