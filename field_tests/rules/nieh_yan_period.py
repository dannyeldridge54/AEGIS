"""What decay constant does the Twist get if its angle is a Nieh-Yan theta-angle? (derivation in NIEH_YAN_PERIOD.md)
Reduced Planck units: kappa = 8 pi G = 1/M_Pl^2 = 1.

Chain:
 1. Action term (Mercuri & Taveras 0903.4407 eq. 6): S_NY = (1/2kappa) * Integral beta(x) N,  N = T^a T_a - e^a e^b R_ab.
 2. Chandia & Zanelli: with A = (omega, e/l) an SO(5) connection, tr_SO5(R R) - tr_SO4(R R) = (2/l^2) N, since
    (e^a e_a) = 0. Pontryagin integrals of R^{ab} R_ab are 8 pi^2 x integer, so Integral N = 4 pi^2 l^2 nu, nu integer.
 3. For constant beta: S_NY = (beta/2kappa) 4 pi^2 l^2 nu. Physics is unchanged under beta -> beta + Delta_beta when
    S changes by 2 pi nu:  Delta_beta = kappa / (pi l^2).
 4. Kinetic term from torsion (eq. 22): phi = sqrt(3/(2 kappa)) beta, so F = Delta_phi / (2 pi) = sqrt(3/2) / (2 pi^2 l^2)
    (l in reduced Planck lengths). If the smallest allowed charge is nu_min > 1, F is divided by nu_min.
Prints F for natural choices of l, and the l each fitted F would need."""
import json
import math

F_of_l = lambda l: math.sqrt(1.5) / (2 * math.pi ** 2 * l ** 2)
l_of_F = lambda F: math.sqrt(math.sqrt(1.5) / (2 * math.pi ** 2 * F))
L_P = 1 / math.sqrt(8 * math.pi)            # sqrt(G) in reduced-Planck units (M_Pl = 1/sqrt(8 pi G))

choices = {"l = reduced Planck length 1/M_Pl": 1.0, "l = Planck length sqrt(G)": L_P,
           "l = 2 x Planck length": 2 * L_P}
fitted = {"early role (P-ACT/Planck) F = 0.14": 0.14, "late DES Y5 best F = 1.00": 1.00,
          "late Pantheon+ best F = 2.51": 2.51, "TF value F1 = sqrt(3/2)": math.sqrt(1.5), "TF value F2 = sqrt6": math.sqrt(6)}
out = {"F for natural l (nu_min = 1)": {k: F_of_l(v) for k, v in choices.items()},
       "l needed (in Planck lengths sqrt(G)) for each F": {k: l_of_F(F) / L_P for k, F in fitted.items()},
       "F at l = Planck length, closed form": "(4/pi) sqrt(3/2) M_Pl",
       "check (4/pi) sqrt(3/2)": 4 / math.pi * math.sqrt(1.5)}
json.dump(out, open("nieh_yan_period.json", "w"), indent=1)
print(json.dumps(out, indent=1))
