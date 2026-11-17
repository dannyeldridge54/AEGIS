"""Single source of truth for SERAPIS-model inputs used by Hyperion checks (lesson D1153: re-read the LATEST D-note).
Each value cites the D-note that currently defines it."""
WINO_THERMAL_MASS_TEV = (2.207, 2.842)   # Born vs NLO-Sommerfeld thermal mass (2009.00640); f bracket (D1152)
def wino_fraction(M_TeV):
    """SERAPIS-E post-hoc wino is THERMAL (D784): f = (M/M_th)^2, bracketed (D1152). Returns (low, high)."""
    return (M_TeV/WINO_THERMAL_MASS_TEV[1])**2, (M_TeV/WINO_THERMAL_MASS_TEV[0])**2
DELTA_NEFF = {'rho': 0.0, 'tau_i': (0.0, 0.054, 0.161, 0.301)}   # D725; D1088/D1122 (unpopulated, U(1), SU(2), SU(2)+gaugino)
OMBH2 = 0.02242                          # Planck 2018 +BAO (D1082)
