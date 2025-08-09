// BASE_URL bisa diubah kalau backend beda origin (mis. 'https://api.domainmu.com')
const BASE_URL = "";

export async function apiGetAccount(acct){ return fetchJSON(`${BASE_URL}/api/account?acct=${encodeURIComponent(acct)}`); }
export async function apiGetPasswordRange(prefix5){
  const res = await fetch(`${BASE_URL}/api/password?k=${encodeURIComponent(prefix5.toUpperCase())}`, {headers:{'cache-control':'no-cache'}});
  if(!res.ok) throw new Error(`HTTP ${res.status}`); return res.text();
}
export async function apiListBreaches(){ return fetchJSON(`${BASE_URL}/api/breaches`); }
export async function apiGetBreach(id){ return fetchJSON(`${BASE_URL}/api/breach/${encodeURIComponent(id)}`); }
export async function apiGetStats(){ return fetchJSON(`${BASE_URL}/api/stats`); }
export async function apiTopDataClasses(){ return fetchJSON(`${BASE_URL}/api/top-dataclasses`); }
export async function apiNotify(target, contact){
  const r = await fetch(`${BASE_URL}/api/notify`, {method:'POST', headers:{'content-type':'application/json'}, body:JSON.stringify({target, contact})});
  if(!r.ok) throw new Error(`HTTP ${r.status}`); return r.json().catch(()=>({ok:true}));
}
async function fetchJSON(url){
  const res = await fetch(url, {headers:{'cache-control':'no-cache'}});
  const t = await res.text();
  try{ const j = JSON.parse(t); if(!res.ok) throw new Error(j?.detail || `HTTP ${res.status}`); return j; }
  catch(e){ if(!res.ok) throw new Error(t || `HTTP ${res.status}`); throw e; }
}
