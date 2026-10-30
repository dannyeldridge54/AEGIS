# UFE three-track research rails

Status: local setup and bounded derivations only. No fit, web request, Ollama/model
call, training, or long-running process is authorized by this artifact. Work stays
inside this AEGIS worktree; saved runs and the primary checkout are read-only.

**Research provenance:** the existing `ufe-v2/DERIVATION_REVIEW.md` includes
external primary-literature research conducted in an earlier pass. That work is
reported as historical context, not as a result of the present offline setup.
This pass adds no literature sources and makes no network requests.

## Shared decision

The supplied theory does not yet predict the assumed cosine-cubed potential,
`N=9`, an equality-triggered hold/release, or the fitted hilltop initial angle.
The branch must preserve that negative conclusion unless new action-level inputs
close the derivations below. A fitted value, dimensional coincidence, or selected
ansatz is not a derivation.

## Track 1 — derive only what the torsion action contains

**Status: source derivation completed; potential-origin gap confirmed.**

Local source chain: `papers/torsion_born_ede.tex`, §§2–4, especially
`eq:canonical`, `eq:canonical_action`, `eq:V`, `eq:lock`, and `eq:kg`.

The local action eliminates algebraic torsion and gives a canonical pseudoscalar
with
\[
\phi=s\,\operatorname{arsinh}(1/\gamma),\qquad
s=\sqrt{3/2}\,M_{\rm Pl}.
\]
The resulting scalar action is canonical and has no potential. The paper explicitly
introduces
\[
V(\phi)=\Lambda^4[1-\cos((\phi-\phi_0)/F)]^n
\]
as its one assumed functional input. Neither the real-valued field redefinition nor
the kinetic normalization asserts compactness, periodicity, a topological charge
lattice, or a Fourier coefficient.

