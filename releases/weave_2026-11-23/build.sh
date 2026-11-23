#!/bin/bash
# Build the Zenodo supplement for "The Weave: predictions, postulates and pre-registered tests on the newest data" (23 Nov 2026)
set -e
cd "$(dirname "$0")/../.."
R=releases/weave_2026-11-23; T=$(mktemp -d)/Weave_supplement; mkdir -p $T
mkdir -p $T/locks $T/code $T/results $T/notes
cp field_tests/rules/PREREG_D21[0-9][0-9]* $T/locks/ 2>/dev/null || true
cp field_tests/weave_lcdm/*.py field_tests/weave_lcdm/*.json field_tests/weave_lcdm/*.txt $T/results/ 2>/dev/null || true
cp -r field_tests/weave_lcdm/referee_indep $T/results/ 2>/dev/null || true
mkdir -p $T/code/engine $T/code/pc_runs $T/code/brane_z6prime $T/code/loom
cp tools/weave_cm_v5/*.py tools/weave_cm_v5/early_calib.json tools/weave_cm_v5/*.md tools/weave_cm_v5/WEAVE_FACTS.txt $T/code/engine/ 2>/dev/null || true
cp tools/weave_pc/* $T/code/pc_runs/ 2>/dev/null || true
cp tools/seed/z6p*.py tools/seed/z6p*.json $T/code/brane_z6prime/ 2>/dev/null || true
cp tools/loom/{resonance,resonance10,negspace_ladder,negspace_outward,negspace_derive,node_equations,open_node_equations,tauq_moduli,wall_pull,restructure}.py $T/code/loom/ 2>/dev/null || true
cp field_tests/results/d21[3-5][0-9]*.json $T/results/ 2>/dev/null || true
cp cmb-fit/cmbfit.py cmb-fit/rt_planck_fit.py $T/code/ 2>/dev/null || true
python3 - "$T/notes/D2110_onward.md" <<'PY'
import sys
t = open('theory/pending_docs/D72_D75_weak_spots.md', encoding='utf-8').read()
i = t.find('## D2110'); open(sys.argv[1], 'w', encoding='utf-8').write(t[i if i >= 0 else 0:])
PY
cp $R/README.md $R/MAKERS_MARK.txt LICENSE $T/
python3 - "$T" <<'PY2'
import hashlib, os, sys
T = sys.argv[1]; mk = hashlib.sha256(open(os.path.join(T, 'MAKERS_MARK.txt'), 'rb').read()).hexdigest()
lines = [f'{mk}  MAKERS_MARK.txt  (the mark)']
for root, _, files in sorted(os.walk(T)):
    for f in sorted(files):
        p = os.path.join(root, f); rel = os.path.relpath(p, T)
        if rel in ('FINGERPRINTS.sha256', 'MAKERS_MARK.txt'): continue
        lines.append(f'{hashlib.sha256(open(p, "rb").read()).hexdigest()}  {rel}  mark:{mk[:12]}')
open(os.path.join(T, 'FINGERPRINTS.sha256'), 'w').write('\n'.join(lines) + '\n')
print('fingerprinted', len(lines) - 1, 'files with mark', mk[:12])
PY2
(cd $(dirname $T) && rm -f Weave_supplement.zip && zip -qr Weave_supplement.zip Weave_supplement)
cp $(dirname $T)/Weave_supplement.zip $R/
ls -la $R; unzip -l $R/Weave_supplement.zip | tail -1
