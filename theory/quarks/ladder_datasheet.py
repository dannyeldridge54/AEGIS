"""Twin slip-ladder DATA SHEET (P-Q9/P-Q10). Writes theory/quarks/LADDER_DATASHEET.csv.
Left ladder: (m,0) classes, rungs climb toward the knot ρ (CP-violating minima, 2201.02020).
Right ladder: (0,n) classes, minima at the knot i (CP-conserving, 2201.02020).
Centre: mixed (m,n) classes sit on the arc |τ|=1 between ρ and i (CP-conserving), moving toward ρ or i as m or n grows.
Every number carries a status: lit (paper), formula (paper's fit, verified m<=7), extrap (m>7), computed, or open."""
import csv, math, os
c = math.sqrt(3)*0.0145
OCC = {1: 'down quarks; charged leptons (T1, D1734; TENSION with Koide-at-ρ)', 8: 'up quarks (T2: m_u*=8.26, chance 52%)'}
rows = []
for m in list(range(1, 33)) + [48, 64, 128]:
    e = c/(m + 1/16)
    rows.append(dict(side='left (ρ)', cls=f'({m},0)', rung=m, eps_abs=f'{e:.5f}', eps_arg_deg=50.0, cp='violating',
                     m2_over_m3_scale=f'{e:.5f}', m1_over_m3_scale=f'{e*e:.2e}', occupant=OCC.get(m, 'empty'),
                     status='formula' if m <= 7 else 'extrap'))
rows.append(dict(side='left (ρ)', cls='(∞,0)', rung='∞', eps_abs='0', eps_arg_deg='', cp='conserving (knot)', m2_over_m3_scale='0',
                 m1_over_m3_scale='0', occupant='Koide circulant leptons? (D1595); inflaton endpoint (D1606)', status='lit/derived'))
rows.append(dict(side='centre (arc)', cls='(m,n), m,n≥1', rung='—', eps_abs='on |τ|=1', eps_arg_deg='', cp='conserving',
                 m2_over_m3_scale='open', m1_over_m3_scale='open', occupant='none assigned', status='lit (positions open: Q11)'))
for n in (1, 2, 3, '∞'):
    rows.append(dict(side='right (i)', cls=f'(0,{n})', rung=n, eps_abs='0 (τ = i)', eps_arg_deg='', cp='conserving',
                     m2_over_m3_scale='none (no slip)', m1_over_m3_scale='none', occupant='neutrino modulus (P-F3); dark thread rests at i (D1653)' if n == '∞' else 'empty',
                     status='lit'))
p = os.path.join(os.path.dirname(__file__), 'LADDER_DATASHEET.csv')
with open(p, 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
print(p, len(rows), 'rows')
