#!/bin/sh
# Re-create the 96 ADF11 files listed in MANIFEST.json from the public OPEN-ADAS mirror (ADAS.jl commit 9c9a319086ca4b6a8139c260ad44d7ef2c4c2eac).
set -e; D=$(dirname "$0"); T=$(mktemp -d)
GIT_LFS_SKIP_SMUDGE=1 git clone -q --depth 1 https://github.com/ProjectTorreyPines/adas.jl "$T/adas"
python3 -c "import json,shutil,sys; m=json.load(open('$D/MANIFEST.json')); [shutil.copy('$T/adas/data/adf11/'+v['file'][:5].rstrip('_')+'/'+v['file'],'$D') for e in m.values() for v in e.values()]"
