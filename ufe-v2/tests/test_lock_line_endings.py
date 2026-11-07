"""The rule-file lock must ignore Windows/Linux line endings but still catch any change to the words."""
import hashlib
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from aegis.method import same_as_lock


def _lock_of(data):
    return hashlib.sha256(data).hexdigest()


def test_crlf_lock_matches_lf_checkout(tmp_path):
    text = b"Rule: pass if dchi2 <= -4.\nLocked 2026-10-29.\n"
    locked_on_windows = _lock_of(text.replace(b"\n", b"\r\n"))
    p = tmp_path / "PREREG.md"
    p.write_bytes(text)                                   # same words, LF endings
    assert same_as_lock(str(p), locked_on_windows)


def test_lf_lock_matches_crlf_checkout(tmp_path):
    text = b"Rule: pass if dchi2 <= -4.\n"
    p = tmp_path / "PREREG.md"
    p.write_bytes(text.replace(b"\n", b"\r\n"))
    assert same_as_lock(str(p), _lock_of(text))


def test_changed_words_still_fail(tmp_path):
    locked = _lock_of(b"Rule: pass if dchi2 <= -4.\r\n")
    p = tmp_path / "PREREG.md"
    p.write_bytes(b"Rule: pass if dchi2 <= -2.\n")        # one number changed
    assert not same_as_lock(str(p), locked)


def test_missing_lock_fails(tmp_path):
    p = tmp_path / "PREREG.md"
    p.write_bytes(b"x\n")
    assert not same_as_lock(str(p), None)
