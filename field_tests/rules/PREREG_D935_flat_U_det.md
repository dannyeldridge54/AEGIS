# PREREG D935: does a point-wise flat single U exist anywhere? (Project F, F1b; the one extended attempt allowed by D934)
Same model and 8 conditions as PREREG_D934 (W, dW/dU1, dW/dU2, dW/dS, dW/dU3, d2W/dU1dU3, d2W/dU2dU3, d2W/dSdU3 at P=(U1,U2,S), linear in the 16 real flux numbers).
Part A (rho grid): each of U1, U2, S from {rho=(-1+i sqrt3)/2, rho+1, i sqrt3/2, i sqrt3, 1/2+i sqrt3/2, i, 2i}; record the numeric nullity (SVD, sigma < 1e-9) at all 343 points.
Part B (continuous): minimise r = sigma_min/sigma_max of the 16x16 real matrix over Re in [-0.5,0.5], Im in [0.2,5] for each of U1, U2, S (6 real parameters); 200 random starts (seed 935), Nelder-Mead, bounds by clipping.
Outcome rules (fixed now):
- ZEROS EXIST if min r < 1e-10 anywhere (A or B) -> F1 continues (integer search at that locus, new lock).
- NO ZEROS FOUND if min r > 1e-4 over all starts -> F1 killed: record "no point-wise flat single U on T^6/(Z2xZ2) in the sampled domain"; Project F switches to the sibling catalogue.
- In between: inconclusive; report min r and its location; no rerun.
Script theory/flux/flat_u_det_d935.py; output field_tests/results/flat_u_det_d935.txt.