The paper also explicitly says the equality rule
\[
a_c=a_{\rm eq}=\frac{\omega_r}{\omega_b+\omega_c}
\]
is not derived. It reduces one phenomenological onset setting only after the rule
is imposed; it is not an output of the action. Its deep-radiation initial
conditions \(\phi=\phi_i,\phi'=0\) likewise leave \(\theta_i\) free.

**Rail / go condition:** any claim beyond these results must cite a term in the
specified action and show the variation, normalization and boundary conditions.
To derive a periodic potential, add a fully specified compact/topological sector
and calculate its vacuum energy. The cited Nieh–Yan/anomaly construction is a
different action, not an automatic consequence of this local Holst action.

**No-go with current inputs:** no unique `F`, `N`, `Lambda`, `n`, or `phi_i` follows.
`N=9` is a fit-compatible hypothesis. A future integer anomaly coefficient could
fix a cosine period only if the coupling and topological normalization are derived;
it would not by itself derive the cosine-cubed shape, amplitude, onset, or initial
state.

## Track 2 — covariant hold/release EFT as a distinct hypothesis

**Status: minimal covariant matter-coupling test completed; full EFT blocked by
missing operator/sector.**

Use the explicit trial action
\[
S=\int d^4x\sqrt{-g}\left[
\frac{M_{\rm Pl}^2}{2}R-\frac12(\partial\phi)^2-V(\phi)\right]
+\sum_i S_i[A_i^2(\phi)g_{\mu\nu},\psi_i],
\qquad \alpha_i(\phi)=d\ln A_i/d\phi.
\]
With \(T_i=g_{\mu\nu}T_i^{\mu\nu}\) and signature \((-+++)\), variation gives
\[
\Box\phi-V_{,\phi}+\sum_i\alpha_iT_i=0,\qquad
\nabla_\mu T_i^{\mu\nu}=\alpha_iT_i\nabla^\nu\phi.
\]
For homogeneous FRW this implies
\[
\dot\rho_i+3H(\rho_i+p_i)=-\alpha_i T_i\dot\phi,\qquad
\dot\rho_\phi+3H(\rho_\phi+p_\phi)=
+\sum_i\alpha_iT_i\dot\phi.
\]
The terms cancel in the total continuity equation, as required by covariance.
For ideal radiation, \(T_r=-\rho_r+3p_r=0\): this minimal conformal coupling
does not feed a radiation hold. For pressureless matter, \(T_m=-\rho_m\), so its
source is proportional to matter, but its coefficient depends on an unspecified
\(A_m(\phi)\). This is not the hypothesized \(\alpha\rho_r-\beta\rho_m\) curvature.

A nonzero radiation contribution would require an explicit nonconformal operator
or trace anomaly, with its Wilson coefficient and thermal expectation value (for
example a specified gauge sector and its finite-temperature free energy). Then the
effective force, potential curvature, radiation transfer, and perturbations must
all be derived from the same action. Merely substituting \(\rho_r(a)\) into an
external \(\kappa(a)\) is not covariant closure.

**Blocked inputs:** the matter and radiation field content; functions \(A_i\) or
nonconformal operators and coefficients; anomaly normalization; state/temperature
history and expectation values; initial perturbations; and the full stress-energy
transfer/perturbation equations. Without these, neither \(\alpha,\beta\), the
threshold crossing, nor the release angle can be computed. The toy in
`anomaly_toy.py` is a sensitivity demonstration, not this missing EFT.

**What has been screened:** the existing bounded single-harmonic ODE used an
imposed \(\theta_i=2.7841\), fixed radiation-plus-matter background, and an
illustrative \(\chi_h\propto\min(1,T_c/T_h)^4\). At the near-target but
non-independent choice \(m_0/H_{\rm eq}=2.8\), it gave
\((\theta_{\rm eq},f_{\phi,\rm eq})=(2.7815,0.00582)\) for
\(T_c/T_{h,\rm eq}=0.5\), \((2.7413,0.08534)\) for ratio 1, and
\((2.6290,0.08426)\) for ratio 2. Ratios 1 and 2 reach a target-like
fraction, and their normalization was chosen for that purpose. None derives the
phase; the single cosine's stationary points are 0 and \(\pi\), not the fitted
\(0.886\pi\). This screens out the toy as an independent solution; it does not
falsify every possible covariant hold EFT.

**Go / no-go:** do not integrate a proposed EFT until its action yields both the
scalar equation and each sector's continuity equation and the summed conservation
identity above. Then, before numerical evolution, fix all coefficients from
independent inputs and preregister the predicted onset and phase. Reject if
\(m_{\rm eff}/H\) never crosses the derived dynamical threshold near the predicted
epoch, if the phase/energy fraction miss the stated target, or if transfer
violates background or perturbation constraints. No such closed model is present.

## Track 3 — conservative phenomenology and fit-validation preparation

**Status: NOT RUN. Validation rails prepared; no likelihood, optimizer, or fit run
in this task.**

Local provenance:

- The theory and fluid/full-field implementation are in `papers/torsion_born_ede.tex`
  and `ufe-v2/aegis/cosmo_v2.py`.
- `ufe-v2/results_v2.json` is not the source of the reported EDE best fits.
- The saved CAMB/Cobaya minima and preregistrations are under `cmb-fit/`, including
  `README.md`, `PREREGISTRATION_ZEQ.md`, `PREREGISTRATION_N.md`,
  `results/cmp_edeP.json`, and `results/cmp_pact_ede.json`.
- Saved outputs are historical evidence, not rerun or independently reproduced
  results. Preserve them unchanged. Their presence does not by itself validate
  the data files, hashes, likelihood configuration, or reproducibility.

Before any later validation run, all three gates are mandatory: (a) validate that
the exact local data/artifacts, checksums, code revision, and likelihood inputs
exist and match the claimed provenance; missing or inconsistent inputs means
**NO-GO**, not a substitute dataset; (b) freeze a new preregistration with the
fields below; and (c) obtain the user's later, explicit authorization to execute.
Setup work here does not grant run authorization.

1. **Scientific claim and tier:** phenomenological replication, not a derivation
   of torsion origin unless Tracks 1–2 pass.
2. **Exact model implementation:** code path/revision, potential, field width,
   onset rule, initial conditions, and parameter-to-likelihood mapping.
3. **Provenance:** datasets, likelihood versions, nuisance parameters, priors,
   baseline, saved source hashes, and the exact comparison statistic.
4. **Search protocol:** deterministic starting points/restarts, convergence
   tolerance, stopping rule, compute ceiling and failure handling.
5. **Decision threshold and falsifiers:** define before opening new results;
   disclose if the onset/width was selected after observing the baseline data.
6. **Reproduction and reporting:** independent baseline/model minimization under
   identical settings, goodness-of-fit and parameter-count treatment, plus
   sensitivity to solver accuracy and relevant likelihood choices.

**Hard rails:** no SH0ES-derived preference described as blind evidence; no result
from a background-only calculator presented as a full CMB likelihood result; no
post-hoc equality or integer-width claim called a prediction; no fit result used
to fill a missing action coefficient; no execution before all gates and explicit
authorization pass. The current task stops before all fit work.

## Dependency order and exit criteria

Track 1 supplies the base field theory. Track 2 can proceed only after an explicit
additional matter/topological sector is written and its covariant transfer is
closed. Track 3 may validate the declared phenomenological model independently,
but cannot promote a fit preference into a microscopic derivation.

| Track | Current exit state | What would reopen it |
|---|---|---|
| 1 — action derivation | Base kinetic field derived; potential, period, lock, and start are assumed/free | A specified action term and its complete variation/topological normalization |
| 2 — covariant EFT | Minimal conformal coupling cannot source ideal radiation; full hypothesis underdetermined | Matter/radiation action, Wilson/anomaly coefficients, thermal state, and conserved transfer equations |
| 3 — fit validation | Preregistration/provenance checklist prepared; not run | Separate authorization, frozen preregistration, exact code/data versions and bounded run plan |

This rails document is setup, not evidence that any of the three open mechanisms
has been physically solved.
