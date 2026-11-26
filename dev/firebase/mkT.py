import shutil,os
src='/home/claude/web';dst='/tmp/webT'
shutil.rmtree(dst,ignore_errors=True);shutil.copytree(src,dst)
p=dst+'/index.html';s=open(p,encoding='utf-8').read()
i=s.rindex('}\n</script>')
s=s[:i]+"window.__T={L,RK,MM,UI,G,rankCompute,legalTriples,renderAll,tierOf,BOTS,seat:()=>SEAT,ev:c=>eval(c)};\n"+s[i:]
open(p,'w',encoding='utf-8').write(s)
