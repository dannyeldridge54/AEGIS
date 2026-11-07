"""Low-energy QCD-anomaly scale and equality-era estimate for the BI pseudoscalar.

The leading periodic approximation is V(phi) = chi_QCD * [1 - cos(phi/F_phi)].
The estimates do not identify the BI field with AEGIS's separate n=3,
equality-locked EDE ansatz and are not a thermal QCD likelihood calculation.
"""
import math


def calculate(
    qcd_susceptibility_quarter_gev=75.6e-3,
    reduced_planck_mass_gev=2.435e18,
    decay_constant_gev=2.0e18,
    hubble_equality_ev=2.50e-28,
    equality_temperature_ev=0.8,
    relativistic_dof_oscillation=10.75,
    entropy_dof_oscillation=10.75,
    entropy_dof_equality=3.91,
    target_equality_fraction=0.05,
):
    """Evaluate the leading-order scales for explicit physical inputs."""

    physical_inputs = {
        "qcd_susceptibility_quarter_gev": qcd_susceptibility_quarter_gev,
        "reduced_planck_mass_gev": reduced_planck_mass_gev,
        "decay_constant_gev": decay_constant_gev,
        "hubble_equality_ev": hubble_equality_ev,
        "equality_temperature_ev": equality_temperature_ev,
        "relativistic_dof_oscillation": relativistic_dof_oscillation,
        "entropy_dof_oscillation": entropy_dof_oscillation,
        "entropy_dof_equality": entropy_dof_equality,
    }
    for name, value in physical_inputs.items():
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or value <= 0:
            raise ValueError(f"{name} must be finite and positive")
    if (isinstance(target_equality_fraction, bool)
            or not isinstance(target_equality_fraction, (int, float))
            or not math.isfinite(target_equality_fraction)
            or not 0 < target_equality_fraction < 1):
        raise ValueError("target_equality_fraction must be finite and strictly between zero and one")

    susceptibility_gev4 = qcd_susceptibility_quarter_gev**4
    mass_gev = math.sqrt(susceptibility_gev4) / decay_constant_gev
    mass_ev = mass_gev * 1e9
    oscillation_hubble_gev = mass_gev / 3
    radiation_hubble_coefficient = math.sqrt(math.pi**2 * relativistic_dof_oscillation / 90)
    oscillation_temperature_gev = math.sqrt(
        oscillation_hubble_gev * reduced_planck_mass_gev / radiation_hubble_coefficient
    )
    equality_growth = (
        oscillation_temperature_gev * 1e9 / equality_temperature_ev
        * (entropy_dof_oscillation / entropy_dof_equality) ** (1 / 3)
    )
    oscillation_density_gev4 = (
        3 * reduced_planck_mass_gev**2 * oscillation_hubble_gev**2
    )
    susceptibility_fraction_at_oscillation = (
        susceptibility_gev4 / oscillation_density_gev4
    )
    theta_for_target_fraction = math.sqrt(
        4 * target_equality_fraction
        / (susceptibility_fraction_at_oscillation * equality_growth)
    )

    return {
        "potential": "V(phi) = chi_QCD * [1 - cos(phi / F_phi)]",
        "potential_status": "leading periodic low-energy approximation; bounded below",
        "input_parameters": {
            "qcd_susceptibility_quarter_GeV": qcd_susceptibility_quarter_gev,
            "reduced_planck_mass_GeV": reduced_planck_mass_gev,
            "F_phi_GeV": decay_constant_gev,
            "H_equality_eV": hubble_equality_ev,
            "T_equality_eV": equality_temperature_ev,
            "g_star_oscillation": relativistic_dof_oscillation,
            "g_star_s_oscillation": entropy_dof_oscillation,
            "g_star_s_equality": entropy_dof_equality,
            "target_total_fraction_at_equality": target_equality_fraction,
        },
        "qcd_susceptibility_quarter_MeV": qcd_susceptibility_quarter_gev * 1e3,
        "qcd_susceptibility_GeV4": susceptibility_gev4,
        "F_phi_GeV": decay_constant_gev,
        "F_phi_reduced_planck": decay_constant_gev / reduced_planck_mass_gev,
        "mass_from_susceptibility_eV": mass_ev,
        "mass_over_H_equality": mass_ev / hubble_equality_ev,
        "oscillation_condition": "3 H = m_phi",
        "radiation_dominated_oscillation_temperature_MeV": oscillation_temperature_gev * 1e3,
        "a_equality_over_a_oscillation": equality_growth,
        "rho_susceptibility_over_background_at_oscillation": susceptibility_fraction_at_oscillation,
        "initial_angle_for_target_total_fraction_at_equality_rad_harmonic_estimate": theta_for_target_fraction,
        "target_total_fraction_at_equality": target_equality_fraction,
        "oscillation_angle_approximation": "rho_phi ~= chi_QCD * theta_i^2 / 2 for theta_i << 1",
        "post_oscillation_equation_of_state": 0.0,
        "post_oscillation_interpretation": "harmonic oscillations redshift as matter, not transient n=3 EDE",
        "equality_Hubble_eV": hubble_equality_ev,
        "equality_temperature_eV": equality_temperature_ev,
        "derivation": [
            "chi_QCD = (chi_QCD^(1/4))^4",
            "m_phi^2 = V''(0) = chi_QCD / F_phi^2",
            "H_osc = m_phi / 3",
            "H_rad(T) = sqrt(pi^2 g_star / 90) * T^2 / M_Pl,reduced",
            "a_eq/a_osc = (T_osc/T_eq) * (g_star_s,osc/g_star_s,eq)^(1/3)",
            "rho_bg,osc = 3 M_Pl,reduced^2 * H_osc^2",
            "Omega_phi,eq ~= (1/2) * [chi_QCD/rho_bg,osc] * (theta_i^2/2) * (a_eq/a_osc)",
        ],
        "assumptions": [
            "The BI pseudoscalar couples to the QCD axial anomaly as in the Nieh-Yan model.",
            "The zero-temperature QCD susceptibility fourth root is approximated as 75.6 MeV.",
            "The oscillation-temperature estimate assumes radiation domination and uses fixed relativistic degrees of freedom.",
            "The equality fraction estimate uses harmonic small-angle evolution after 3H = m_phi.",
            "The factor 1/2 converts the scalar-to-radiation ratio at equality to a fraction of total density when matter and radiation are equal.",
            "The published BI field normalization is not assumed identical to the separate AEGIS arsinh field map.",
        ],
        "references": [
            "Mercuri and Taveras, arXiv:0903.4407, especially Eqs. (20)-(31).",
            "Lu et al., arXiv:2003.01625, QCD theta-vacuum energy and axion properties.",
        ],
    }


if __name__ == "__main__":
    import json

    print(json.dumps(calculate(), indent=2))
