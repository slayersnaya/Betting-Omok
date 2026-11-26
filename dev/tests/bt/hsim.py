import json,random,bisect
B=json.load(open('botr.json'))
def botsAt(day):
    ks=sorted(int(k) for k in B);k=min(ks,key=lambda x:abs(x-day));return B[str(k)]
MIX=[(0,900,[70,30,0,0]),(900,1100,[30,60,10,0]),(1100,1300,[0,30,60,10]),(1300,1500,[0,0,60,40]),(1500,1e9,[0,0,20,80])]
HUM={'입문':[.5,.25,.12,.02],'보통':[.7,.5,.3,.05],'잘함':[.85,.7,.5,.12],'고수':[.95,.85,.7,.25]}
def tier(r):
    return '브론즈' if r<900 else '실버' if r<1100 else '골드' if r<1300 else '플래티넘' if r<1500 else '다이아' if r<1700 else '마스터'
def sim(htype,gpd,new,seed):
    rnd=random.Random(seed);r=1000.;hist=[];ws=0;ls=0;n=0
    for day in range(94):
        bots=botsAt(day)
        for g in range(gpd):
            c=sorted(bots,key=lambda x:abs(x[1]-r));pool=[x for x in c if abs(x[1]-r)<=150][:6] or c[:1];bk,br=rnd.choice(pool)
            if new:
                row=next(m for lo,hi,m in MIX if lo<=r<hi);t=rnd.random()*100;k=0
                while k<3:
                    t-=row[k]
                    if t<0:break
                    k+=1
                if r<1500 and len(hist)>=5:
                    w=sum(hist[-10:])/len(hist[-10:])
                    if w<.4:k=max(0,k-1)
                    elif w>.6:k=min(3,k+1)
            else: k=bk
            if ws>=5:k=3
            cap=0 if ls>=5 else 1 if ls>=4 else 2 if ls>=2 else 3
            k=min(k,cap)
            win=rnd.random()<HUM[htype][k]
            K=40 if n<10 else 32;e=1/(1+10**((br-r)/400));r+=K*((1 if win else 0)-e);n+=1
            hist.append(1 if win else 0);ws=ws+1 if win else 0;ls=0 if win else ls+1
    return r,sum(hist)/len(hist)
for new in (False,True):
    print('=== ','새 방식' if new else '지금 방식')
    for h in HUM:
        for gpd in (1,3):
            rs=[sim(h,gpd,new,s) for s in range(40)];T={}
            for r,_ in rs:T[tier(r)]=T.get(tier(r),0)+1
            wr=sum(w for _,w in rs)/len(rs)
            print(f'{h} 하루{gpd}판: 평균 {sum(r for r,_ in rs)/len(rs):.0f}점 승률 {wr*100:.0f}% ',' '.join(f'{k}{v}' for k,v in sorted(T.items(),key=lambda x:['브론즈','실버','골드','플래티넘','다이아','마스터'].index(x[0]))))
