import { apiGetAccount, apiGetPasswordRange, apiCheckPassword, apiNotify } from './api.js';
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
    if(data.found){
      UI.alert('Ditemukan!', `Akun terdeteksi di breach database.`, 'error');
      acctOut.innerHTML = renderBreachResults(data);
    }else{
      UI.alert('Aman', 'Tidak ditemukan di database breach.', 'success');
      acctOut.innerHTML = `<div class="small status-ok">✅ Tidak ditemukan di database breach.</div>`;
    }
  }catch(e){
    UI.close();
    UI.alert('Error', e.message || String(e), 'error');
    acctOut.innerHTML = `<div class="small status-bad">Error: ${e}</div>`;
  }
}

function renderBreachResults(data){
  if(!data.found) return '<div class="small status-ok">✅ Tidak ditemukan.</div>';
  
  let html = '<div class="card">';
  html += '<h3>⚠️ Breach Detected</h3>';
  
  // Show results from each source
  if(data.sources){
    Object.entries(data.sources).forEach(([source, result]) => {
      if(result.found || result.pwned){
        html += `<div class="status-bad" style="margin: 10px 0; padding: 10px; border-left: 4px solid #e74c3c;">`;
        html += `<strong>${source.toUpperCase()}</strong>: `;
        if(result.message){
          html += result.message;
        } else if(result.total){
          html += `Found in ${result.total} entries`;
        } else {
          html += 'Breach detected';
        }
        html += '</div>';
      } else if(!result.error){
        html += `<div class="status-ok" style="margin: 10px 0; padding: 10px; border-left: 4px solid #27ae60;">`;
        html += `<strong>${source.toUpperCase()}</strong>: Clean`;
        html += '</div>';
      }
    });
  }
  
  if(data.breaches && data.breaches.length > 0){
    html += '<h4>Breach Details:</h4>';
    data.breaches.forEach(breach => {
      html += `<div style="margin: 5px 0; padding: 8px; background: rgba(231, 76, 60, 0.1); border-radius: 4px;">`;
      html += `<strong>Source:</strong> ${breach.source}<br>`;
      if(breach.data){
        html += `<strong>Details:</strong> ${JSON.stringify(breach.data, null, 2)}`;
      }
      html += '</div>';
    });
  }
  
  html += '</div>';
  return html;
}

async function onCheckPassword(){
  const pwd = pwdInput.value;
  if(!pwd) return UI.toast('Masukkan password.', 'warning');
  pwdOut.innerHTML = UI.skeleton(1);
  UI.loading('Hash & check password…');
  try{
    // Use our Flask API endpoint
    const result = await apiCheckPassword(pwd);
    UI.close();
    
    if(result.pwned){
      pwdOut.innerHTML = `<div class="card"><div class="status-bad">⚠️ Password ditemukan ${result.count}× di HIBP</div></div>`;
      UI.alert('Password Pwned', `Password kamu muncul <b>${result.count}</b> kali. Segera ganti & aktifkan 2FA.`, 'error');
    } else {
      pwdOut.innerHTML = `<div class="card"><div class="status-ok">✅ Tidak ditemukan di pwned list</div></div>`;
      UI.toast('Password OK', 'success', 1500);
    }
  }catch(e){
    UI.close();
    // Fallback to original k-anonymity method if API fails
    try {
      const h = await sha1Hex(pwd);
      const prefix = h.slice(0,5), suffix = h.slice(5);
      const text = await apiGetPasswordRange(prefix);
      const hit = text.split('\n').find(line => line.startsWith(suffix));
      if(hit){
        const count = hit.split(':')[1];
        pwdOut.innerHTML = `<div class="card"><div class="status-bad">⚠️ Password ditemukan ${count}× di HIBP</div></div>`;
        UI.alert('Password Pwned', `Password kamu muncul <b>${count}</b> kali. Segera ganti & aktifkan 2FA.`, 'error');
      }else{
        pwdOut.innerHTML = `<div class="card"><div class="status-ok">✅ Tidak ditemukan di pwned list</div></div>`;
        UI.toast('Password OK', 'success', 1500);
      }
    } catch(fallbackError) {
      UI.alert('Error', e.message || String(e), 'error');
      pwdOut.innerHTML = `<div class="small status-bad">Error: ${e}</div>`;
    }
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
    try{ 
      await apiNotify(target, contact); 
      UI.close(); 
      UI.toast('Berhasil subscribe!', 'success'); 
    }
    catch(e){ 
      UI.close(); 
      UI.alert('Error', e.message || String(e), 'error'); 
    }
  });
}
