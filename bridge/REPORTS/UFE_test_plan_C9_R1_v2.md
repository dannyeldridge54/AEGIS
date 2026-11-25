# C9 search plan v2: R1 flux-local admission

The leader chooses one outward step from R0: add independent complex S
through the conditional flux-local bridge because its specified quadratic
model closes all four real masses. This checker did not propose the case.
This plan admits **only R1 once**, including its declared null control.
It is not an R0 rerun, a new search branch, or permission to choose R2.
Full derivation through testing remains the team goal, not an achieved UFE.

## Fixed model, reference and views

MPl=1; U0=S0=rho=(1/2,sqrt(3)/2). Tree K=-ln(2y)-ln(2s),
K0=-ln3, KUUinv=KSSinv=3, real G=(2/3)I4. At W=DW=0,
W2=-b_f deltaU deltaS, a=0 under the **assumed** unbroken U-only
order-three selection rule; no omitted sector/uplift. In coordinates
(deltaUx,deltaUy,deltaSc,deltaSs), evaluate exactly
V2=exp(K0)[3|b_f deltaS|^2+3|b_f deltaU|^2].
Thus coordinate H=2 b_f^2 I4 and the four local canonical mass-squares
are3 b_f^2. No full/global R0 potential retention or UV realization follows.

Fixed analytic R0 reference m0_squared=11.566718599357344=2E2(rho),
not a noisy FD estimate. Candidate b_f=positive sqrt(m0_squared/3).
This spends one deliberate matching condition, not a UV derivation.
Null b_f=0 has four zero local masses: not strictly positive, not a
tachyon, and not a CUT because the nonzero-coupling rescue is declared.
Inherited budget(V0,C)=2 plus new b_f=1 gives3; numerical optimization0.
No extra V_w input, loop32 tuning, physical S/YFORK2/Weave mass match,
sector identification or unprovided matter/photon coupling is introduced.

Required views: geometry/positive tree metric with conditional symmetry;
the complete four-real local spectrum; data/bounds. Missing common
physical action, UV or observable/data bindings makes overall UNCLEAR.
Optional Loom placement is metadata only. No global, endpoint, removal,
minimality or physical fractal claim is admitted.

## Predeclared computation and decision

One isolated Python process: candidate and null, each at central-FD
h=(1e-3,3e-4,1e-4), all4 gradient components and the full symmetric4x4
coordinate Hessian. Every stencil must be finite and in y,s>0 with
finite positive tree metric. Use G Cholesky L and eigvalsh of
L^-1 H L^-T, not a2x2 subblock or Euclidean coordinate spectrum.
At this stationary background the coordinate/covariant Hessians agree.

All12 candidate eigenvalues must have relative error to m0_squared<=1e-6;
maximum ordered-eigenvalue inter-h spread/m0_squared<=1e-6.
Gradient infinity norm across all h<=1e-10*max(1,m0_squared).
Strict positive margin=1e-6*max(1,maxabs eigenvalues).
Null maxabs eigenvalue<=1e-12*max(1,m0_squared), with the same gradient rule.
Call only TOOLS['ufe_flux_mass'][2] fitter and[3] tester for each variant:
finite engine mass within1e-12*max(1,m0_squared) of the fixed reference
(zero for null), and its Boolean tester must be true. That tester checks
algebraic normalization; it is not independent physical evidence.

After identity/metric/finite admission, a candidate eigenvalue below
-margin is NOT STABLE locally (R0 sign rule); otherwise all candidate
checks and strict margin passing gives STABLE locally CONDITIONAL;
otherwise UNCLEAR. Null passing means MASSLESS locally, not STABLE.
Overall remains UNCLEAR under the unresolved data/common-action/UV view.
Numerical/API mismatch exits2 with failed checks; runtime/import/identity
failure exits1 with traceback and explicit error; all numerical checks
passing exits0. No automatic retune, rerun, install or application-control
bypass. Preserve failures and return to the leader.

## Exact identities and execution gate

Source AEGIS `35ee189df9bc94ce9e98d754405b6441cc8d6412`:
audit `bridge/REPORTS/UFE_final_copilot_2026-11-25.md:174-194`,
SHA256 `e0fc222ac37c078de9c0b507091173b30b7e35dbf7b5f08b05fb98c34279a9de`;
`tools/field_engine/ufe_pack.py`, SHA256
`32fc0710ac6ae7caa6a4436dd3801f35a0499039c936d210cacb4714a06ee178`.
The engine's old gauge-gate metadata is not the source-owner correction
or a current UFE convention verdict; no combine()/other tools are run.
R0v1 is frozen at `f85e0445fca898a9dab14bfc4f263c4ee7da1f8a`,
plan SHA256 `1d21e7c5b39e87f8145b146d4c34c6b55c9377e866770f506ecd251247ab4bc4`.
The accompanying DEVIATIONS record admits only the differences above.

| R1 artifact | SHA256 |
|---|---|
| r1.py | 7767c9c1424072bb3acfebd05e53f4d99075cf431dba7d2df328dafbf55ca155 |
| invoke-r1.ps1 | 1007c7dfa367b6064cce23cb7da71b7fe9667eb1a8b667298a138c5443da2205 |
| r1-input-v2.json | da1b2cc917c8720545be98210aefb1d89349fb6c729afde17dd05c76ba708232 |
| runtime-manifest-v2.json | 257e98d69374491a1b80527d82f481ad30be7a4f774f920890337c0507369398 |
| UFE_test_plan_C9_R1_v2_DEVIATIONS.md | 12c8fa85a73bc83c5c59ad367335b533047f90bd2ef2b93fa27f84a2b6da317c |

Intended host Windows x64, Python3.12.10, NumPy2.5.4, SciPy1.18.1,
mpmath1.3.0/dps30. Executable SHA256
`4d6f5f81a4bca11191c4c7c6b43632694d0a4ce74e068619d8fdc161d469859a`;
python312.dll SHA256
`9a0e3435aaa680d868150f87ab3e388ad2eebc22f87e036155c7b4eda8cd2120`.
Runtime manifest binds2623 package/native/metadata files (excluding bytecode
caches); no claim to pin the entire Windows OS. Verify these bytes/versions
before scientific/model imports. No such import/evaluation occurred while
preparing this plan; only source/metadata reads and hashes.

AEGIS alone publishes this plan, SHA256 sidecar, deviation and the four
other listed support artifacts, verifies remote byte hashes at a full commit,
and returns a lock receipt **before execution**. The private local receipt
binds that commit and all seven files; the harness checks it and the
sidecar/source/runtime bytes. Actual app gates remain. No receipt is
fabricated to satisfy the gate.

In the dedicated R1 directory containing pinned sources and those artifacts:

```powershell
& .\invoke-r1.ps1
```

Wrapper resolves the declared interpreter via the host's LocalApplicationData,
uses -I -B -u r1.py, and exclusively creates r1-stdout-v2.txt,
r1-stderr-v2.txt and r1-execution-v2.json; harness exclusively creates
r1-started-v2.json and r1-result-v2.json. Existing attempts/outputs cause
refusal. Capture real exit code, elapsed time, all cases/views/checks/errors
and output hashes. No historical output is touched. Report a short R1
verdict to the leader and sole publisher, then wait; one INBOX line per
round is published by AEGIS, not by this checker.
