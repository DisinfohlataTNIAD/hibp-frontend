rimport { apiGetBreach } from './api.js';
import { UI } from './ui.js';

const box = document.getElementById('detail');
const params = new URLSearchParams(location.search);
const id = params.get('id');

(async ()=>{
  box.innerHTML = UI.skeleton(3, 90);
  try{
    const b = await apiGetBreach(id);
    box.innerHTML = render(b);
  }catch(e){
    box.innerHTML = `<div class="small status-bad">Error: ${e}</div>`;
  }
})();

function render(b){
  const data = (b.DataClasses||b.dataClasses||[]).join(', ') || '—';
  const ver  = b.IsVerified ? '✅ Verified' : '⚠️ Unverified';
  const size = b.PwnCount ? new Intl.NumberFormat().format(b.PwnCount) : '—';
  const logo = b.LogoPath || '';
  return `
    <div class="card">
      <div class="row">
        <div class="col" style="max-width:120px">${logo?`<img src="${logo}" style="width:96px;height:96px;border-radius:12px;border:1px solid #1f1f25;object-fit:cover"/>`:'<div class="skeleton" style="width:96px;height:96px"></div>'}</div>
        <div class="col">
          <h2 style="margin:0">${b.Title || b.Name}</h2>
          <div class="small">${b.Domain || ''}</div>
          <div class="small">${b.BreachDate || '-'}</div>
          <div class="small">${ver}</div>
        </div>
      </div>
    </div>
    <div class="kpi">
      <div class="item"><div class="num">${size}</div><div class="lbl">Pwned Accounts</div></div>
      <div class="item"><div class="num">${(b.IsSpamList?'Yes':'No')}</div><div class="lbl">Spam List</div></div>
      <div class="item"><div class="num">${(b.IsSensitive?'Yes':'No')}</div><div class="lbl">Sensitive</div></div>
    </div>
    <div class="card">
      <div class="small" style="margin-bottom:6px">Data Classes</div>
      <div>${data}</div>
    </div>
    ${b.Description?`<div class="card"><div class="small">Deskripsi</div><div>${b.Description}</div></div>`:''}
  `;
}
