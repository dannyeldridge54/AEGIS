"""The locked rules copied into field_tests/rules/ must still match the hashes recorded when they were locked."""
import glob
import hashlib
import os

RULES = os.path.join(os.path.dirname(__file__), "..", "..", "field_tests", "rules")


def test_rule_copies_match_their_lock_hashes():
    shas = glob.glob(os.path.join(RULES, "*.md.sha256"))
    assert len(shas) >= 3
    for s in shas:
        doc = s[: -len(".sha256")]
        locked = open(s).read().split()[0]
        b = open(doc, "rb").read()
        variants = {hashlib.sha256(x).hexdigest() for x in (b, b.replace(b"\r\n", b"\n"),
                                                           b.replace(b"\r\n", b"\n").replace(b"\n", b"\r\n"))}
        assert locked in variants, f"{os.path.basename(doc)} no longer matches its lock"
