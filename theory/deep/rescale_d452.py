import math, sys
sys.path.insert(0, 'theory/deep'); from cloud_capture_d446 import run
xs, xE = 1.3e-4, 29.6; allcap = True
for lab, a in (("V(x*)=1", 1/(2*xs)), ("V(x*)=10", 10**(2/3)/(2*xs))):
    VE = (2*a*xE)**1.5
    for gs in (0.1, 0.5):
        r = gs**0.25*math.sqrt(math.pi/VE)
        for ms in (1e4, 1e5):
            refl, xmin, ret, xf, rem = run(ms, r)
            ok = ret is not None and abs(xE-xf) < 1e-2
            if lab == "V(x*)=1" and not ok: allcap = False
            print(f"{lab} a={a:.0f} V(x_E)={VE:.2e} g_s={gs} M_s/M_P={r:.2e} m_s={ms:.0e}: reflections {len(refl)}, xmin {xmin if xmin is None else round(xmin,4)}, "
                  f"return {'yes' if ret else 'no'}, offset {xE-xf:.2e} -> {'CAPTURES' if ok else 'FAILS TO PIN'}", flush=True)
for gs in (0.1, 0.5):
    m = gs**0.25*math.sqrt(math.pi); print(f"plateau with V(x*)=1: M_s(x*)/M_P = {m:.2f} (g_s {gs}) -> D439 at M_s~M_P: dn_s ~ -2e-6..-6e-6 (amplitude offset only)")
print("VERDICT:", "CONTROL + CAPTURE COMPATIBLE" if allcap else "TENSION: control vs capture")
