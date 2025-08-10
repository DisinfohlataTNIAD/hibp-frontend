const dict = {
  id: {
    "nav.home":"Home","nav.breaches":"Breaches","nav.stats":"Stats",
    "hero.subtitle":"Cek email/username & password (k-anonymity). Front-end only — sambungkan ke backend di assets/js/api.js.",
    "home.checkAccount":"Check","home.checkPasswordTitle":"Cek Password (k-anonymity)","home.checkPassword":"Check",
    "home.notifyTitle":"Notify me","home.notifyDesc":"Dapatkan notifikasi saat akun/keyword kamu muncul di breach baru.","home.subscribe":"Subscribe"
  },
  en: {
    "nav.home":"Home","nav.breaches":"Breaches","nav.stats":"Stats",
    "hero.subtitle":"Check email/username & password (k-anonymity). Front-end only — wire to backend in assets/js/api.js.",
    "home.checkAccount":"Check","home.checkPasswordTitle":"Check Password (k-anonymity)","home.checkPassword":"Check",
    "home.notifyTitle":"Notify me","home.notifyDesc":"Get alerts when your account/keyword appears in a new breach.","home.subscribe":"Subscribe"
  }
};
const sel = document.getElementById('lang');
if(sel){
  const stored = localStorage.getItem('lang') || 'id';
  sel.value = stored; applyLang(stored);
  sel.addEventListener('change', e=>{ localStorage.setItem('lang', e.target.value); applyLang(e.target.value); });
}
function applyLang(lang){
  document.querySelectorAll('[data-i18n]').forEach(el=>{
    const key = el.getAttribute('data-i18n'); const val = dict[lang]?.[key]; if(val) el.textContent = val;
  });
}
