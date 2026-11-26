import asyncio,threading,http.server,socketserver,functools
from playwright.async_api import async_playwright
PORT=8766
class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self,*a):pass
def serve():
    socketserver.TCPServer.allow_reuse_address=True
    with socketserver.TCPServer(('127.0.0.1',PORT),functools.partial(Q,directory='/home/claude/web')) as s:s.serve_forever()
threading.Thread(target=serve,daemon=True).start()
FAKE={'firebase-app.js':'fake/app.js','firebase-auth.js':'fake/auth.js','firebase-firestore.js':'fake/fs.js'}
UAS={'android':'Mozilla/5.0 (Linux; Android 14; SM-S918N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0 Mobile Safari/537.36',
 'kakao':'Mozilla/5.0 (Linux; Android 14; SM-S918N; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/131.0 Mobile Safari/537.36 KAKAOTALK 10.8.0',
 'ios':'Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Mobile/15E148 Safari/604.1'}
async def main():
    async with async_playwright() as pw:
        b=await pw.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
        for k,ua in UAS.items():
            ctx=await b.new_context(viewport={'width':390,'height':844},user_agent=ua,device_scale_factor=2)
            await ctx.add_init_script("localStorage.setItem('bo-tut-done','1');localStorage.setItem('bo-rkintro','1');localStorage.setItem('bo-rklg','1');sessionStorage.setItem('bo-noatt','1');localStorage.setItem('bo-welcomed','1');window.__fsSend=()=>{}")
            async def route(rt): await rt.fulfill(path=FAKE[rt.request.url.split('/')[-1]],content_type='application/javascript')
            await ctx.route('https://www.gstatic.com/**',route)
            p=await ctx.new_page();errs=[];p.on('pageerror',lambda e:errs.append(str(e)))
            await p.goto(f'http://127.0.0.1:{PORT}/index.html');await p.wait_for_timeout(1500)
            if k=='android':
                await p.evaluate("()=>{const e=new Event('beforeinstallprompt',{cancelable:true});e.prompt=()=>{window.__prompted=1};e.userChoice=Promise.resolve({outcome:'accepted'});window.dispatchEvent(e)}")
                await p.wait_for_timeout(300)
            t=await p.evaluate("()=>{const c=document.getElementById('instCard'),s=document.getElementById('instSheet');return [c?c.innerText.replace(/\\s+/g,' '):null,s?s.innerText.replace(/\\s+/g,' '):null,location.href.slice(0,60)]}")
            await p.screenshot(path=f'/tmp/inst_{k}.png')
            if k=='android':
                await p.click('#instSheet [data-ok]');await p.wait_for_timeout(300)
                print(k,'prompted',await p.evaluate("()=>window.__prompted"),'card after',await p.evaluate("()=>!!document.getElementById('instCard')"))
            sw=await p.evaluate("()=>navigator.serviceWorker.getRegistration().then(r=>!!r)")
            print(k,'|',t,'| sw',sw,'| errs',errs)
            await ctx.close()
        await b.close()
asyncio.run(main())
