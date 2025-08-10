// BASE_URL bisa diubah kalau backend beda origin (mis. 'https://api.domainmu.com')
const BASE_URL = "";

export async function apiGetAccount(acct){ 
  const response = await fetch(`${BASE_URL}/api/check-account`, {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({account: acct})
  });
  if(!response.ok) throw new Error(`HTTP ${response.status}`);
  return response.json();
}

export async function apiGetPasswordRange(prefix5){
  // Menggunakan HIBP API langsung untuk k-anonymity
  const res = await fetch(`https://api.pwnedpasswords.com/range/${prefix5.toUpperCase()}`, {
    headers:{'cache-control':'no-cache'}
  });
  if(!res.ok) throw new Error(`HTTP ${res.status}`); 
  return res.text();
}

export async function apiCheckPassword(password){
  const response = await fetch(`${BASE_URL}/api/check-password`, {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({password: password})
  });
  if(!response.ok) throw new Error(`HTTP ${response.status}`);
  return response.json();
}

export async function apiListBreaches(){ 
  return fetchJSON(`${BASE_URL}/api/breaches`); 
}

export async function apiGetBreach(id){ 
  return fetchJSON(`${BASE_URL}/api/breach/${encodeURIComponent(id)}`); 
}

export async function apiGetStats(){ 
  return fetchJSON(`${BASE_URL}/api/stats`); 
}

export async function apiTopDataClasses(){ 
  return fetchJSON(`${BASE_URL}/api/top-dataclasses`); 
}

export async function apiNotify(target, contact){
  const r = await fetch(`${BASE_URL}/api/notify`, {
    method:'POST', 
    headers:{'content-type':'application/json'}, 
    body:JSON.stringify({target, contact})
  });
  if(!r.ok) throw new Error(`HTTP ${r.status}`); 
  return r.json().catch(()=>({ok:true}));
}

async function fetchJSON(url){
  const res = await fetch(url, {headers:{'cache-control':'no-cache'}});
  const t = await res.text();
  try{ 
    const j = JSON.parse(t); 
    if(!res.ok) throw new Error(j?.detail || `HTTP ${res.status}`); 
    return j; 
  }
  catch(e){ 
    if(!res.ok) throw new Error(t || `HTTP ${res.status}`); 
    throw e; 
  }
}
