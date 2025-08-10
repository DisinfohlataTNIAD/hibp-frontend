export async function sha1Hex(str){
  const enc = new TextEncoder().encode(str);
  const buf = await crypto.subtle.digest('SHA-1', enc);
  return [...new Uint8Array(buf)].map(b=>b.toString(16).padStart(2,'0')).join('').toUpperCase();
}
