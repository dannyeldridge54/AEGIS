import json,numpy as np,hashlib
d=json.load(open(''+__import__('sys').argv[1]+''))
L=np.arange(4001); fsky=0.4
arc=np.pi/180/60
def N(dT,fw):  # white noise D_l in muK^2
    s=fw*arc/np.sqrt(8*np.log(2)); nl=(dT*arc)**2*np.exp(L*(L+1)*s*s); return L*(L+1)/(2*np.pi)*nl
NT=N(6.2,1.4); NP=N(6.2*np.sqrt(2),1.4)
bins=[(30,300),(300,800),(800,1500),(1500,2500),(2500,4000)]
res={}
for sn in ["","_dovekie","_union3"]:
    t=d["edelockP"+sn]; l=d["lcdmP"+sn]; r={}
    TT,EE,TE=[np.array(l[k]) for k in("tt","ee","te")]
    for k in("ee","te","tt"):
        a,b=np.array(t[k]),np.array(l[k]); dd=a-b
        if k=="ee": var=2*(EE+NP)**2
        elif k=="tt": var=2*(TT+NT)**2
        else: var=(TE**2+(TT+NT)*(EE+NP))
        var=var/((2*L+1)*fsky); m=(L>=30)
        snr2=float(np.sum(dd[m]**2/var[m]))
        r[k]={"bins":[{"l":[lo,hi],"mean_dD_muK2":float(dd[lo:hi].mean()),"mean_frac":float((dd[lo:hi]/np.where(np.abs(b[lo:hi])>1e-3*np.abs(b[lo:hi]).max(),b[lo:hi],np.nan)).__array__()[~np.isnan(dd[lo:hi]/np.where(np.abs(b[lo:hi])>1e-3*np.abs(b[lo:hi]).max(),b[lo:hi],np.nan))].mean())} for lo,hi in bins],
              "rough_SO_snr":snr2**0.5}
    r["H0_twist"]=t["H0"]; r["H0_lcdm"]=l["H0"]; r["ns_twist"]=t["ns"]; r["ns_lcdm"]=l["ns"]
    res["edelockP"+sn]=r
json.dump({"note":"Locked Twist (edelockP*) minus Planck-data LCDM (lcdmP*), lensed D_l from CAMB at stored best fits; sigma8 gate passed (<=1e-4). rough_SO_snr: white noise 6.2 uK-arcmin T (x sqrt2 pol), 1.4' beam, f_sky 0.4, l 30-4000, Gaussian, no foregrounds; indicative only.","spectra_sha256":hashlib.sha256(open(''+__import__('sys').argv[1]+'','rb').read()).hexdigest(),"results":res},open('v4_cmb_pattern_frozen.json','w'),indent=1)
for n,r in res.items():
    print(n,"H0 %.2f vs %.2f ns %.4f vs %.4f"%(r["H0_twist"],r["H0_lcdm"],r["ns_twist"],r["ns_lcdm"]))
    for k in("ee","te","tt"): print("  ",k,"SNR %.1f"%r[k]["rough_SO_snr"],[ (b["l"][0],round(b["mean_dD_muK2"],3),round(b["mean_frac"]*100,2)) for b in r[k]["bins"]])
