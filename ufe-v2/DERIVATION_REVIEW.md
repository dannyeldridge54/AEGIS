# UFE physics derivation review

**Scope.** Local review of the action, hypothesis, preregistrations, paper, and saved fit outputs in this worktree, followed by a focused check of primary literature on scalarized Holst and Nieh–Yan models. No private repository data was sent externally; no fits or long-running jobs were run.

## Result in brief

The local model does **not** derive either the radiation-fed hold/release mechanism or the integer width \(N=9\). It does contain a valid algebraic correspondence between a chosen hold coefficient and an angle near the fitted value. That correspondence is not a prediction until the coefficient, its cosmological source, and the field's time evolution are supplied. Likewise, the torsion field redefinition fixes a normalization scale, but not a compact period or an anomaly integer.

**Evidence provenance:** the action and hypothesis are in `ufe-v2/`, but its `results_v2.json` contains only LCDM and LegacyBeta; it has no torsion-EDE likelihood result. The preregistrations and run JSON cited below are present in the separate top-level `cmb-fit/` directory, not under `ufe-v2/cmb-fit/`. Its README describes CAMB `EarlyQuintessence`/Cobaya results. I used the saved summaries and selected saved run minima as recorded evidence, but did not rerun or independently reproduce those fits. In particular, the N-profile width is reported in the paper, while the raw scan points were not among the selected artifacts inspected here. Treat those fit-based statements as claims supported by local records, not as a computation from the UFE engine in this folder.

## 1. Hold and release near equality

The paper derives the canonical kinetic term and field redefinition
\[
\phi=s\,\operatorname{arsinh}(1/\gamma),\qquad s=\sqrt{3/2}\,M_{\rm Pl},
\]
then explicitly assumes \(V=\Lambda^4[1-\cos(\phi/F)]^3\). The proposed hold term is not in that action or the implemented field equation (`papers/torsion_born_ede.tex`, §§2–4; `ufe-v2/aegis/cosmo_v2.py`, `TorsionField`). It is introduced only as a hypothesis in `ufe-v2/hypotheses/HOLD_RELEASE.md`.

The hypothesis's static algebra is internally checkable. Write \(u=1-\cos\theta\), where \(\theta=(\phi-\phi_0)/F\) is the potential phase (with any shift \(\phi_0\) suppressed in the hypothesis notation), and, in units of \(\Lambda^4\), \(U(u)=u^3-\kappa u\). Then
\[
\frac{dU}{d\theta}=(3u^2-\kappa)\sin\theta,\qquad
U''(\pi)=\kappa-12.
\]
Thus \(\theta=\pi\) is a local minimum for \(\kappa>12\), marginal at 12, and unstable below 12. For \(0<\kappa<12\), off-peak stationary minima satisfy \(u=\sqrt{\kappa/3}\). At the *chosen* value \(\kappa=11.25\),
\[
\theta_*=\arccos\!\left(1-\sqrt{11.25/3}\right)=2.783\ {\rm rad}\simeq0.886\pi.
\]
This reproduces the fitted angle numerically, but it does not derive \(\kappa=11.25\); that value was selected by inverting the desired angle.

There is also a threshold mismatch in the proposed clock. If \(\kappa\) is proportional only to \(\alpha\rho_r-\beta\rho_m\), then \(\rho_r/\rho_m=\beta/\alpha\) marks where that difference is **zero**. The hilltop loses stability at \(\kappa=12\), not at zero. At equality, \(\rho_r=\rho_m\), and for \(\alpha=\beta\) the difference vanishes; it is not 12. An additive offset or a specified normalization and scale-dependent term could move the \(\kappa=12\) crossing to equality, but none is fixed in the supplied model. The densities alone therefore do not establish the proposed release clock.

Nor does a static minimum establish the release angle dynamically. One must specify \(\kappa(a)\), its normalization and any offset, then solve the sourced Klein–Gordon equation. Near the threshold the curvature, and hence the effective oscillation frequency, tends to zero, so adiabatic tracking through the transition cannot simply be presumed. An exactly symmetric field placed at \(\pi\) also remains there in the classical equation absent a perturbation/seed. If \(\kappa\) varies externally, the scalar continuity equation has a source,
\[
\dot\rho_\phi+3H(\rho_\phi+p_\phi)=-\dot\kappa\,u
\]
(with dimensionful \(\kappa\)); the action must specify where the compensating energy transfer goes. No such coupled matter/radiation dynamics or seed is supplied.

