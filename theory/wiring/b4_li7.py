"""B4 — run PRyMordial (external, path given as argv[1]) and print light elements. PREREG_B4_li7.md"""
import sys, os, math, time
ext = sys.argv[1]; os.chdir(ext); sys.path.insert(0, ext)
import PRyM.PRyM_init as I
I.aTid_flag = True; I.compute_bckg_flag = True; I.compute_nTOp_flag = True; I.compute_nTOp_thermal_flag = False
I.save_bckg_flag = I.save_nTOp_flag = I.save_nTOp_thermal_flag = False; I.verbose_flag = False
I.smallnet_flag = True; I.julia_flag = False
import PRyM.PRyM_main as Mn
out = []
for wb in (0.02230, 0.02242):
    I.Omegabh2 = wb; t = time.time(); r = Mn.PRyMclass().PRyMresults()
    out.append(f"Obh2={wb}: Neff={r[0]:.4f} Yp(CMB)={r[3]:.5f} D/H={r[5]:.4f}e-5 He3/H={r[6]:.4f}e-5 Li7/H={r[7]:.4f}e-10 ({time.time()-t:.0f}s)")
    last = r
li = last[7]
out.append(f"L1 Li7 {li:.3f} vs 4.94+-0.72: {(li-4.94)/0.72:+.2f} sigma -> {'CONSISTENT' if abs(li-4.94) <= 0.72 else 'NOT'}")
out.append(f"L2 Yp {last[3]:.5f} vs PRIMAT 0.24721 (rel {last[3]/0.24721-1:+.4f}); D/H {last[5]:.4f} vs 2.4393 (rel {last[5]/2.4393-1:+.4f})")
out.append(f"L3 Li7/Spite = {li/1.6:.2f}; ({li}-1.6)/sqrt(0.3^2+0)= {(li-1.6)/0.3:.1f} sigma (obs error only)")
print("\n".join(out))
