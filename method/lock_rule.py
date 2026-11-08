"""AEGIS Method: lock a pre-registration rule (SHA-256 + UTC time) and verify locks later. Stdlib only, any field.
    python lock_rule.py lock   RULE.md        -> writes RULE.md.sha256 ("<hash>  RULE.md  locked <UTC time>"); refuses if one exists
    python lock_rule.py verify [FOLDER ...]   -> re-hashes every file named in every *.sha256 under the folders
A lock proves the text existed unchanged since that time only if the .sha256 is also published (git push, Zenodo,
Software Heritage). Line-ending-only differences (Windows checkouts) are reported separately from content changes."""
import hashlib
import os
import sys
import time


def sha(path, crlf_to_lf=False):
    b = open(path, "rb").read()
    return hashlib.sha256(b.replace(b"\r\n", b"\n") if crlf_to_lf else b).hexdigest()


def lock(rule):
    out = rule + ".sha256"
    if os.path.exists(out):
        sys.exit(f"{out} exists: a locked rule is never re-locked. Write a new rule or log a deviation.")
    stamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    line = f"{sha(rule)}  {os.path.basename(rule)}  locked {stamp}\n"
    with open(out, "x", encoding="utf-8") as f:
        f.write(line)
    print(line.strip(), "\nNow publish the .sha256 (commit + push) before looking at any data.")


def verify(folders):
    n = ok = eol = 0
    for folder in folders or ["."]:
        for root, _, files in os.walk(folder):
            for f in files:
                if not f.endswith(".sha256"):
                    continue
                for raw in open(os.path.join(root, f), encoding="utf-8").read().splitlines():
                    parts = raw.split()
                    if len(parts) < 2 or len(parts[0]) != 64:
                        continue
                    n += 1
                    target = os.path.join(root, parts[1])
                    if not os.path.exists(target):
                        print("MISSING ", target)
                    elif sha(target) == parts[0]:
                        ok += 1
                    elif sha(target, True) == parts[0]:
                        eol += 1
                        print("EOL ONLY", target)
                    else:
                        print("CHANGED ", target)
    print(f"{n} locked files: {ok} exact, {eol} line endings only, {n - ok - eol} changed or missing")
    return n - ok - eol


if __name__ == "__main__":
    if len(sys.argv) >= 3 and sys.argv[1] == "lock":
        lock(sys.argv[2])
    elif len(sys.argv) >= 2 and sys.argv[1] == "verify":
        sys.exit(1 if verify(sys.argv[2:]) else 0)
    else:
        print(__doc__)