**What the saved fits establish:** the free Planck run `cmb-fit/results/cmp_edeP.json` has \(\theta_i=2.7841\). The preregistered fixed-angle runs give \(\Delta\chi^2=+5.68\) at \(2.00\) and \(+4.22\) at \(1.50\) relative to that minimum (`cmp_th2.00.json`, `cmp_th1.50.json`), supporting a near-hilltop fit preference within this phenomenological model. The fit preference is not a derivation of the hold mechanism or of the angle. The locked onset itself is explicitly acknowledged as phenomenological and selected after the free fit in `PREREGISTRATION_ZEQ.md` and the paper's §3.

**Conclusion:** the numerical coincidence \(\kappa=11.25\to\theta_*\simeq\theta_i\) is valid algebra, but the radiation-fed/matter-drained mechanism and equality release remain un-derived. Needed inputs are the actual interaction/action producing \(\kappa\), its coefficient and additive scale, the associated energy-transfer equations, and initial perturbation/seed plus a dynamical solution.

### What the stated Holst–fermion coupling actually implies

The paper identifies the fermion term schematically as \(C(\phi)\partial_\mu\phi\,J_5^\mu\), with \(C\) fixed by the Holst/torsion elimination, and explicitly leaves its calculation open. Varying this interaction together with a canonical scalar gives, up to the overall sign convention for the interaction,
\[
\Box\phi-V_{,\phi}-C(\phi)\nabla_\mu J_5^\mu=0.
\]
The terms proportional to \(C_{,\phi}\partial_\mu\phi J_5^\mu\) cancel in the variation; equivalently, defining \(B(\phi)=\int^\phi C(\varphi)d\varphi\), integration by parts gives \(-B(\phi)\nabla_\mu J_5^\mu\) up to a boundary term. For constant \(C\), this is \(-C\phi\nabla_\mu J_5^\mu\). In a homogeneous isotropic universe, \(J_5^\mu=(n_5,0,0,0)\), and \(\nabla_\mu J_5^\mu=\dot n_5+3Hn_5\). If the axial charge is conserved, \(n_5\propto a^{-3}\) and this source is zero: the derivative interaction is a boundary term and gives no hold force. If it is not conserved, its divergence must be calculated from the fermion masses, gauge anomalies, and state; the local files specify none of these. In particular, total radiation energy density and total matter density are not the axial-current divergence.

This is a no-go for deriving the proposed hold **from the supplied interaction alone**: the action has no term whose stated variation yields \(W=-\Lambda^4\kappa(a)(1-\cos\theta)\). To obtain that term one must provide a nonzero microscopic operator expectation with a specified \(\phi\)-dependent coupling and show that its finite-density/temperature evolution gives the required function. Merely saying “axial current” does not fix that expectation, its sign, its normalization, or its time dependence.

There is a second model-independent condition. For the assumed effective potential \(U=(1-\cos\theta)^3-\kappa(1-\cos\theta)\), hilltop stability changes at \(\kappa=12\), while the static off-peak minimum \(\theta=2.783\) corresponds to \(\kappa=11.25\). Therefore the transition that removes hilltop stability and the point at which the desired off-peak value is a minimum are distinct. If the desired angle is required at equality, the coefficient must already have fallen below 12 before equality and the field must roll far enough in the intervening time. Near \(\kappa=12\), the local curvature and relaxation frequency vanish, so quasi-static tracking necessarily breaks down at the critical point; it cannot be invoked there without solving the dynamics. The six-run test above shows that the chosen short lead time and the stated target-point scale do not supply that roll.

**Minimal information that would make the next derivation well-posed:** (1) the full fermion action and spin-connection coupling, including species, masses, gauge representations, and axial charges; (2) the axial-charge initial conditions/chemical potentials and collision or equilibration history; (3) the anomaly equation and regulator/topological normalization, if an anomalous source is intended; (4) a finite-temperature/density effective action derived from those fields, including its \(\phi\)-dependent free energy and energy-transfer equations; and (5) a seed or perturbation prescription for departure from the exactly symmetric hilltop. Without these, fitting a \(\kappa(a)\) profile would introduce free physical input rather than improve the derivation.

### Literature-based candidate check: the Nieh–Yan Immirzi axion

The closest explicit microscopic candidate found is not the local model's Holst scalar action, but the distinct Nieh–Yan extension studied by Mercuri and Taveras. Their construction yields a canonical pseudoscalar with a derivative axial-current coupling; chiral rotation moves this coupling into fermion mass phases and the quantum anomaly generates gauge/Pontryagin couplings. In their QCD example, the low-energy quark mass terms generate a BI-field mass \(m_\phi\simeq3.0\times10^{-12}\,\mathrm{eV}\), with interaction scale \(F_\phi\simeq2.0\times10^{18}\,\mathrm{GeV}\) [Mercuri & Taveras, arXiv:0903.4407, §§II–IV](https://arxiv.org/abs/0903.4407). This is a concrete anomaly-induced potential mechanism, not merely a fitted \(\kappa(a)\); however, it changes the gravitational action to a field multiplying the Nieh–Yan invariant and does not derive the AEGIS cubic cosine or its \(N=9\).

