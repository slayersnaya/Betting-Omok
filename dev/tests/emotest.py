# 이모트 버튼 시험: 보임·글자·아이콘 = 이모트 캐릭터 / 첫 대국 말풍선 1번만·누름 통과 / 고르기 창·쿨다운 / 좁은 화면 글자 숨김(겹침·가로 넘침 없음)
import asyncio,os,json
os.environ.setdefault('WEBDIR','/home/claude/eval/invite/web');os.environ.setdefault('GPORT','9631')
os.environ['OUT']='/tmp/emotest';exec(open('/home/claude/eval/invite/tests/gshots.py').read().split('async def main():')[0])
R=[]
def chk(n,ok,info=''):R.append(ok);print(('PASS ' if ok else 'FAIL ')+n+(' | '+str(info)[:200] if info!='' else ''),flush=True)
AI="(()=>{closeSheet();goLobby();UI.mode='local';L.start('A','mid');show('game');renderAll();return 1})()"
BOT="(()=>{const x=BOTS[7];closeSheet();goLobby();UI.mode='local';L.start('A',x.lv,{bot:{id:x.id,nick:x.nick,r:x.base}});show('game');renderAll();return 1})()"
async def start(p,c):
    await ev(p,c);await p.wait_for_timeout(1200)
    try: await p.click('#coin',timeout=600)
    except Exception: pass
async def main():
    async with async_playwright() as pw:
        b=await pw.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
        seed();ctx,p=await ctxpage(b,412,860,'dark',games=False);await ev(p,"lrm('bo-emotip')")
        await start(p,AI);await p.wait_for_timeout(300)
        chk('E1 첫 대국 시작 직후(동전 넘기기 중)엔 말풍선 없음',await p.evaluate("()=>!document.querySelector('#emoTip')"))
        await p.wait_for_timeout(3000)
        st=await p.evaluate("()=>{const b=document.querySelector('#emoBtn');return {vis:!b.classList.contains('hide'),lbl:b.querySelector('.eml')&&getComputedStyle(b.querySelector('.eml')).display!=='none',txt:b.innerText.trim(),face:!!b.querySelector('.emic svg circle[fill^=\"url(#fxs\"]'),aria:b.getAttribute('aria-label')}}")
        chk('E2 버튼 보임 · 글자 "이모트" · 아이콘 = 이모트 캐릭터',st['vis'] and st['lbl'] and st['txt']=='이모트' and st['face'],st)
        tip=await p.evaluate("()=>{const t=document.querySelector('#emoTip');return t?{txt:t.innerText,pe:getComputedStyle(t).pointerEvents,top:t.getBoundingClientRect().top,bb:document.querySelector('#emoBtn').getBoundingClientRect().bottom}:null}")
        chk('E3 첫 대국 말풍선 "이모트를 보낼 수 있어요"(버튼 바로 아래)',tip and tip['txt']=='이모트를 보낼 수 있어요' and 0<tip['top']-tip['bb']<20,tip)
        chk('E4 말풍선은 누름 통과(대국 조작 안 막음)',tip and tip['pe']=='none')
        await p.wait_for_timeout(5000)
        chk('E5 4.6초 뒤 사라짐',await p.evaluate("()=>!document.querySelector('#emoTip')"))
        chk('E6 한 번 보면 기록',await ev(p,"lget('bo-emotip')")=='1')
        await ev(p,"goLobby()");await start(p,AI);await p.wait_for_timeout(3500)
        chk('E7 다음 대국엔 다시 안 뜸',await p.evaluate("()=>!document.querySelector('#emoTip')"))
        await p.click('#emoBtn');await p.wait_for_timeout(300)
        chk('E8 누르면 고르기 창 12개',await p.evaluate("()=>!document.querySelector('#emoPick').classList.contains('hide')&&document.querySelectorAll('#emoPick .emoi').length===12"))
        await p.click('#emoPick .emoi[data-i=\"1\"]');await p.wait_for_timeout(500)
        c=await p.evaluate("()=>{const b=document.querySelector('#emoBtn');return [b.classList.contains('cool'),getComputedStyle(b.querySelector('.emic'),'::after').content,!!document.querySelector('.emob.me')]}")
        chk('E9 보낸 뒤 쿨다운 고리(얼굴 둘레) · 내 말풍선',c[0] and c[1]!='none' and c[2],c)
        await ctx.close()
        # 좁은 화면: 글자 숨김 · 넘침 없음
        for (w,mode,expect) in [(320,AI,True),(360,BOT,True),(412,BOT,False),(390,AI,False)]:
            seed();ctx,p=await ctxpage(b,w,780,'light',games=False);await ev(p,"lset('bo-emotip','1')");await start(p,mode);await p.wait_for_timeout(1500)
            g=await p.evaluate("()=>{const b=document.querySelector('#emoBtn'),gm=document.querySelector('#gmid'),t=document.querySelector('.gtop');return {tight:b.classList.contains('tight'),gm:gm.scrollWidth<=gm.clientWidth+1,top:t.scrollWidth<=t.clientWidth+1,sw:document.documentElement.scrollWidth<=innerWidth}}")
            chk(f'E10 {w}px {"랭크AI" if mode==BOT else "AI"}: 글자 {"숨김" if expect else "보임"} · 가운데 글 안 잘림 · 가로 넘침 없음',g['tight']==expect and g['gm'] and g['top'] and g['sw'],g)
            await ctx.close()
        await b.close()
    print('ERRS',[e for e in ERRS if 'ERR_' not in e][:5]);print(f'결과 {sum(R)}/{len(R)}')
asyncio.run(main())
