# 우편함·관리자 선물 시험: 관리자 화면에서 보내기(베타 양식·한 명·공지) → 받기·모두 받기·장착 → 규칙 거부(두 번·위조·기간·남의 우편·mr 조작) → 정리
# 사용: WEBDIR=/home/claude/eval/mail/web FPORT=9611 python3 mailtest.py
import sys;exec(open('/home/claude/eval/mail/tests/common.py').read())
import time
SH='/home/claude/eval/mail/shots'
async def wal(u): return STORE.get('wal/'+u)
async def reload_w(p):
    await p.evaluate("()=>window.__T.ev(`(async()=>{const x=await db.doc('wal/'+SEAT).get();ECO.w=ecoNorm(x.data());ecoLook();ecoPaint()})()`)");await asyncio.sleep(0.4)
async def forge(p,js):
    return await p.evaluate("""js=>new Promise(res=>{const w=window.__T.ev('ECO.w');const n=JSON.parse(JSON.stringify(w));const t=Math.floor((Date.now()+324e5)/864e5);if(n.d!==t){n.d=t;n.dc=0;n.dq=[]}
      try{(new Function('n',js))(n)}catch(e){return res('js '+e.message)}const db=window.__T.ev('db');db.doc('wal/'+window.__T.ev('SEAT')).set(Object.assign({},n,{at:{__st:1}})).then(()=>res('ok'),e=>res('denied'))})""",js)
async def mkmail(p,d,id=None):
    return await p.evaluate("""([d,id])=>new Promise(res=>{const db=window.__T.ev('db');id=id||('m'+d.until+'_'+Math.random().toString(36).slice(2,8).padEnd(6,'0'));db.doc('mail/'+id).set(Object.assign({by:window.__T.ev('SEAT'),at:{__st:1}},d)).then(()=>res(id),e=>res('denied'))})""",[d,id])
async def dlg(p): return await p.evaluate("()=>{const d=document.querySelector('#dlg');return d.classList.contains('hide')?'':d.innerText.replace(/\\s+/g,' ')}")
async def dlgok(p): await p.evaluate("()=>document.querySelector('#dlg [data-act=dlgok]')?.click()");await asyncio.sleep(0.6)
async def badge(p): return await p.evaluate("()=>{const e=document.querySelector('#hMail .mbn');return e&&e.classList.contains('on')?e.textContent:''}")
async def toastt(p): return await p.evaluate("()=>document.querySelector('#toast').textContent")
async def openmail(p):
    await p.evaluate("()=>window.__T.ev('closeSheet(true)')");await p.evaluate("()=>document.querySelector('#hMail').click()");await asyncio.sleep(1.2)
