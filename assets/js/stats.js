import { apiGetStats, apiTopDataClasses } from './api.js';
import { UI } from './ui.js';

const kpi = document.getElementById('kpi');
const topData = document.getElementById('topData');

(async ()=>{
  kpi.innerHTML = `<div class="skeleton" style="height:84px"></div><div class="skeleton" style="height:84px"></div><div class="skeleton" style="height:84px"></div>`;
  topData.innerHTML = `<div class="skeleton" style="height:120px"></div>`;
  try{
    const s = await apiGetStats(); const t = await apiTopDataClasses();
    kpi.innerHTML = renderKPI(s); topData.innerHTML = renderTopData(t);
  }catch(e){
    kpi.innerHTML = `<div class="small status-bad">Error: ${e}</div>`;
    topData.innerHTML = `<div class="small status-bad">Error: ${e}</div>`;
  }
})();
function renderKPI(s){
  const fmt = x => x!=null ? new Intl.NumberFormat().format(x) : '—';
  return `
    <div class="item"><div class="num">${fmt(s.totalBreaches)}</div><div class="lbl">Total Breaches</div></div>
    <div class="item"><div class="num">${fmt(s.totalAccounts)}</div><div class="lbl">Accounts Indexed</div></div>
    <div class="item"><div class="num">${fmt(s.totalPwnedPasswords)}</div><div class="lbl">Pwned Passwords</div></div>
  `;
}
function renderTopData(items){
  if(!items?.length) return '<div class="small">No data.</div>';
  const rows = items.map(x=>`<tr><td>${x.name}</td><td>${new Intl.NumberFormat().format(x.count)}</td></tr>`).join('');
  return `<h2>Top Data Classes</h2><table class="table"><thead><tr><th>Class</th><th>Count</th></tr></thead><tbody>${rows}</tbody></table>`;
}
