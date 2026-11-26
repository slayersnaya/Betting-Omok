// 테스트용 가짜 Firebase Auth (페이지마다 익명 uid)
const listeners=[];let cur=null;
export const getAuth=()=>A;const A={get currentUser(){return cur}};
export function onAuthStateChanged(a,cb){listeners.push(cb);setTimeout(()=>cb(cur),0);return()=>{const i=listeners.indexOf(cb);if(i>=0)listeners.splice(i,1)}}
export async function signInAnonymously(){let id=sessionStorage.getItem('fake-uid');if(!id){id='u'+Math.random().toString(36).slice(2,12)+Math.random().toString(36).slice(2,10);sessionStorage.setItem('fake-uid',id)}const g=sessionStorage.getItem('fake-g')==='1';cur={delete:async()=>{sessionStorage.removeItem('fake-uid');sessionStorage.removeItem('fake-g');cur=null;listeners.forEach(f=>f(null))},uid:id,isAnonymous:!g,providerData:g?[{providerId:sessionStorage.getItem('fake-p')||'google.com',email:(sessionStorage.getItem('fake-em')||window.__fakeEmail||'tester@example.com')}]:[]};listeners.slice().forEach(f=>f(cur));return{user:cur}}
export class GoogleAuthProvider{static credentialFromError(){return{}}}
export async function linkWithPopup(u){if(window.__fakeGoogleInUse){const e=new Error('in use');e.code='auth/credential-already-in-use';throw e}u.isAnonymous=false;u.providerData=[{providerId:'google.com',email:(window.__fakeEmail||'tester@example.com')}];sessionStorage.setItem('fake-g','1');return{user:u}}
export async function signInWithCredential(){cur={uid:'uGoogleOld0000000000',isAnonymous:false,providerData:[{providerId:'google.com',email:(window.__fakeEmail||'tester@example.com')}]};sessionStorage.setItem('fake-uid',cur.uid);sessionStorage.setItem('fake-g','1');return{user:cur}}
export const signInWithPopup=linkWithPopup;
export async function reauthenticateWithPopup(){return{}}
// 가짜 계정 삭제: 저장된 uid를 지우고 새 익명으로
export function __attachDelete(){}
// 이메일/비밀번호 흉내: 비밀번호 'wrong'이면 실패, __fakeEmailInUse면 이미 쓰는 이메일
export class EmailAuthProvider{static credential(email,password){return{email,password}}}
const ePD=email=>[{providerId:'password',email}];
export async function linkWithCredential(u,c){if(!c||!/@/.test(c.email||'')){const e=new Error('bad');e.code='auth/invalid-email';throw e}if((c.password||'').length<6){const e=new Error('weak');e.code='auth/weak-password';throw e}if(window.__fakeEmailInUse){const e=new Error('in use');e.code='auth/email-already-in-use';throw e}u.isAnonymous=false;u.providerData=ePD(c.email);sessionStorage.setItem('fake-g','1');sessionStorage.setItem('fake-p','password');sessionStorage.setItem('fake-em',c.email);return{user:u}}
export async function signInWithEmailAndPassword(a,email,password){if(password==='wrong'){const e=new Error('wrong');e.code='auth/invalid-credential';throw e}const id='uE'+[...email].reduce((h,c)=>(h*31+c.charCodeAt(0))>>>0,7).toString(36)+'0000000000';cur={uid:id,isAnonymous:false,providerData:ePD(email)};sessionStorage.setItem('fake-uid',id);sessionStorage.setItem('fake-g','1');sessionStorage.setItem('fake-p','password');sessionStorage.setItem('fake-em',email);listeners.slice().forEach(f=>f(cur));return{user:cur}}
export async function sendPasswordResetEmail(a,email){window.__fakeReset=email;return}
export async function reauthenticateWithCredential(){return{}}
