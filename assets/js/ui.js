// SweetAlert2 harus di-include di HTML via CDN
export const UI = {
  toast(msg, type="info", ms=2200){ Swal.fire({toast:true, position:'top-end', icon:type, title:msg, showConfirmButton:false, timer:ms, timerProgressBar:true}); },
  alert(title, html, type="info"){ return Swal.fire({title, html, icon:type, confirmButtonText:'OK', showClass:{popup:'swal2-show'}, hideClass:{popup:'swal2-hide'}}); },
  confirm(title, text, type="warning"){ return Swal.fire({title, text, icon:type, showCancelButton:true, confirmButtonText:'Lanjut', cancelButtonText:'Batal'}); },
  loading(title="Loading…"){ Swal.fire({title, didOpen:()=>Swal.showLoading(), allowOutsideClick:false, allowEscapeKey:false, backdrop:true}); },
  close(){ Swal.close(); },
  skeleton(count=3, h=64){ return new Array(count).fill(0).map(()=>`<div class="skeleton" style="height:${h}px"></div>`).join(""); }
}
