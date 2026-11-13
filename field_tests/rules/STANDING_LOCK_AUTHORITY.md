# Standing lock authority (24-hour development run)

Granted by Danny, 2026-11-12 21:57 CT: "Set it up to lock and perform like I asked" — following
"Everytime u come to a crossroads … record all options test and keep moving forward best route on ure own"
and "For 24 hrs or full theory realization".

Valid until 2026-11-13 22:00 CT or full realization (plan doc checklist), whichever is first.

## What it allows
The development driver may lock a new pre-registered rule itself and then run (perform) the test.

## Lock protocol (every lock, no exceptions)
1. Write the rule in full **before** any data for that test is fitted or scored: hypothesis, data, likelihood,
   priors, readings (SUPPORTED / PARTIAL / NOT SUPPORTED thresholds), gates, failure handling.
2. Compute its sha256, save `<RULE>.sha256`, add a header line
   "LOCKED <time CT> by the development driver under STANDING_LOCK_AUTHORITY.md".
3. Commit and push the locked rule **before** the run starts. The commit time is the lock time.
4. Run the test. Score it exactly as the rule says. Record whatever comes out.
5. Fixes go only in a `<RULE>_DEVIATIONS.md` entry written before any rerun. No reruns to chase a result.

## Full autonomy (Danny, 2026-11-12 21:58 CT: "Everything we do together have it be able to do itself")
The driver does on its own everything done together in sessions: develop theory, review online and local sources,
write and lock rules, run cloud tests, queue PC fits and record their results, update CURRENT_MODEL.md, the matter
doc, schoolbook, plan doc and paper, re-export the paper PDF to the PC (Desktop\AEGIS_zenodo), commit and push.
Zenodo: may update the existing *draft* only if a signed-in session is already open; never types a password and
never presses Publish (Danny's button). arXiv: prepare files only.

## Full authority (Danny, 2026-11-12 21:59 CT: "Full authority")
Cadence every 30 minutes ("Have it check every 30 mins"). Danny's own earlier working limits are lifted for the
run, including merging unify-bg into master on GitHub when a milestone is complete and all results are committed.

## Still not allowed (integrity and safety, not Danny's choice to waive in advance)
Editing any already-locked rule, prior or result (that would break the pre-registration itself); typing passwords;
pressing Publish on Zenodo or submitting to arXiv (public, irreversible: Danny's button each time); permanent
deletes on the PC (move to _to_delete/); closing windows running fits; touching the PC repo's git.
