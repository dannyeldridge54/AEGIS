"""Bounded hidden-confinement axion toy on the saved UFE equality background.

This is a sensitivity calculation, not a UFE derivation or a fit. It uses
V = chi(T_h) * (1 - cos(theta)), theta = 9 phi / s, F = s / 9. The unknown
low-temperature mass scale and hidden confinement temperature are supplied as
dimensionless grid values. The saved fitted phase is imposed initially.
"""

from math import cos, exp, log, pi, sin, sqrt

from scipy.integrate import solve_ivp


# Saved Planck + DESI + Pantheon+ free-EDE background values.
OMEGA_B_H2 = 0.022638271592185517
OMEGA_C_H2 = 0.1269348874535147
H = 0.70776
N_EFF = 3.044
T_CMB0_EV = 2.34865e-4
MPL_EV = 2.435e27
H100_EV = 100.0 * 3.240779289e-20 * 6.582119569e-16
OMEGA_R_H2 = 2.4728e-5 * (1.0 + 0.22711 * N_EFF)
OMEGA_M_H2 = OMEGA_B_H2 + OMEGA_C_H2
A_EQ = OMEGA_R_H2 / OMEGA_M_H2
Z_EQ = 1.0 / A_EQ - 1.0
OMEGA_M = OMEGA_M_H2 / H**2
OMEGA_R = OMEGA_R_H2 / H**2
H_EQ_EV = H * H100_EV * sqrt(OMEGA_R / A_EQ**4 + OMEGA_M / A_EQ**3)
T_GAMMA_EQ_EV = T_CMB0_EV / A_EQ

S_MPL = sqrt(1.5)
F_MPL = S_MPL / 9.0
THETA_FIT = 2.784071586852119
F_EDE_TARGET = 0.08572528095614122
SUSCEPTIBILITY_POWER = 4.0
X_INITIAL = 0.01
RTOL = 2e-9
ATOL = 1e-11
MAX_STEP = 0.002


def background_h(x):
    """H(x)/H_eq in a radiation + matter background, normalized at equality."""
    return sqrt(0.5 * (x**-4 + x**-3))


def dlnh_dlnx(x):
    rad = x**-4
    matter = x**-3
    return 0.5 * (-4.0 * rad - 3.0 * matter) / (rad + matter)


def susceptibility_ratio(x, tc_over_th_eq):
    # T_h/T_c = 1/(x * (T_c/T_h,eq)); saturate below confinement.
    return min(1.0, x * tc_over_th_eq) ** SUSCEPTIBILITY_POWER


def evolve(mu0_over_heq, tc_over_th_eq):
    """Integrate the homogeneous field in N=ln(a/a_eq), without backreaction."""
    def rhs(n, state):
        x = exp(n)
        h_ratio = background_h(x)
        chi_ratio = susceptibility_ratio(x, tc_over_th_eq)
        mass_over_h_sq = mu0_over_heq**2 * chi_ratio / h_ratio**2
        theta, theta_n = state
        return (
            theta_n,
            -(3.0 + dlnh_dlnx(x)) * theta_n - mass_over_h_sq * sin(theta),
        )

    sol = solve_ivp(
        rhs,
        (log(X_INITIAL), 0.0),
        (THETA_FIT, 0.0),
        method="DOP853",
        rtol=RTOL,
        atol=ATOL,
        max_step=MAX_STEP,
    )
    if not sol.success:
        raise RuntimeError(sol.message)

    theta_eq, theta_n_eq = sol.y[:, -1]
    chi_eq = susceptibility_ratio(1.0, tc_over_th_eq)
    # rho_phi/(3 M_Pl^2 H_eq^2); H is the fixed background value at equality.
    rho_phi_over_bg = (
        F_MPL**2
        * (mu0_over_heq**2 * chi_eq * (1.0 - cos(theta_eq)) / 3.0
           + theta_n_eq**2 / 6.0)
    )
    f_phi_eq = rho_phi_over_bg / (1.0 + rho_phi_over_bg)
    return theta_eq, theta_n_eq, mu0_over_heq * sqrt(chi_eq), f_phi_eq


def target_normalization_mu(tc_over_th_eq):
    """Low-T mass ratio required for target f if the field is still frozen."""
    u = 1.0 - cos(THETA_FIT)
    chi_eq_ratio = susceptibility_ratio(1.0, tc_over_th_eq)
    mu_eq = sqrt(
        3.0 * F_EDE_TARGET / ((1.0 - F_EDE_TARGET) * F_MPL**2 * u)
    )
    return mu_eq / sqrt(chi_eq_ratio), mu_eq


def main():
    print(f"a_eq={A_EQ:.9g}  z_eq={Z_EQ:.3f}  T_gamma_eq={T_GAMMA_EQ_EV:.4f} eV")
    print(f"H_eq={H_EQ_EV:.5e} eV  F=s/9={F_MPL:.8f} M_Pl")
    print(f"imposed theta_i={THETA_FIT:.6f} rad ({THETA_FIT / pi:.5f} pi)")
    print(
        f"frozen-field normalization for saved free-fit f_EDE={F_EDE_TARGET:.6f}: "
        f"m_eq/H_eq={target_normalization_mu(1.0)[1]:.5f} "
        "(conditional target, not a prediction)"
    )
    mu_eq_target = target_normalization_mu(1.0)[1]
    chi_eq_target_ev4 = (
        mu_eq_target * H_EQ_EV * F_MPL * MPL_EV
    ) ** 2
    print(
        "same conditional normalization: "
        f"chi_eq^(1/4)={chi_eq_target_ev4**0.25:.5f} eV"
    )
    print("mu0/H_eq  Tc/Th_eq  x(T=Tc)  m_eq/H_eq  theta_eq  dtheta/dln(a)  f_phi_eq")
    for mu0 in (1.0, 2.8, 5.0):
        for tc_ratio in (0.5, 1.0, 2.0):
            theta, theta_n, mu_eq, f_phi = evolve(mu0, tc_ratio)
            x_cross = 1.0 / tc_ratio
            print(
                f"{mu0:8.3f}  {tc_ratio:9.3f}  {x_cross:8.3f}  "
                f"{mu_eq:9.3f}  {theta:8.5f}  {theta_n:14.6g}  {f_phi:9.5f}"
            )
    print("required low-T mass ratios if frozen at theta_i, by Tc/Th_eq:")
    for tc_ratio in (0.5, 1.0, 2.0):
        mu0, mu_eq = target_normalization_mu(tc_ratio)
        print(
            f"  Tc/Th_eq={tc_ratio:.3f}: m_eq/H_eq={mu_eq:.5f}, "
            f"m0/H_eq={mu0:.5f}"
        )


if __name__ == "__main__":
    main()
