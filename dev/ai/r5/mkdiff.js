// node mkdiff.js aifile out.html : 현재 서비스 index.html의 AI 구간을 aifile로 바꾼 새 html 생성
const fs=require('fs');const S='/home/claude/betting-omok/index.html';const s=fs.readFileSync(S,'utf8');
const a='// ===== AI START =====',b='// ===== AI END =====';const i=s.indexOf(a),j=s.indexOf(b)+b.length;
if(i<0||j<b.length||s.indexOf(a,i+1)>=0)throw new Error('marker');
const ai=fs.readFileSync(process.argv[2],'utf8');if(!ai.startsWith(a)||!ai.endsWith(b))throw new Error('ai file markers');
fs.writeFileSync(process.argv[3],s.slice(0,i)+ai+s.slice(j));
console.log('AI 구간 줄 범위(원본):',s.slice(0,i).split('\n').length,'~',s.slice(0,j).split('\n').length);