Recomputing from the saved free-fit Planck values in `anomaly_toy.py` gives \(H_{\rm eq}=2.50\times10^{-28}\,\mathrm{eV}\) (the earlier \(3.53\times10^{-28}\,\mathrm{eV}\) estimate in this report was erroneous). Thus the published QCD-induced mass is \(m_\phi/H_{\rm eq}\simeq1.20\times10^{16}\). In radiation domination, \(H\propto a^{-2}\), so \(H\sim m_\phi\) at roughly \(a/a_{\rm eq}\simeq\sqrt{H_{\rm eq}/m_\phi}\simeq9.1\times10^{-9}\), or \(z\sim3.9\times10^{11}\), not near equality. This rules out that specific minimal QCD-anomaly mass as the mechanism that keeps the field frozen until equality, absent an additional suppression/hold sector. The AEGIS assumed-potential target's characteristic hilltop curvature scale \(\sqrt{12}\Lambda^2/F\sim2.7\times10^{-27}\,\mathrm{eV}\) for \(\Lambda=0.510\) eV and \(F=s/9\) is about \(11H_{\rm eq}\); its scale is equality-relevant, but its origin remains unspecified.

The same literature distinguishes the models: Taveras & Yunes' scalarized Holst action yields kinetic dynamics with **no potential** at the classical level [arXiv:0807.2652](https://arxiv.org/abs/0807.2652); Mercuri's topological/Nieh–Yan interpretation and anomaly proposal is a separate extension [arXiv:0902.2764](https://arxiv.org/abs/0902.2764). Kaul & Sengupta discuss quantized Nieh–Yan indices in an axionic first-order gravity/wormhole construction [arXiv:1411.4793](https://arxiv.org/abs/1411.4793), but this does not calculate the AEGIS potential's Fourier coefficient or establish \(N=9\). These sources support a possible *route* to a potential, not a derivation of the claimed EDE model or equality clock.

### Astrophysical/theory analogues and the most defensible next direction

1. **Hilltop EDE is established phenomenology, not a torsion fingerprint.** Poulin et al. use \(V\propto[1-\cos(\phi/f)]^n\) (including \(n=3\)); the field is initially Hubble-frozen and later rolls when \(H\) becomes comparable to its effective mass. Their preferred EDE phenomenology has a roughly 5% energy fraction near \(z\sim5000\), with the initial field value and critical epoch specified/fitted as model parameters rather than dynamically generated by torsion [arXiv:1811.04083, *Phys. Rev. Lett.* 122, 221301](https://arxiv.org/abs/1811.04083). This is close to the UFE assumed background shape, but it does not identify matter-radiation equality as the trigger; a near-\(\pi\) fit by itself cannot support the torsion origin.

2. **A genuine dynamical hilltop exists in axion model-building, but by a different mechanism.** Co, Gonzalez & Harigaya's DAMP\(_\pi\) construction first makes the axion heavy enough to relax to an early minimum, then shifts the minimum by \(\pi\) through a change in competing CP-sensitive contributions. This relies on explicit supersymmetric/Higgs/inflaton and CP-sector assumptions; it does not predict matter-radiation equality as the transition [arXiv:1812.11192, *JHEP* 05 (2019) 163](https://arxiv.org/abs/1812.11192). This is a useful conceptual lead: derive a moving minimum from competing physical terms, rather than postulate \(\kappa(a)\). With CP-conserving relative phase \(0\) or \(\pi\), the minima are exactly aligned or opposite; the mechanism naturally targets \(\pi\), not the UFE value \(0.886\pi\). An intermediate angle would need a calculable phase or a dynamically demonstrated lag, not a selected offset.

3. **Thermal friction is a real alternative to a potential hold, but it does not select an angle.** Choi et al. derive \(\ddot\phi+(3H+\gamma_\phi)\dot\phi+V_{,\phi}=0\) from an axion coupling to a thermalized hidden Yang–Mills sector, with \(\gamma_\phi\sim(N\alpha_h)^5T_h^3/f_h^2\); the hidden bath and its energy transfer are explicit [arXiv:2206.01462, *JHEP* 02 (2023) 180](https://arxiv.org/abs/2206.01462). This is damping, not a hilltop potential or equality clock by itself: it can delay/alter motion but supplies no special \(\theta=0.886\pi\). A hidden bath becoming relevant at equality would be a new sector and would require temperature-ratio, entropy, radiation-density and perturbation constraints.

**Most defensible theory direction:** if the goal is a derived hilltop-like start, investigate a two-source, temperature-dependent axion potential as an explicit *extension*:
\[
V(\theta,T_A,T_B)=\chi_A(T_A)[1-\cos\theta]
 +\chi_B(T_B)[1-\cos(\theta-\delta)],\qquad \theta=\phi/f.
\]
This is the generic leading-harmonic form when two sectors with distinct CP phases generate a periodic potential. Its instantaneous minimum and curvature follow without fitting a hold coefficient:
\[
\theta_{\min}=\operatorname{atan2}\!\left(\chi_B\sin\delta,\,
\chi_A+\chi_B\cos\delta\right),\qquad
m_{\rm eff}^2=\frac{\sqrt{\chi_A^2+\chi_B^2+2\chi_A\chi_B\cos\delta}}{f^2}.
\]
For \(\delta=\pi\), the minimum jumps between 0 and \(\pi\) when the susceptibilities cross, and \(m_{\rm eff}\to0\) at the crossing. This provides a mathematically well-defined way to test a moving-minimum/critical-release idea. But it does **not** solve UFE as written: \(\chi_A,\chi_B,\delta\), their temperature evolution and energy exchange must come from specified sectors. A crossing at equality must be predicted by those independent susceptibilities, not defined by setting their crossing temperature to \(T_{\rm eq}\); and this leading-harmonic potential is not the assumed cubic cosine.

The visible photon temperature at the saved equality redshift is only \(T_\gamma\simeq0.84\) eV. Thus any thermal-sector explanation tied to equality needs an eV-scale transition in the visible bath or a specified hidden-to-visible temperature ratio that yields it. No such eV-scale sector, susceptibility, or phase structure appears in the supplied UFE action or local records. The next valid calculation is therefore **conditional**, not another parameter scan: first name the two sectors and give their Lagrangians, anomaly coefficients, mass spectra, CP phases, thermal susceptibilities \(\chi_i(T_i)\), and entropy/energy-transfer equations; preregister the predicted crossing redshift and \(\theta_{\min}(T)\); then integrate the scalar plus bath with no fitted \(\theta_i\) or \(z_c\). Falsify if the independently calculated crossing misses equality, if the evolving field does not reach the stated misalignment without tuning initial conditions, or if the required bath violates expansion/perturbation constraints. Until those inputs exist, there is no non-arbitrary numerical evolution to run.

**What this comparison points to:** the nearest viable *architecture* is an explicitly specified axion/anomaly sector whose temperature-dependent competing contributions predict a moving minimum, potentially supplemented by a separately modeled thermal bath. The literature demonstrates these ingredients in other theories, not in UFE. In particular, standard EDE is phenomenology; DAMP\(_\pi\) requires its own SUSY/Higgs/inflaton CP-sector; thermal friction requires its hidden bath and transfer equations; and the Nieh–Yan construction is a distinct action from scalarized Holst. None supplies the missing UFE coupling, equality trigger, or angle derivation. Such mechanisms must not be transplanted automatically or used to relabel an extension as a result of the current Holst-only setup.

### Best explicit toy ansatz to test (speculative; do not adopt as model physics)

The simplest background-level coefficient that both holds the hilltop in radiation domination and gives the fitted static angle at equality is
\[
\kappa(a)=11.25+g\,\frac{\rho_r(a)-\rho_m(a)}{\rho_{\rm eq}},\qquad
\rho_{\rm eq}\equiv\rho_r(a_{\rm eq})=\rho_m(a_{\rm eq}).
\]
This makes \(\kappa(a_{\rm eq})=11.25\) by construction, hence \(\theta_*(a_{\rm eq})=2.783\). With \(x=a/a_{\rm eq}\), the hilltop threshold \(\kappa=12\) is crossed when \(g(x^{-4}-x^{-3})=0.75\): \(g\simeq12.2\) places it at \(x=0.95\), and \(g\simeq72\) at \(x=0.99\). These are illustrative dimensionless choices for transitions about 5% or 1% before equality, not estimates measured by the fits. The offset 11.25 and equal radiation/matter coefficients are tuned assumptions; no local action generates them. The ansatz is useful precisely because it can fail a dynamical test, not because it solves the physical-origin problem.

For the width, one concrete *UV sketch* is a hidden confining gauge sector with an anomalous coupling \(C_A x Q\), where \(x=\phi/s\), \(Q\) is normalized to integer topological charge, and \(C_A=9\). Its instanton potential could contain \(\chi_h(T_h)[1-\cos(9x)]\), giving the effective cosine width \(F=s/9=0.13608\,M_{\rm Pl}\). A coefficient of nine could, for example, be engineered from nine unit-anomaly Dirac species in a specified representation; it does not follow from three generations times three colors, nor is such a sector present in the supplied action. It also gives a cosine, not automatically the fitted cubic shape \([1-\cos(\phi/F)]^3\). To make an onset near equality, this sketch additionally needs hidden-sector temperature and susceptibility such that the potential becomes dynamically important near \(z_{\rm eq}\sim3.55\times10^3\); the paper's target-point potential scale is about \(0.51\) eV. These extra choices are free inputs, not consequences of the anomaly. This is a candidate to sharpen or reject, not a claim that the hidden sector exists.

### Bounded anomaly-potential calculation (single-harmonic prototype; not a fit)

To turn that UV sketch into a calculable toy without pretending the missing sector is known, I added `ufe-v2/anomaly_toy.py`. Start with a hidden topological density \(Q_h=(g_h^2/32\pi^2)G_h\widetilde G_h\), normalized so \(\int Q_h\) is integer, and an interaction
\[
\mathcal L\supset (C_A\phi/s)Q_h,\qquad s=\sqrt{3/2}\,M_{\rm Pl}.
\]
If the hidden vacuum energy is dominated by its first Fourier harmonic, the finite-temperature effective potential is
\[
V_h(\phi,T_h)=\chi_h(T_h)\left[1-\cos(C_A\phi/s+\delta)\right],\quad
m_{\rm amp}^2(T_h)=\frac{C_A^2\chi_h(T_h)}{s^2}.
\]
Here \(\chi_h=\partial^2 E_{\rm vac}/\partial\vartheta_h^2|_{\vartheta_h=0}\) is the topological susceptibility. For integer \(C_A\), the period is \(2\pi s/C_A\), so the cosine width is \(F=s/C_A\). Thus a separately calculated anomaly coefficient \(C_A=9\) would remove the *phenomenological width setting* by predicting \(F=s/9\); it does not follow from the Holst field redefinition. The coupling convention, chiral charges/representations and any fermion masses are needed to calculate \(C_A\). Higher Fourier harmonics near strong confinement, or a non-cosine vacuum-energy function, also require a microscopic calculation; the first-harmonic form is an ansatz, not guaranteed near \(T_c\).

The cited source chain has a strict boundary: the scalarized Holst result supplies a canonical kinetic degree of freedom but no classical \(V(\phi)\); the Nieh–Yan construction is a different action, and its fermion/chiral-anomaly coupling can transmit QCD's nonperturbative, periodic vacuum energy to the BI pseudoscalar. The cited QCD example gives a mass near a vacuum minimum, not the UFE cosine-cubed function, an eV susceptibility, a hidden confinement transition at equality, or \(C_A=9\). The assumed UFE shape itself contains several Fourier modes,
\[
[1-\cos\theta]^3=\frac52-\frac{15}{4}\cos\theta+\frac32\cos(2\theta)-\frac14\cos(3\theta),
\]
so a single leading-harmonic hidden instanton term does not reproduce it.

For the one-sector prototype I used \(C_A=9,\delta=0\), so \(\theta=C_A\phi/s\), and explicitly parameterized the missing susceptibility as
\[
\chi_h(T_h)=\chi_0\min[1,T_c/T_h]^4,\quad
\mu_0\equiv\frac{\sqrt{\chi_0}}{F H_{\rm eq}},\quad
\tau\equiv\frac{T_c}{T_{h,\rm eq}},\quad T_h/T_{h,\rm eq}=a_{\rm eq}/a.
\]
The power \(4\) and constant hidden-to-visible temperature ratio are illustrative placeholders, not values extracted from a gauge theory. The numerical background uses the saved free-fit \(\omega_b,\omega_c,h,N_{\rm eff}\), \(a_{\rm eq}=2.79616\times10^{-4}\), \(z_{\rm eq}=3575.335\), \(T_{\gamma,\rm eq}=0.8400\) eV, and, neglecting the immaterial equality-era cosmological constant, \(H_{\rm eq}=2.49525\times10^{-28}\) eV. The field starts at the *imposed* saved phase \(\theta_i=2.7840716\) with zero velocity at \(a/a_{\rm eq}=0.01\). The evolution solves
\[
\theta_{NN}+(3+d\ln H/dN)\theta_N+
\frac{\mu_0^2\,\min(1,\tau a/a_{\rm eq})^4}{(H/H_{\rm eq})^2}\sin\theta=0,\quad N=\ln(a/a_{\rm eq}),
\]
on the fixed radiation-plus-matter background. DOP853 used `rtol=2e-9`, `atol=1e-11`, `max_step=0.002`; four representative cases rerun at tighter tolerances changed \(\theta_{\rm eq}\) by at most \(7\times10^{-10}\) rad and \(f_{\phi,\rm eq}\) by at most \(3\times10^{-11}\). This is only nine bounded integrations, not a fit.

The algebra fixes a useful consistency scale independent of the toy grid. For an internally consistent comparison, use the exact saved free-fit phase \(\theta_i=2.7840716\) and \(f_{\rm EDE}=0.0857253\) from `cmb-fit/results/cmp_edeP.json`. If the field is still frozen at that phase, matching this saved target requires
\[
\frac{\rho_\phi}{3M_{\rm Pl}^2H_{\rm eq}^2}=
\frac{\chi_{\rm eq}(1-\cos\theta_i)}{3M_{\rm Pl}^2H_{\rm eq}^2}
=\frac{f_{\rm EDE}}{1-f_{\rm EDE}},
\quad \frac{m_{\rm amp,eq}}{H_{\rm eq}}=2.801,\quad
\chi_{\rm eq}^{1/4}=0.481\ {\rm eV}
\]
for \(F=s/9\). This is an amplitude *inferred from the UFE target*, not a hidden-sector prediction; it also shows that the target fraction implies \(m/H\) somewhat above the rough onset criterion \(m/H\sim1\). If \(\tau<1\), then equality is above the confinement temperature and \(\chi_{\rm eq}/\chi_0=\tau^4\), so the required low-temperature mass is larger by \(\tau^{-2}\). For example \(\tau=0.5\) requires \(\mu_0=11.20\), versus \(2.801\) for \(\tau\ge1\).

| \(\mu_0=m_0/H_{\rm eq}\) | \(\tau=T_c/T_{h,\rm eq}\) | \(m_{\rm amp,eq}/H_{\rm eq}\) | \(\theta_{\rm eq}\) (rad) | \(f_{\phi,\rm eq}\) |
|---:|---:|---:|---:|---:|
| 1.0 | 0.5 | 0.250 | 2.78374 | 0.00075 |
| 1.0 | 1.0 | 1.000 | 2.77876 | 0.01181 |
| 1.0 | 2.0 | 1.000 | 2.76589 | 0.01179 |
| 2.8 | 0.5 | 0.700 | 2.78147 | 0.00582 |
| 2.8 | 1.0 | 2.800 | 2.74134 | 0.08534 |
| 2.8 | 2.0 | 2.800 | 2.62896 | 0.08426 |
| 5.0 | 0.5 | 1.250 | 2.77576 | 0.01832 |
| 5.0 | 1.0 | 5.000 | 2.63884 | 0.22718 |
| 5.0 | 2.0 | 5.000 | 2.18239 | 0.21403 |

The \(\mu_0=2.8\) row is deliberately near the target-normalized \(2.801\), not independently predicted; its near-match to \(f_{\rm EDE}\) is therefore calibration, not evidence. The grid does show the conditional trends: \(\tau=0.5\) delays the susceptibility rise and misses the target fraction badly; \(\tau\ge1\) can yield the target-like fraction for the selected amplitude, while earlier turn-on (\(\tau=2\)) moves the field farther by equality. The angle was imposed as the initial condition, and the single cosine has its minimum at zero and hilltop at \(\pi\); it does not attract the field to \(0.886\pi\). With a two-sector potential, a desired moving minimum instead requires
\[
\chi_A\sin\theta+\chi_B\sin(\theta-\delta)=0,\qquad
\frac{\chi_B}{\chi_A}=\frac{\sin\theta}{\sin(\delta-\theta)},
\]
so the target angle fixes only a relation between the unknown susceptibility ratio and relative CP phase \(\delta\). It does not determine either one. The UFE locked summary reports a separate rounded target \(f_{\rm EDE}=0.078,\theta_i=2.77\); the prototype uses the exact *free* run's pair rather than mixing those summaries. Because \(\chi_h(T_h)\) was prescribed externally, the ODE's scalar energy is not separately conserved; a real model must include the hidden-bath energy transfer and perturbations. The fixed-background fraction is diagnostic only and includes no EDE backreaction.

**Minimum inputs needed to close this candidate:** a UV gauge group and matter/charge table to fix \(C_A\); the hidden gauge coupling/scale and spectrum to calculate \(T_c\) and \(\chi_h(T_h)\) (including its harmonics); the hidden-to-visible temperature ratio and entropy history; any relative CP phase if a second source is invoked; and a covariant energy-transfer/stress perturbation model. With those independently fixed, the falsifier is direct: calculate \(T_h(a)\), \(\chi_h(T_h)\), and \(m_{\rm amp}(a)/H(a)\) without setting them to equality, then integrate from a specified early state. Reject the candidate if its predicted onset is not near the claimed \(z_c\), or if its predicted misalignment and energy fraction at the prescribed epoch disagree with the saved UFE targets. No unique potential scale, equality trigger, initial angle, or \(C_A=9\) follows from the currently supplied action; this toy removes **zero** independent settings until those UV inputs are specified. Even a future UV derivation of \(C_A=9\) would remove the width setting only, not automatically the onset, amplitude, or initial-angle settings.

### Bounded ODE falsification test (completed)

Ran only the proposed fixed-background toy calculation; no fit or saved result was changed. The background used the saved free-fit Planck cosmology, \(\omega_b=0.0226383\), \(\omega_c=0.1269349\), \(h=0.70776\), plus \(\omega_r=2.4728\times10^{-5}(1+0.22711N_{\rm eff})\), \(N_{\rm eff}=3.044\). This gives \(a_{\rm eq}=2.7962\times10^{-4}\), \(z_{\rm eq}=3575.3\). Set \(x=a/a_{\rm eq}\), \(F=s/9=0.136083M_{\rm Pl}\), and \(\Lambda=0.510\) eV. Important qualification: the paper's cited \(n=3\) background target with \(\Lambda=0.510\) eV lists \(F=0.2139M_{\rm Pl}\), not \(s/9\); therefore the ODE used a deliberately speculative mixed parameter pair, not a saved best-fit pair. Moreover, the background held fixed was LCDM and omitted EDE backreaction. The numerical result below falsifies only this illustrative fixed-background ansatz/parameter choice; it is not a test of a self-consistent saved EDE best fit. The potential was
\[
\kappa(x)=11.25+g(x^{-4}-x^{-3}),\quad
U(\theta,x)=(1-\cos\theta)^3-\kappa(x)(1-\cos\theta).
\]
Integrated \(\theta''+(3+H'/H)\theta'+[3v_0/(F^2E^2)]\,\partial_\theta U=0\) in \(N=\ln a\) on the LCDM matter+radiation+\(\Lambda\) background, from \(x=0.1\) to 1.2. Here \(v_0=\Lambda^4/(3M_{\rm Pl}^2H_{100}^2)\), \(E=H/H_{100}\), and \(F\) is in \(M_{\rm Pl}\) units. Used DOP853, `rtol=2e-9`, `atol=1e-11`, `max_step=0.002` in \(N\); six runs, with \(\theta(0.1)=\pi-\delta\), \(\theta'(0.1)=0\), \(\delta=10^{-2},10^{-4},10^{-6}\), for each \(g=12.2,72\). These \(g\)'s were chosen to put the \(\kappa=12\) crossing near \(x=0.95,0.99\), respectively.

| \(g\) | \(\delta\) | \(x\) at \(\kappa=12\) | \(\theta(x=1)\) | \(\theta(x=1.2)\) |
|---:|---:|---:|---:|---:|
| 12.2 | \(10^{-2}\) | 0.9500 | 3.140643 | 3.137101 |
| 12.2 | \(10^{-4}\) | 0.9500 | 3.141583 | 3.141548 |
| 12.2 | \(10^{-6}\) | 0.9500 | 3.141593 | 3.141592 |
| 72 | \(10^{-2}\) | 0.9900 | 3.138357 | 3.140709 |
| 72 | \(10^{-4}\) | 0.9900 | 3.141560 | 3.141584 |
| 72 | \(10^{-6}\) | 0.9900 | 3.141592 | 3.141593 |

The static off-peak minimum at equality is \(2.783\) rad, but none of the six trajectories approaches it by equality: all end within 0.0033 rad of \(\pi\). For the two smaller seeds the field barely moves, and the displacement at equality scales strongly with the chosen seed. Thus the intended \(0.88\)–\(0.89\pi\) release snapshot is **not dynamically produced** by this calibrated toy ansatz on the selected background and potential scale. This particular parameterization fails that necessary test; the broader hold idea is not ruled out because its microscopic coupling and normalization were never derived. It is not a robust prediction: the angle is a static calibration, while the actual short crossing interval and finite roll time leave the field near the unstable point.

This fixed-background ODE remains a kinematic screening test, not a consistent model: the time-dependent external \(\kappa\) has no covariant source or compensating energy-transfer equation, and it ignores backreaction. The anomaly sketch remains untested; calculating \(C_A\) would first require a specified field/charge table, and checking the resulting potential's shape and susceptibility. Choosing nine in advance is not that calculation.

## 2. Does torsion derive \(N=9\)?

The canonical field relation gives the scale \(s=\sqrt{3/2}\,M_{\rm Pl}=1.2247\,M_{\rm Pl}\). If one **assumes** that \(x=\operatorname{arsinh}(1/\gamma)\) is compact with period \(2\pi\), then \(\phi=sx\) has period \(2\pi s\), corresponding to \(F=s\) in the assumed cosine potential. It does not imply \(F=s/9\). The redefinition maps a real \(\gamma\)-field coordinate monotonically to a real \(\phi\); it supplies no compact identification. A divisor of nine would require further structure, for example an explicitly derived \(\cos(9x)\) term or a justified smaller field identification.

The local action/paper does not give the requisite topological or anomaly calculation: there is no specified compact field space, instanton charge lattice and action, anomaly operator and normalization, or fermion representations/charges and couplings from which an integer could be computed. The paper itself labels the potential as assumed and the width origin as open. Fermion or color counts alone do not select an anomaly coefficient.

**What the saved fits establish:** the disclosed free-fit width \(F=0.13657\,M_{\rm Pl}\) gives \(s/F\simeq8.97\), but this is a fit-derived ratio, not a prediction. The paper reports a Planck width profile with a \(\Delta\chi^2=1\) half-width of 1.2 in \(N\), too broad to distinguish neighboring integers. It also reports P-ACT free-width \(N=8.0\), which does not meet the preregistered \(9\pm0.5\) pass band; the fixed-\(N=9\) fit does pass its separate fit-improvement test (\(\Delta\chi^2=-6.14\), \(\Delta{\rm AIC}=-4.14\)), which only shows that the imposed width can fit those data. Note: the preregistration calls values outside 8–10 a failure and values between that range and the pass band inconclusive, so exactly \(N=8.0\) is a boundary/inconclusive under that three-way wording, even though it fails the stated \(9\pm0.5\) pass criterion. Sources: `cmb-fit/PREREGISTRATION_N.md`, `PREREG_N_PACT.md`, `papers/torsion_born_ede.tex` §6, and the locked preregistration hashes in `cmb-fit/results/N_PACT_LOCK.json`.

**Conclusion:** the current evidence does not derive or establish \(N=9\). Needed inputs are a UV/topological action that fixes compactness and periodicity, the relevant fermion content and couplings, and an explicit anomaly/instanton calculation fixing the coefficient before fitting.

## Decision by derivation step

1. **Canonical field vs potential:** the Holst field redefinition and kinetic normalization \(s=\sqrt{3/2}M_{\rm Pl}\) are derived. The potential \(\Lambda^4[1-\cos(\phi/F)]^3\) is explicitly assumed. Scalarized Holst supplies no classical periodic potential; a Nieh–Yan plus anomaly/QCD route is a distinct extension and does not produce the UFE potential or its equality scale from the supplied action.
2. **Width:** \(F=s/C_A\) follows only after an anomaly coefficient \(C_A\) and the topological normalization are specified. No such matter/charge content or topological sector is supplied. Therefore \(N=C_A=9\) remains fit-compatible, not derived; current work removes no width setting.
3. **Equality lock/hold:** the given action has no radiation/matter-dependent term and supplies no \(\alpha,\beta\). The existing \(\kappa=12\) instability condition is algebraic, not a cosmological trigger; equality does not set its normalization. The anomaly toy shows the required scales conditionally but chooses its susceptibility law, \(T_c/T_{h,\rm eq}\), and amplitude. It removes no onset or amplitude setting.
4. **Initial phase:** no stated early-time boundary condition or force selects \(\theta_i\). The one-harmonic potential has a minimum at zero and a maximum at \(\pi\); the fitted \(0.886\pi\) is imposed in the prototype. A two-source potential only gives a relation between unknown relative phase and susceptibility ratio. Hence the angle is not derived.

**Best defensible result:** the requested mechanism is underdetermined by the supplied theory, not solved. The candidate's falsifier is now explicit: supply an independently specified UV sector (gauge group, charged matter, anomaly coefficient, \(\chi_h(T_h)\), \(T_c\), hidden/visible thermal history, and energy-transfer equations), then predict \(m_{\rm amp}/H\), release redshift, field phase and \(f_{\rm EDE}\) from fixed early data without fitting them. If those predictions miss the saved onset/phase/fraction or violate expansion and perturbation constraints, reject that sector. The only possible setting reduction is conditional: a UV-derived \(C_A\) would fix \(F\); if the same UV/thermal model also predicts the susceptibility history and initial state, it could remove onset/amplitude/phase settings. None of those reductions is presently established.
