const Z=require('./zurvan_core.js'),fs=require('fs');const out={};
for(const f of fs.readdirSync('.').filter(f=>f.endsWith('.slha'))){const p=Z.paramsFromSLHA(fs.readFileSync(f,'utf8'));p.mZ=Math.sqrt((p.g**2+p.gp**2)/2*(p.vu**2+p.vd**2));const r=Z.deltaEW(p);out[f]={D:r.Delta_EW,Ds:r.Delta_EW_pairs_summed,top3:r.contributions.slice(0,3)};}
console.log(JSON.stringify(out));
