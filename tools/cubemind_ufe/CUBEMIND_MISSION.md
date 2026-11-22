# CubeMind mission brief (Danny, 21 Nov 2026)
**Use the UFE (CUBEMIND_UFE_LENS.md) as the main lens on everything.**
- Every piece you examine fits somewhere in the field: on S (time and cosmology), T (forces and scales), U (matter and flavour), or on an interface (S–T, T–U, S–U).
- Your job is to find where. Say honestly when it does not fit.

## How to run: no timer, no check-ins
`START_UFE_JANUS.bat <modelA> <modelB>` runs back to back until stopped.
- **LEARN:** lessons and held-out exams, graded mechanically, until a face masters every track. Mastery means ≥ 80% on two exams in a row, no open WRONG, and Brier ≤ 0.20.
- **MISSION:** M1 Hutter knobs, M2 Ramsey R(3,10), M3 postulates on the big open problems. A refresher exam runs every 10 steps; falling below mastery sends it back to LEARN.

## The Loom method (how we work), and the goalposts
- **Goalposts:** every target has a numeric bar and a pass rule fixed in advance.
- **Median and triangulation:** take three independent readings or vectors. Consensus means within 1σ or 0.3 dex. Use the median, not the best-looking one.
- **Lock, then compute:** sha256 the proposal, then score it. Never rerun to chase a result; a fix needs a written deviation first.
- **Seven nulls:** repeat until seven rounds in a row find nothing new. That is a STALL, not success; switch to exploring.
- **Compass:** fingerprint every result with ring, direction, headroom and the knobs it pulls.
- **Referee:** an independent check before any claim. Labels: PASS, FIT, TRUST, PHEN, CONDITIONAL, INDETERMINATE, NO-POWER.
- **Data retrieval, as practised today:**
  - pull three sources and cross-check them;
  - prefer primary data;
  - fingerprint each result into the compass;
  - archive processed data with cm_compress.py, which keeps a verified round-trip.

## Honest limits
- **M3:** postulates are never claims. Millennium-type problems have no mechanical grader here; Claude and a referee must lock and test any idea.
- **M2:** a valid witness raises an ALERT. It must be re-verified with ramsey/verify.py before anyone says anything.
- **Guards:**
  - no downloads, publishing, emails or passwords;
  - nothing deleted;
  - originals are deleted only if Danny sets CM_DELETE_ORIGINALS=1.
