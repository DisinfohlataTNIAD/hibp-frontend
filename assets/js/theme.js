const btn = document.getElementById('btnTheme');
if(btn){
  btn.addEventListener('click', ()=>{
    const onLight = document.documentElement.classList.toggle('light');
    localStorage.setItem('theme', onLight ? 'light' : 'dark');
  });
  const saved = localStorage.getItem('theme'); if(saved === 'light') document.documentElement.classList.add('light');
}
