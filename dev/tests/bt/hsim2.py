import json,random,sys
B=json.load(open('botr.json'))
def botsAt(day):
    ks=sorted(int(k) for k in B);k=min(ks,key=lambda x:abs(x-day));return B[str(k)]
HUM={'입문':[.5,.25,.12,.02],'보통':[.7,.5,.3,.05],'잘함':[.85,.7,.5,.12],'고수':[.95,.85,.7,.25]}
TI=['브론즈','실버','골드','플래티넘','다이아','마스터']
def tier(r): return TI[0] if r<900 else TI[1] if r<1100 else TI[2] if r<1300 else TI[3] if r<1500 else TI[4] if r<1700 else TI[5]
def sim(MIX,floor,wrmax,htype,gpd,seed):
    rnd=random.Random(seed);r=1000.;hist=[];ws=0;ls=0;n=0
    for day in range(94):
        bots=botsAt(day)
        for g in range(gpd):
            c=sorted(bots,key=lambda x:abs(x[1]-r));pool=[x for x in c if abs(x[1]-r)<=150][:6] or c[:1];bk,br=rnd.choice(pool)
            row=next(m for lo,hi,m in MIX if lo<=r<hi);t=rnd.random()*100;k=0
            while k<3:
                t-=row[k]
                if t<0:break
                k+=1
            if r<wrmax and len(hist)>=5:
                w=sum(hist[-10:])/len(hist[-10:])
                if w<.4:k=max(0,k-1)
                elif w>.6:k=min(3,k+1)
            if ws>=5:k=3
            cap=0 if ls>=5 else 1 if ls>=4 else 2 if ls>=2 else 3
            k=min(k,cap)
            win=rnd.random()<HUM[htype][k]
            orr=max(br,r-floor) if floor is not None else br
            K=40 if n<10 else 32;e=1/(1+10**((orr-r)/400));r+=K*((1 if win else 0)-e);n+=1
            hist.append(1 if win else 0);ws=ws+1 if win else 0;ls=0 if win else ls+1
    return r,sum(hist)/len(hist)
def run(name,MIX,floor,wrmax):
    print('===',name)
    for h in HUM:
        for gpd in (1,3):
            rs=[sim(MIX,floor,wrmax,h,gpd,s) for s in range(40)];T={}
            for r,_ in rs:T[tier(r)]=T.get(tier(r),0)+1
            print(f' {h} {gpd}판: {sum(r for r,_ in rs)/len(rs):.0f}점 승률{sum(w for _,w in rs)/len(rs)*100:.0f}%',' '.join(f'{k}{T[k]}' for k in TI if k in T))
CUR=[(0,900,[70,30,0,0]),(900,1100,[30,60,10,0]),(1100,1300,[0,30,60,10]),(1300,1500,[0,0,60,40]),(1500,1e9,[0,0,20,80])]
A=[(0,900,[70,30,0,0]),(900,1100,[30,60,10,0]),(1100,1300,[0,30,60,10]),(1300,1500,[0,10,70,20]),(1500,1700,[0,0,75,25]),(1700,1e9,[0,0,40,60])]
run('표만 조정(A)',A,None,1700)
run('표 A + 상대 점수 하한(내 점수-50)',A,50,1700)
run('표 A + 하한 100',A,100,1700)
import sys
B2=[(0,900,[70,30,0,0]),(900,1100,[30,60,10,0]),(1100,1300,[0,30,60,10]),(1300,1500,[0,10,70,20]),(1500,1700,[0,0,80,20]),(1700,1e9,[0,0,50,50])]
run('B2 + 하한0',B2,0,1700)
B3=[(0,900,[70,30,0,0]),(900,1100,[30,60,10,0]),(1100,1300,[0,30,60,10]),(1300,1500,[0,10,70,20]),(1500,1700,[0,0,85,15]),(1700,1e9,[0,0,50,50])]
run('B3 + 하한0 (보정 다이아까지)',B3,0,1700)
