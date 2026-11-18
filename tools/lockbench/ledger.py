# AEGIS-FP VPET5IH57KTJK2LN · (c) Danny Lee Eldridge · AEGIS Community License (business use needs the Commercial License)
"""Reference-precision ledger: field_tests/results/LEDGER.jsonl. A claim's stated precision may not be smaller than the reference's own spread."""
import json, time
PATH = 'field_tests/results/LEDGER.jsonl'
def record(dnote, quantity, claimed_rel, reference_spread_rel, reference, verdict):
    honest = claimed_rel >= reference_spread_rel
    rec = dict(t=time.strftime('%Y-%m-%dT%H:%MZ', time.gmtime()), dnote=dnote, quantity=quantity, claimed_rel=claimed_rel,
               reference_spread_rel=reference_spread_rel, reference=reference, verdict=verdict, precision_honest=honest)
    open(PATH, 'a').write(json.dumps(rec) + '\n'); return rec
