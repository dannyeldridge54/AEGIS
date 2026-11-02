# Copyright (c) 2012-2026 Danny Lee Eldridge. Licensed under the Hippocratic License 3.0 with the Military Activities and Mass Surveillance modules (HL3-MIL-SV; see LICENSE): free to everyone, for any use that respects human rights.
"""One-off: replace this PC's absolute paths in cmb-fit/axiclass with portable ones. Defaults resolve to exactly the
old paths on the author's PC, so behaviour there is unchanged. Elsewhere set (or accept the defaults):
    TWIST_RESULTS  results folder        (default: cmb-fit/results next to this code)
    TWIST_BUILDS   folder holding the AxiCLASS builds (AxiCLASS, AxiCLASS_nlfix, AxiCLASS_coupled, ...; default: $HOME)
    TWIST_PY       python with cobaya + classy (shell scripts; default: the author's env if present, else python3)
    python make_portable.py [--apply] [skip.sh ...]"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
WIN = "/mnt/c/Users/Danny/.copilot/repos/AEGIS/cmb-fit"
PYENV = "/home/syndyr/micromamba/envs/aegis"
apply = "--apply" in sys.argv
skip = {a for a in sys.argv[1:] if not a.startswith("--")}

PY_HEAD = ("import os as _os\n_AXI = {axi}\n_RESULTS = _os.environ.get(\"TWIST_RESULTS\", _os.path.join(_os.path.dirname(_AXI), "
           "\"results\"))\n_BUILDS = _os.environ.get(\"TWIST_BUILDS\", _os.path.expanduser(\"~\"))\n")
SH_HEAD = ("# Portable paths (make_portable.py): override with TWIST_RESULTS, TWIST_BUILDS, TWIST_PY.\n"
           "AXI=\"$(cd \"$(dirname \"${{BASH_SOURCE[0]:-$0}}\")\"{up} && pwd)\"\n"
           "RES=\"${{TWIST_RESULTS:-$(dirname \"$AXI\")/results}}\"\nBLD=\"${{TWIST_BUILDS:-$HOME}}\"\n"
           "PY=\"${{TWIST_PY:-" + PYENV + "/bin/python}}\"; [ -x \"$PY\" ] || PY=python3\n")


def py(text, depth):
    axi = "_os.path.dirname(_os.path.abspath(__file__))" if depth == 0 else \
          "_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))"
    t = re.sub(r'Usage: python (\S+) /home/syndyr/[^\s"]+', r"Usage: python \1 <path to your AxiCLASS clone>", text)
    t = t.replace("python bug_reproducer.py /home/syndyr/", "python bug_reproducer.py $TWIST_BUILDS/")
    t = t.replace(f"python {WIN}/axiclass/", "python cmb-fit/axiclass/")
    t = t.replace(f'"{WIN}/axiclass"', "_AXI").replace(f'"{WIN}/results"', "_RESULTS")
    t = t.replace(f'"{WIN}"', "_os.path.dirname(_AXI)")
    t = re.sub(rf'"{re.escape(WIN)}/results/([^"]+)"', r'_os.path.join(_RESULTS, "\1")', t)
    t = re.sub(r'"/home/syndyr/([^"]*)"', r'_os.path.join(_BUILDS, "\1")', t)
    if t == text:
        return text
    lines = t.split("\n")
    i = 0                                                      # after the module docstring / leading comments
    if lines[0].startswith("#"):
        i = 1
    if i < len(lines) and lines[i].lstrip().startswith(('"""', "'''")):
        q = lines[i].lstrip()[:3]
        if lines[i].count(q) >= 2 and len(lines[i].strip()) > 3:
            i += 1
        else:
            i += 1
            while i < len(lines) and q not in lines[i]:
                i += 1
            i += 1
    lines.insert(i, PY_HEAD.format(axi=axi).rstrip("\n"))
    return "\n".join(lines)


def sh(text, depth):
    up = "" if depth == 0 else "/.."
    t = text
    t = re.sub(rf"^(PY|P)={re.escape(PYENV)}/bin/python\s*$\n?", lambda m: "" if m.group(1) == "PY" else "P=$PY\n", t,
               flags=re.M)
    t = re.sub(rf"^ENV={re.escape(PYENV)}\s*$", 'ENV="${TWIST_ENV:-$(dirname "$(dirname "$PY")")}"', t, flags=re.M)
    t = t.replace(f"{PYENV}/bin/python", "$PY")
    t = t.replace(f"{WIN}/axiclass", "$AXI").replace(f"{WIN}/results", "$RES")
    t = t.replace("/home/syndyr/", "$BLD/")
    if t == text:
        return text
    lines = t.split("\n")
    i = 1 if lines[0].startswith("#!") else 0
    while i < len(lines) and lines[i].startswith("#"):
        i += 1
    lines.insert(i, SH_HEAD.format(up=up).rstrip("\n"))
    return "\n".join(lines)


changed = []
for d, _, files in os.walk(HERE):
    depth = 0 if d == HERE else 1
    for f in files:
        p = os.path.join(d, f)
        if f in skip or f == "make_portable.py" or not f.endswith((".py", ".sh")):
            continue
        src = open(p, encoding="utf-8", newline="").read()
        crlf = "\r\n" in src
        text = src.replace("\r\n", "\n")
        new = py(text, depth) if f.endswith(".py") else sh(text, depth)
        if new != text:
            changed.append(os.path.relpath(p, HERE))
            if apply:
                open(p, "w", encoding="utf-8", newline="").write(new.replace("\n", "\r\n") if crlf else new)
print(f"{'changed' if apply else 'would change'} {len(changed)} files:")
print("\n".join(sorted(changed)))
