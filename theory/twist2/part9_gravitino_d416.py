"""D416 (locked PREREG_D416_PART9): Part 9 (light gravitino) — total dark radiation = gravitino + hidden decay products (D412). AI-assisted.
Gravitino: ΔN = 0.059 (g*_dec/90)^{-4/3} (arXiv:1601.07386 normalisation at g* = 90). Hidden pair: D412 values (0.034 MSSM g*, 0.094 SM g*)."""
grav = {"g*=90 (paper)": 0.059, "g*=106.75 (SM, superpartners heavier than T_dec)": 0.059 * (106.75 / 90) ** (-4 / 3),
        "g*=228.75 (full MSSM)": 0.059 * (228.75 / 90) ** (-4 / 3)}
hid = {"hidden pair, MSSM g* (D412)": 0.034, "hidden pair, SM g* (D412)": 0.094}
for gk, gv in grav.items():
    for hk, hv in hid.items():
        t = gv + hv
        print(f"gravitino {gk:48s} {gv:.3f} + {hk:28s} {hv:.3f} = {t:.3f}  vs < 0.14: {'OK' if t < 0.14 else 'EXCEEDS'}")
