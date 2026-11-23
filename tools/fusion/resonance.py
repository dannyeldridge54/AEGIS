"""N4: resolved-resonance cross sections rebuilt from ENDF-6 File 2 parameters (ENDF-102 Appendix D), at 0 K.
SLBW (for the can-fail check), MLBW (LRF=2) and Reich-Moore (LRF=3, no fission). Returns elastic, capture, total in barns, plus the MF3
background added (H9)."""
import numpy as np
import endf

C_K = 2.196807e-3      # k = C_K * AWRI/(AWRI+1) * sqrt(E[eV])  in 1e12 cm^-1 (sigma in barns via pi/k^2)

def pen(l, rho):
    r2 = rho * rho
    if l == 0: return rho, np.zeros_like(rho)
    if l == 1: return rho * r2 / (1 + r2), -1 / (1 + r2)
    if l == 2: d = 9 + 3 * r2 + r2 * r2; return rho * r2 * r2 / d, -(18 + 3 * r2) / d
    if l == 3: d = 225 + 45 * r2 + 6 * r2 * r2 + r2 ** 3; return rho * r2 ** 3 / d, -(675 + 90 * r2 + 6 * r2 * r2) / d
    raise ValueError(l)

def phase(l, rho):
    if l == 0: return rho
    if l == 1: return rho - np.arctan(rho)
    if l == 2: return rho - np.arctan2(3 * rho, 3 - rho * rho)
    if l == 3: return rho - np.arctan2(rho * (15 - rho * rho), 15 - 6 * rho * rho)
    raise ValueError(l)

def _radii(rg, sec, awri):
    a_ch = 0.123 * awri ** (1 / 3) + 0.08
    ap = sec.get('APL') or rg['AP']
    a_pen = ap if rg.get('NAPS', 0) == 1 else a_ch
    return a_pen, ap

def load(path):
    m = endf.Material(path); r = m.section_data[2, 151]; iso = r['isotopes'][0]; rg = iso['ranges'][0]
    bg = {}
    for mt in (1, 2, 102):
        if (3, mt) in m.section_data:
            t = m.section_data[3, mt]['sigma']; bg[mt] = (np.asarray(t.x), np.asarray(t.y))
    return rg, bg

def xs(path, E, form=None):
    """E: array of eV. form: None -> the file's own (LRF 2 = MLBW, 3 = RM); 'SLBW' forces single-level."""
    rg, bg = load(path); E = np.asarray(E, float); I = rg['SPI']; lrf = rg['LRF']; form = form or {2: 'MLBW', 3: 'RM'}[lrf]
    inside = (E >= rg['EL']) & (E <= rg['EH'])
    el = np.zeros_like(E); cap = np.zeros_like(E); tot = np.zeros_like(E)
    for sec in rg['sections']:
        l = int(sec['L']); awri = sec['AWRI']; a_pen, ap = _radii(rg, sec, awri)
        k = C_K * awri / (awri + 1) * np.sqrt(E); rho = k * a_pen; rhoh = k * ap
        P, S = pen(l, rho); phi = phase(l, rhoh); pik2 = np.pi / k ** 2
        ER = np.asarray(sec['ER']); AJ = np.asarray(sec['AJ']); GN = np.asarray(sec['GN']); GG = np.asarray(sec['GG'])
        # spin groups present
        Js = sorted(set(np.round(np.abs(AJ), 3)))
        gsum = 0.0
        for J in Js:
            g = (2 * J + 1) / (2 * (2 * I + 1)); gsum += g
            sel = np.isclose(np.abs(AJ), J)
            er, gn, gg = ER[sel], GN[sel], GG[sel]
            kr = C_K * awri / (awri + 1) * np.sqrt(np.abs(er)); Pr, Sr = pen(l, kr * a_pen)
            if form == 'RM':
                R = np.zeros_like(E, dtype=complex)
                for j in range(len(er)):
                    gnE = gn[j] * P / Pr[j]
                    R += (gnE / 2) / (er[j] - E - 0.5j * gg[j])
                U = np.exp(-2j * phi) * (1 + 1j * R) / (1 - 1j * R)
                t = 2 * pik2 * g * (1 - U.real); e = pik2 * g * np.abs(1 - U) ** 2
                tot += t; el += e; cap += t - e
            else:
                acc = np.zeros_like(E, dtype=complex)
                for j in range(len(er)):
                    gnE = gn[j] * P / Pr[j]; erp = er[j] + gn[j] * (Sr[j] - S) / (2 * Pr[j]); gt = gnE + gg[j]
                    den = (erp - E) ** 2 + gt ** 2 / 4
                    cap += pik2 * g * gnE * gg[j] / den
                    if form == 'SLBW':   # single-level: resonances do not interfere with each other
                        el += pik2 * g * (gnE ** 2 - 2 * gnE * gt * np.sin(phi) ** 2 + 2 * (E - erp) * gnE * np.sin(2 * phi)) / den
                    acc += 1j * gnE / (erp - E - 0.5j * gt)
                if form == 'MLBW':
                    U = np.exp(-2j * phi) * (1 + acc); e = pik2 * g * (np.abs(1 - U) ** 2 - 4 * np.sin(phi) ** 2)
                    el += e
        # potential scattering for every partial wave (all J), including J values that carry resonances (added once here)
        el += 4 * pik2 * (2 * l + 1) * np.sin(phi) ** 2 if form != 'RM' else 4 * pik2 * ((2 * l + 1) - gsum) * np.sin(phi) ** 2
        if form == 'RM': tot += 4 * pik2 * ((2 * l + 1) - gsum) * np.sin(phi) ** 2
    if form != 'RM': tot = el + cap
    el = np.where(inside, el, 0.0); cap = np.where(inside, cap, 0.0); tot = np.where(inside, tot, 0.0)
    for mt, arr in ((2, el), (102, cap), (1, tot)):
        if mt in bg: arr += np.interp(E, bg[mt][0], bg[mt][1], left=0, right=0) * inside
    return dict(E=E, elastic=el, capture=cap, total=tot)
