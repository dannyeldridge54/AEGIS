const Z=require('./zurvan_core.js'),fs=require('fs');const out={};
for(const f of fs.readdirSync('.').filter(f=>f.endsWith('.slha'))){const p=Z.paramsFromSLHA(fs.readFileSync(f,'utf8'));const r=Z.deltaEW(p);out[f]={D:r.Delta_EW,Ds:r.Delta_EW_pairs_summed,top3:r.contributions.slice(0,3),head:r.headline,nw:r.warnings.length,res:r.EWSB_residual};}
console.log(JSON.stringify(out));
