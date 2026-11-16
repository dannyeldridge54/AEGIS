# PREREG D934: integer search for a point-wise flat single U on T^6/(Z2xZ2)
Locked before running. Follows D933.
Model: W(U1,U2,U3,S) = sum_k (f_k - S h_k) Pi_k, Pi = (1, U1, U2, U3, U2U3, U1U3, U1U2, U1U2U3), f,h in Z^8 (signs absorbed).
N_flux = sum over symplectic pairs (1<->U1U2U3, U1<->U2U3, U2<->U1U3, U3<->U1U2) of (f_k h_k' - f_k' h_k); overall sign is convention: report N and |N|.
Conditions at P = (U1*, U2*, S*): W, dW/dU1, dW/dU2, dW/dS, dW/dU3, d2W/dU1dU3, d2W/dU2dU3, d2W/dSdU3 all = 0 (16 real linear eqs). These make W = dW = 0 for every U3 (D933).
Grid: each of U1*, U2*, S* from {i, 2i, 3i, 1/2+i, 1+i, 1/2+i/2, 1/3+i, 2+i} (Gaussian rationals only; rho not included).
Method: exact rational nullspace (sympy) per grid point; integer combinations of nullspace basis with coefficients in [-2,2].
Accept a solution if: (f,h) != 0, 0 < |N_flux| <= 32, and the 3x3 matrix d2W/da db over a,b in {U1,U2,S} at (P, U3 = i) is nonsingular (U1,U2,S massive).
PASS: >= 1 accepted solution. FAIL: none on this grid (means "not found on grid", not a no-go).
Report: number of grid points with nonzero nullspace, number accepted, the smallest-|N| example.
Script: theory/flux/flat_u_d934.py; output field_tests/results/flat_u_d934.txt. No reruns to chase results; fixes only via DEVIATIONS written first.
