"""D711 (locked PREREG_D711). AI-assisted."""
import math, numpy as np, camb
AS=2.1e-9
print("T11 DESI DR1 P1D: D2*=0.379±0.032, n*=-2.309±0.019 | T12 S8")
for name,ns,a,b in (("LCDM P18",0.9649,0,0),("SERAPIS low",0.970,-0.94e-3,-3.8e-5),("SERAPIS mid",0.9725,-1.0e-3,-3.8e-5),("SERAPIS high",0.975,-1.06e-3,-3.8e-5)):
    p=camb.CAMBparams(); p.set_cosmology(H0=67.4,ombh2=0.0224,omch2=0.120,mnu=0.06)
    p.InitPower.set_params(As=AS,ns=ns,nrun=a,nrunrun=b,pivot_scalar=0.05)
    p.set_matter_power(redshifts=[3.0,0.0],kmax=50); res=camb.get_results(p)
    kh,z,pk=res.get_matter_power_spectrum(minkh=1e-3,maxkh=40,npoints=600)
    h=0.674; Hz=res.hubble_parameter(3.0); kp=0.009*Hz/4.0
    iz=list(z).index(3.0); k=kh*h; P=pk[iz]/h**3; lnk=np.log(k); lnD=np.log(k**3*P/(2*np.pi**2))
    f=lambda x: np.interp(x,lnk,lnD); D2=math.exp(f(math.log(kp))); nL=(f(math.log(kp)+0.01)-f(math.log(kp)-0.01))/0.02-3
    s8=res.get_sigma8_0(); Om=(0.0224+0.120+0.06/93.14)/h**2; S8=s8*math.sqrt(Om/0.3)
    print(f"  {name}: D2*={D2:.4f} (pull {(D2-0.379)/0.032:+.2f}) n*={nL:.4f} (pull {(nL+2.309)/0.019:+.2f}) | sigma8={s8:.4f} S8={S8:.4f} (vs HSC+BOSS {(S8-0.8294)/0.0110:+.2f}σ, vs CMB {(S8-0.836)/0.0125:+.2f}σ)")
print(f"  running: pred -1.0e-3 vs P1D joint 0.0014±0.0041: pull {(-1.0e-3-0.0014)/0.0041:+.2f}σ")
print(f"T13 N_eff 3.044 vs ACT DR6 2.86±0.13: pull {(3.044-2.86)/0.13:+.2f}σ")