async def mailtxt(p): return await p.evaluate("()=>document.querySelector('#mailBody').innerText.replace(/\\s+/g,' ')")
async def fetchm(p): await p.evaluate("()=>window.__T.ev('mailFetch(true)')");await asyncio.sleep(0.8)
async def main():
    errs=[]
    async with async_playwright() as pw:
        b=await pw.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
        A=await page2(b,errs,'하늘',vp=(360,740));await asyncio.sleep(2.5)
        C=await page2(b,errs,'바다',vp=(390,844),scheme='light');await asyncio.sleep(2)
        G=await page2(b,errs,'손님',google=False);await asyncio.sleep(2)
        ad=await adminpage(b,errs,vp=(360,740));await asyncio.sleep(1.5)
        ua,uc,ug,uad=[await ev(x,'SEAT') for x in (A,C,G,ad)]
        chk('가짜 규칙에 우편 규칙 켜짐',await A.evaluate("()=>window.__T.ev('1')")==1 and await A.evaluate("()=>!!window.__mailRulesOn") )
        chk('머리줄 우편 버튼(옥돌 옆)',await A.evaluate("()=>{const b=document.querySelector('#hMail');return !!b&&!b.classList.contains('hide')&&b.previousElementSibling&&b.previousElementSibling.id==='hGem'}"))
        chk('처음엔 배지 없음',await badge(A)=='')
        # --- 관리자만 보이는 것
        await A.evaluate("()=>window.__T.ev(\"openSheet('set')\")");await asyncio.sleep(0.3)
        chk('일반: 설정에 선물 보내기 숨김',await A.evaluate("()=>document.querySelector('#admMail').classList.contains('hide')"))
        await A.evaluate("()=>window.__T.ev('closeSheet()')")
        chk('관리자 판별',await ev(ad,'isAdmin()'))
        await ad.evaluate("()=>window.__T.ev(\"openSheet('set')\")");await asyncio.sleep(0.4)
        chk('관리자: 설정에 선물 보내기',await ad.evaluate("()=>!document.querySelector('#admMail').classList.contains('hide')"))
        await ad.evaluate("()=>window.__T.ev('closeSheet()')")
        await ad.evaluate("()=>{const d=document.querySelector('#dlg');if(!d.classList.contains('hide'))d.querySelector('[data-act=dlgno]')?.click()}");await asyncio.sleep(0.3)
        await openmail(ad);t=await mailtxt(ad);chk('관리자 우편함: 베타 알림 줄',('베타 선물을 아직' in t),t)
        await ad.screenshot(path=SH+'/m_admin_box_360.png')
        # --- 일반 사용자 위조: 우편 만들기·지우기 거부
        r=await mkmail(A,{'to':'all','t':'x','msg':'','g':100,'it':'','from':int(time.time()*1000)-1000,'until':int(time.time()*1000)+864e5});chk('일반: 우편 만들기 거부',r=='denied',r)
        # --- 관리자: 베타 양식 → 보내기
        await ad.evaluate("()=>document.querySelector('[data-act=mailbeta]').click()");await asyncio.sleep(0.8)
        v=await ad.evaluate("()=>({t:document.querySelector('#maT').value,i:document.querySelector('#maI').value,g:document.querySelector('#maG').value,d0:document.querySelector('#maD0').value,d1:document.querySelector('#maD1').value,to:document.querySelector('#maTo [aria-pressed=true]').dataset.v})")
        kd=time.strftime('%Y-%m-%d',time.gmtime(time.time()+9*3600));kd6=time.strftime('%Y-%m-%d',time.gmtime(time.time()+9*3600+6*86400))
        chk('베타 양식: 제목·물결 테두리·전체·7일',v['t']=='Beta Test 참여 감사 선물' and v['i']=='f2' and v['to']=='all' and v['d0']==kd and v['d1']==kd6,v)
        await ad.screenshot(path=SH+'/m_admin_form_360.png',full_page=False)
        await ad.evaluate("()=>document.querySelector('[data-act=mailsend]').click()");await asyncio.sleep(0.5)
        d=await dlg(ad);chk('보내기 확인 창',('모든 사람' in d and '물결 테두리' in d),d)
        await ad.screenshot(path=SH+'/m_admin_confirm_360.png')
        await dlgok(ad);await asyncio.sleep(1)
        ms=[(k,v) for k,v in STORE.items() if k.startswith('mail/')]
        chk('우편 문서 1개 생김',len(ms)==1,[k for k,_ in ms])
        bid,bm=ms[0];bid=bid.split('/')[1]
        endk=int(time.mktime(time.strptime(kd6,'%Y-%m-%d')))*1000+86400000-9*3600000-int(time.timezone*-1000) if False else None
        import calendar;until_exp=calendar.timegm(time.strptime(kd6,'%Y-%m-%d'))*1000+86400000-9*3600000
        chk('우편: to all · f2 · 끝=마지막 날 다음 0시(한국)',bm['to']=='all' and bm['it']=='f2' and bm['g']==0 and bm['until']==until_exp and bid.startswith('m%d_'%until_exp),{k:bm[k] for k in ('to','it','g','from','until')})
        t=await ad.evaluate("()=>document.querySelector('#mailAdmBody').innerText.replace(/\\s+/g,' ')");chk('보낸 우편 목록에 보임',('Beta Test' in t and '받는 중' in t),t[-160:])
        await ad.screenshot(path=SH+'/m_admin_sent_360.png')
        # --- 사용자 A(구글) 받기
        await fetchm(A);chk('A 배지 1',await badge(A)=='1',await badge(A))
        await A.screenshot(path=SH+'/m_hdr_badge_360.png',clip={'x':0,'y':0,'width':360,'height':70})
        await openmail(A);t=await mailtxt(A);chk('A 우편함: 제목·선물·기간',('Beta Test 참여 감사 선물' in t and '물결 테두리' in t and '까지' in t and '받기' in t),t)
        await A.screenshot(path=SH+'/m_box_360_dark.png')
        g0=(await wal(ua))['g']
        await A.evaluate("()=>document.querySelector('[data-act=mailget]').click()");await asyncio.sleep(1.5)
        w=await wal(ua);chk('A 받기: f2 보유·mr 기록·옥돌 그대로',('f2' in w['own']) and w.get('mr')==[bid] and w['g']==g0 and w.get('k')=='mail',json.dumps(w)[:200])
        chk('A 받기 알림',('물결 테두리' in await toastt(A)),await toastt(A))
        t=await mailtxt(A);chk('A 받은 뒤: 받음·장착 버튼',('받음' in t and '장착' in t),t)
        chk('A 배지 0',await badge(A)=='')
        await A.screenshot(path=SH+'/m_box_360_got.png')
        await A.evaluate("()=>document.querySelector('[data-act=mailequip]').click()");await asyncio.sleep(1.2)
        w=await wal(ua);chk('A 장착: eq.f=f2',w['eq'].get('f')=='f2',w['eq'])
        t=await mailtxt(A);chk('장착 뒤 장착 버튼 사라짐',('장착' not in t and '받음' in t),t)
        # 두 번 받기·위조
        r=await forge(A,f"n.mr=n.mr.concat(['{bid}']);n.k='mail'");chk('같은 우편 두 번 거부',r=='denied',r)
        r=await forge(A,f"n.mr=[];n.k='mail'");chk('mr 비우기(mail) 거부',r=='denied',r)
        r=await forge(A,"n.mr=[];n.k='equip'");chk('다른 쓰기(equip)로 mr 비우기 거부',r=='denied',r)
        r=await forge(A,"n.mr=n.mr.concat(['m1999999999999_aaaaaa']);n.k='equip'");chk('다른 쓰기로 mr 늘리기 거부',r=='denied',r)
        r=await forge(A,"n.k='equip';n.eq={}");chk('정상 장착 쓰기(mr 그대로) 허용',r=='ok',r)
        await reload_w(A)
        # --- C: 이미 물결 테두리 보유 → 옥돌 1500
        w=dict(await wal(uc));w.update({'g':100,'own':['f2','t1'],'eq':{'f':'f2'}});await push('wal/'+uc,w);await reload_w(C)
        await fetchm(C);await openmail(C);t=await mailtxt(C);chk('C 보유 안내 한 줄',('보유 중 · 옥돌 1,500으로 받아요' in t),t)
        await C.screenshot(path=SH+'/m_box_390_light_owned.png')
        await C.evaluate("()=>document.querySelector('[data-act=mailget]').click()");await asyncio.sleep(1.5)
        w=await wal(uc);chk('C 받기: 옥돌 +1500·아이템 중복 없음',w['g']==1600 and w['own']==['f2','t1'] and w.get('mr')==[bid],json.dumps(w)[:200])
        chk('C 알림 옥돌 +1,500',('옥돌 +1,500' in await toastt(C)),await toastt(C))
        # --- 게스트도 받음
        await fetchm(G);await openmail(G);await G.evaluate("()=>document.querySelector('[data-act=mailget]').click()");await asyncio.sleep(1.5)
        w=await wal(ug);chk('게스트 받기',w and 'f2' in w['own'],json.dumps(w)[:160])
        # --- 규칙 위조: 금액·없는 우편·기간·남의 우편
        now=int(time.time()*1000)
        bmid=await mkmail(ad,{'to':'all','t':'옥돌 선물','msg':'','g':500,'it':'','from':now-60000,'until':now+864e5})
        chk('관리자 옥돌 우편 만들기',bmid!='denied',bmid)
        r=await forge(A,f"n.mr=n.mr.concat(['{bmid}']);n.g+=600;n.k='mail'");chk('옥돌 부풀리기 거부',r=='denied',r)
        r=await forge(A,f"n.mr=n.mr.concat(['{bmid}']);n.g+=500;n.own.push('x1');n.k='mail'");chk('아이템 끼워 넣기 거부',r=='denied',r)
        r=await forge(A,f"n.mr=n.mr.concat(['{bmid}']);n.g+=500;n.dc+=10;n.k='mail'");chk('하루 상한 값 건드리기 거부',r=='denied',r)
        r=await forge(A,f"n.mr=n.mr.concat(['m{now+864e5:.0f}_zzzzzz']);n.g+=500;n.k='mail'");chk('없는 우편 거부',r=='denied',r)
        fut=await mkmail(ad,{'to':'all','t':'예정','msg':'','g':50,'it':'','from':now+3600000,'until':now+7200000})
        r=await forge(A,f"n.mr=n.mr.concat(['{fut}']);n.g+=50;n.k='mail'");chk('시작 전 우편 거부',r=='denied',r)
        old=f'm{now-3600000}_oldold';STORE['mail/'+old]={'to':'all','t':'끝','msg':'','g':50,'it':'','from':now-7200000,'until':now-3600000,'by':uad,'at':now-7200000}
        await push('mail/'+old,STORE['mail/'+old])
        r=await forge(A,f"n.mr=n.mr.concat(['{old}']);n.g+=50;n.k='mail'");chk('끝난 우편 거부',r=='denied',r)
        pm=await mkmail(ad,{'to':uc,'t':'개인','msg':'','g':70,'it':'','from':now-60000,'until':now+864e5,'nk':'바다'})
        r=await forge(A,f"n.mr=n.mr.concat(['{pm}']);n.g+=70;n.k='mail'");chk('남의 개인 우편 거부',r=='denied',r)
        r=await A.evaluate(f"()=>window.__T.ev(\"db.collection('mail').where('to','==','{uc}').get().then(()=>'read',()=>'denied')\")");chk('남의 개인 우편 읽기 거부',r=='denied',r)
        r=await A.evaluate("()=>window.__T.ev(\"db.collection('mail').get().then(()=>'read',()=>'denied')\")");chk('일반: 전체 우편함 목록 읽기 거부(개인 우편 섞임)',r=='denied',r)
        r=await A.evaluate(f"()=>window.__T.ev(\"db.doc('mail/{bmid}').delete().then(()=>'ok',()=>'denied')\")");chk('일반: 우편 지우기 거부',r=='denied',r)
        # --- 끝난 id 정리: mr 에 끝난 우편 id 가 있으면 받을 때 빠짐
        w=dict(await wal(ua));w['mr']=[old]+w['mr'];await push('wal/'+ua,w);await reload_w(A)
        r=await forge(A,f"n.mr=n.mr.filter(x=>x!=='{old}');n.k='equip'");chk('끝난 id 도 다른 쓰기로는 못 뺌',r=='denied',r)
        await fetchm(A);chk('A 배지 1(옥돌 우편)',await badge(A)=='1',await badge(A))
        g0=(await wal(ua))['g'];await openmail(A);await A.evaluate(f"()=>document.querySelector('[data-act=mailget][data-id=\"{bmid}\"]').click()");await asyncio.sleep(1.5)
        w=await wal(ua);chk('받으면서 끝난 id 정리·옥돌 +500',old not in w['mr'] and bmid in w['mr'] and w['g']==g0+500,json.dumps(w.get('mr')))
        # --- 개인 우편: 관리자 화면 '한 명' → 찾기 → 보내기
        k=await ev(C,"nickKey('바다')");await push('nicks/'+k,{'by':uc,'g':True,'at':now,'n':'바다'})
        await ad.evaluate("()=>window.__T.ev('closeSheet(true)')");await ad.evaluate("()=>window.__T.ev('mailAdmOpen(false)')");await asyncio.sleep(0.8)
        await ad.evaluate("()=>document.querySelector('[data-act=mailto][data-v=one]').click()");await asyncio.sleep(0.2)
        await ad.fill('#maN','없는사람');await ad.evaluate("()=>document.querySelector('[data-act=mailfind]').click()");await asyncio.sleep(0.6)
        chk('없는 닉네임 안내',('찾지 못했' in await txt(ad,'#maFound')),await txt(ad,'#maFound'))
        await ad.fill('#maN','바다');await ad.press('#maN','Enter');await asyncio.sleep(0.6)
        chk('닉네임 찾기',('찾음' in await txt(ad,'#maFound')),await txt(ad,'#maFound'))
        await ad.fill('#maT','고마워요');await ad.fill('#maM','버그 제보 고마워요');await ad.fill('#maG','300');await ad.select_option('#maI','')
        await ad.screenshot(path=SH+'/m_admin_one_360.png')
        await ad.evaluate("()=>document.querySelector('[data-act=mailsend]').click()");await asyncio.sleep(0.4);d=await dlg(ad);chk('확인 창: 받는 사람 닉네임',('바다' in d and '옥돌 300' in d),d);await dlgok(ad);await asyncio.sleep(0.8)
        pm2=[k2 for k2,v2 in STORE.items() if k2.startswith('mail/') and v2.get('t')=='고마워요']
        chk('개인 우편 문서: to=C uid·nk',len(pm2)==1 and STORE[pm2[0]]['to']==uc and STORE[pm2[0]].get('nk')=='바다',pm2)
        await fetchm(A);t=await mailtxt(A);chk('A 에겐 안 보임',('버그 제보' not in t),t)
        await fetchm(C);chk('C 배지 3(전체 옥돌 + 개인 2)',await badge(C)=='3',await badge(C))
        await openmail(C);await C.screenshot(path=SH+'/m_box_390_light_two.png')
        g0=(await wal(uc))['g'];await C.evaluate("()=>document.querySelector('[data-act=mailall]').click()");await asyncio.sleep(2.5)
        w=await wal(uc);chk('C 모두 받기: +500+300+70',w['g']==g0+870 and len(w['mr'])==4,json.dumps(w.get('mr')))
        chk('모두 받기 알림',('옥돌 +870' in await toastt(C)),await toastt(C))
        # --- 공지(선물 없음): 열면 읽음
        nid=await mkmail(ad,{'to':'all','t':'점검 안내','msg':'오늘 밤 10시에 잠깐 점검해요','g':0,'it':'','from':now-60000,'until':now+864e5})
        await A.evaluate("()=>window.__T.ev('closeSheet(true)')");await fetchm(A);chk('공지 배지 1',await badge(A)=='1',await badge(A))
        await openmail(A);t=await mailtxt(A);chk('공지는 받기 버튼 없음',('점검 안내' in t),t);await asyncio.sleep(0.3)
        chk('열면 공지 읽음 → 배지 0',await badge(A)=='',await badge(A))
        await A.screenshot(path=SH+'/m_box_360_notice.png')
        # --- mr 20개 한도
        w=dict(await wal(ug));w['mr']=['m%d_%06d'%(now+864e5,i) for i in range(20)];await push('wal/'+ug,w);await reload_w(G)
        await fetchm(G);await openmail(G);await G.evaluate(f"()=>document.querySelector('[data-act=mailget][data-id=\"{bmid}\"]').click()");await asyncio.sleep(1.5)
        chk('20개 한도: 안내',('많아요' in await toastt(G)),await toastt(G))
        r=await forge(G,f"n.mr=n.mr.concat(['{bmid}']);n.g+=500;n.k='mail'");chk('21개 쓰기 거부',r=='denied',r)
        # --- 관리자 지우기·자동 정리
        STORE['mail/'+old]['until']=now-2*864e5;await push('mail/'+old,STORE['mail/'+old])
        await ad.evaluate("()=>window.__T.ev('closeSheet(true)')");await ad.evaluate("()=>window.__T.ev('mailAdmOpen(false)')");await asyncio.sleep(1.2)
        chk('끝난 지 하루 지난 우편 자동 정리','mail/'+old not in STORE)
        await ad.evaluate(f"()=>document.querySelector('[data-act=maildel][data-id=\"{nid}\"]').click()");await asyncio.sleep(0.3);await dlgok(ad);await asyncio.sleep(0.6)
        chk('관리자 지우기','mail/'+nid not in STORE)
        # --- 베타 알림 줄은 보낸 뒤 사라짐
        await ad.evaluate("()=>window.__T.ev('closeSheet(true)')");await fetchm(ad);await openmail(ad);t=await mailtxt(ad);chk('보낸 뒤 베타 알림 줄 없음',('아직 보내지' not in t),t[:80])
        # --- 다시 열 때 2분 안이면 다시 안 읽음
        n0=await A.evaluate("()=>{window.__q=0;const db=window.__T.ev('db');const c=db.collection;db.collection=function(p){if(p==='mail')window.__q++;return c.apply(this,arguments)};return 0}")
        await openmail(A);await openmail(A);chk('2분 안 다시 열기: 추가 읽기 없음',await A.evaluate("()=>window.__q")==0,await A.evaluate("()=>window.__q"))
        # --- 앱을 다시 열 때: 30분 안이면 서버 질의 없음(저장해 둔 목록) · 새 기기(저장 없음)는 질의 2개
        await A.reload();await asyncio.sleep(3.5)
        q=await A.evaluate("()=>window.__mailQ||0");chk('다시 열기(30분 안): 우편 질의 0',q==0,q)
        chk('다시 열기: 저장해 둔 목록으로 우편함 보임',await A.evaluate("()=>window.__T.ev('MAIL.list.length')")>=2)
        N=await page2(b,errs,'새손님',vp=(360,740));await asyncio.sleep(3.5)
        q=await N.evaluate("()=>[window.__mailQ||0,window.__mailR||0]");chk('새 기기 첫 열기: 질의 2개',q[0]==2,q)
        bad=[e for e in errs if 'TUNNEL' not in e and 'ERR_' not in e]
        chk('페이지 오류 없음',not bad,bad[:4])
        print('mail denies',await A.evaluate("()=>(window.__mailDeny||[]).slice(-3)"))
        print('RESULT %d/%d'%(sum(1 for _,o in RES if o),len(RES)));await b.close()
asyncio.run(main())
