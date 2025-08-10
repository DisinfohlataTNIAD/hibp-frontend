import { apiListBreaches } from './api.js';
import { UI } from './ui.js';

const listBox = document.getElementById('breachList');
const qInput  = document.getElementById('q');
const fData   = document.getElementById('f-data');

document.getElementById('btnSearch').addEventListener('click', render);
qInput.addEventListener('keydown', e=>{if(e.key==='Enter') render();});
if(fData) fData.addEventListener('change', render);

render();

async function render(){
  listBox.innerHTML = UI.skeleton(6, 72);
  try{
    const data = await apiListBreaches();
    const q = (qInput?.value || '').trim().toLowerCase();
    const f = fData?.value || '';
    const filtered = data.filter(b=>{
      const hay = `${b.Name||b.name} ${b.Title||b.title} ${(b.DataClasses||b.dataClasses||[]).join(' ')}`.toLowerCase();
      const passQ = !q || hay.includes(q);
      const passF = !f || (b.DataClasses||b.dataClasses||[]).includes(f);
      return passQ && passF;
    });
    listBox.innerHTML = filtered.map(card).join('') || `<div class="small">Tidak ada hasil.</div>`;
  }catch(e){
    listBox.innerHTML = `<div class="small status-bad">Error: ${e}</div>`;
  }
}
function card(b){
  const data = (b.DataClasses||b.dataClasses||[]).slice(0,5).join(', ');
  const ver  = b.IsVerified ? '✅ Verified' : '⚠️ Unverified';
  const logo = b.LogoPath || b.logoPath || '';
  const id   = b.Name || b.Id || b.name;
  return `
    <a class="card link" href="breach.html?id=${encodeURIComponent(id)}" style="display:block">
      <div class="row" style="align-items:center">
        <div class="col" style="max-width:80px">
          ${logo ? `<img src="${logo}" alt="" style="width:64px;height:64px;border-radius:12px;border:1px solid #1f1f25;object-fit:cover"/>` : `<div class="skeleton" style="width:64px;height:64px"></div>`}
        </div>
        <div class="col" style="min-width:200px">
          <div style="font-weight:700">${b.Title || b.Name}</div>
          <div class="small">${b.Domain || b.domain || ''}</div>
          <div class="small">${b.BreachDate || b.breachDate || '-'}</div>
          <div class="small">${ver}</div>
        </div>
        <div class="col">
          <span class="badge">${data || '—'}</span>
        </div>
      </div>
    </a>`;
}
