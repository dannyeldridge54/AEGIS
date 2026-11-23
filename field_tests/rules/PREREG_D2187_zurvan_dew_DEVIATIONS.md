# D2187 DEVIATIONS (written before any fix or rerun), 2026-11-23 ~08:00 CT
Referee R75 (independent agent) returned 2 blockers, 3 major, 5 minor. Core physics confirmed correct
(CW dof factors, D-terms, LR entries, v=174 convention, C_i mapping).

DEV-1 (blocker 1, transcription): the closed form in test_d2187.closed() was checked against arXiv:2111.03096
  App. A, Eqs. A.20/A.21 (fetched 08:00 CT): our transcription matches the printed equations, and the printed
  stop mass matrix (A.14) has off-diagonal a_t v_u - mu y_t v_d, the same as Zurvan. The exact derivative of
  that matrix contains the cross-terms -y_t^2 A_t mu cot(b) (in Su) and -y_t^2 A_t mu tan(b) (in Sd) inside the
  -/+[...]/(m2^2-m1^2) bracket; with them added, closed() reproduces Zurvan to all printed digits (R75 ran it).
  T1 verdict stays as locked: CONVENTION DIFFERENCE, NOT A PASS. To Baer this is a question, not a correction.
DEV-2 (blocker 2, EWSB): P1-P3 inputs were hand-picked and do not satisfy the minimisation condition
  (sum C_i = 8.7e4, 1.7e5, 5.0e8 GeV^2 vs mZ^2/2 = 4.2e3). Fix: Zurvan prints the residual every run and warns
  when |sum C_i - mZ^2/2| > mZ^2/2; examples relabelled "illustrative, not EWSB-consistent". T3 for the Weave
  benchmark is quoted only as the robust bound Delta_EW >= 2 mu^2/mZ^2 = 1.8e6 (mu = 87.6 TeV).
DEV-3 (major, degenerate pairs): flag when |C(1)+C(2)| << max|C(i)| (ratio < 0.1) for any sfermion pair; then the
  headline is the pair-summed value and the per-term value is shown as "DEW4SLHA-style, please confirm".
DEV-4 (major, tachyons): collect a warning whenever a field-dependent m^2 <= 0 is met.
DEV-5 (major, SLHA2): accept TU/TD/TE (A = T/Y); error if neither A nor T block exists for the top;
  JS errors on missing YU like Python.
DEV-6..8 (minor): first block of a repeated name kept (+warning); MSOFT 33-49 squared with sign; one mZ convention
  in both versions: running mZ from g, g', v at Q, printed.
DEV-9/10 (minor): "not included" list extended (tau sneutrino, QCD/gluino corrections to y_t, 2-loop terms);
  README states: third family only; not yet checked against DEW4SLHA on a real Isajet/SoftSUSY file; examples
  hand-built; the cross-check compares our derivative with the printed closed form, not with his code.
T2 is rerun after the fixes (JS vs Python, now through the same command-line path).

## Round 2 (R75b) returned NULL on blockers/majors; minors fixed (written before the fix), 08:15 CT
DEV-11: when a tachyonic field-dependent state is met, the headline is printed as "UNRELIABLE (tachyonic state)".
DEV-12: Python raises a clear error when YU has no (3,3) entry (JS already did).
DEV-13: T3 to Baer is quoted only as the mu bound Delta_EW >= 2 mu^2/mZ^2 ~ 1.8e6, not the printed headline
        (which depends on the hand-picked m_Hd^2).
