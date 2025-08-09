import { apiGetAccount, apiGetPasswordRange, apiNotify } from './api.js';
import { UI } from './ui.js';
import { sha1Hex } from './hash.js';

const acctInput = document.getElementById('acct');
const acctOut   = document.getElementById('acctOut');
const pwdInput  = document.getElementById('pwd');
const pwdOut    = document.getElementById('pwdOut');

document.getElementById('btnAcct').addEventListener('click', onCheckAccount);
document.getElementById('btnPwd').addEventListener('click', onCheckPassword);

async function onCheckAccount(){
  const acct = acctInput.value.trim();
  if(!acct) return UI.toast('Masukkan email/username.', 'warning');
  acctOut.innerHTML = UI.skeleton(3);
  UI.loading('Check account…');
  try{
    const data = await apiGetAccount(acct);
    UI.close();
    if(data.pwned){
      UI.alert('Ditemukan!', `Akun terdeteksi di <b>${data.breaches.length}</b> breach.`, 'error');
      acctOut.innerHTML = renderBreachList(data.breaches);
    }else{
      UI.alert('Aman', 'Tidak ditemukan di database publik.', 'success');
      acctOut.innerHTML = `<div class="small status-ok">✅ Tidak ditemukan.</div>`;
    }
  }catch(e){
    UI.close();
    UI.alert('Error', e.message || String(e), 'error');
    acctOut.innerHTML = `<div class="small status-bad">Error: ${e}</div>`;
  }
}

function renderBreachList(items){
  if(!items?.length) return '<div class="small">—</div>';
  const rows = items.map(b=>`
    <tr>
      <td><a class="link" href="breach.html?id=${encodeURIComponent(b.Name || b.Id || b.name)}">${b.Title || b.Name}</a></td>
      <td>${b.BreachDate || b.breachDate || '-'}</td>
      <td>${(b.DataClasses || b.dataClasses || []).join(', ')}</td>
      <td>${b.IsVerified ? '✅' : '⚠️'}</td>
    </tr>
  `).join('');
  return `<div class="card"><table class="table"><thead><tr><th>Breach</th><th>Tanggal</th><th>Data</th><th>Verified</th></tr></thead><tbody>${rows}</tbody></table></div>`;
}

async function onCheckPassword(){
  const pwd = pwdInput.value;
  if(!pwd) return UI.toast('Masukkan password.', 'warning');
  pwdOut.innerHTML = UI.skeleton(1);
  UI.loading('Hash & check password…');
  try{
    const h = await sha1Hex(pwd);
    const prefix = h.slice(0,5), suffix = h.slice(5);
    const text = await apiGetPasswordRange(prefix);
    UI.close();
    const hit = text.split('\n').find(line => line.startsWith(suffix));
    if(hit){
      const count = hit.split(':')[1];
      pwdOut.innerHTML = `<div class="card"><div class="status-bad">⚠️ Password ditemukan ${count}× di HIBP</div></div>`;
      UI.alert('Password Pwned', `Password kamu muncul <b>${count}</b> kali. Segera ganti & aktifkan 2FA.`, 'error');
    }else{
      pwdOut.innerHTML = `<div class="card"><div class="status-ok">✅ Tidak ditemukan di pwned list</div></div>`;
      UI.toast('Password OK', 'success', 1500);
    }
  }catch(e){
    UI.close();
    UI.alert('Error', e.message || String(e), 'error');
    pwdOut.innerHTML = `<div class="small status-bad">Error: ${e}</div>`;
  }
}

/* Subscribe Notify */
const btnNotify = document.getElementById('btnNotify');
if(btnNotify){
  btnNotify.addEventListener('click', async ()=>{
    const target = document.getElementById('notifyTarget').value.trim();
    const contact = document.getElementById('notifyContact').value.trim();
    if(!target) return UI.toast('Isi target dulu.', 'warning');
    UI.loading('Mendaftar…');
    try{ await apiNotify(target, contact); UI.close(); UI.toast('Berhasil subscribe!', 'success'); }
    catch(e){ UI.close(); UI.alert('Error', e.message || String(e), 'error'); }
  });
}
