#!/bin/sh
# usage: sh fetch.sh  (needs git; downloads only the listed blobs)
set -e; D=$(dirname "$0"); T=$(mktemp -d)
git clone -q --depth 1 --filter=blob:none --no-checkout https://github.com/openmc-data-storage/ENDF-B-VIII.0-NNDC "$T/e8"
for n in Li6 Li7 H1 H2 H3 He4 Be9 C12 O16 Si28 Cr52 Fe56 Ni58 Pb208 W184 Mn55 Zr90 Ca40; do (cd "$T/e8" && git checkout HEAD -- h5_files/neutron/$n.h5); cp "$T/e8/h5_files/neutron/$n.h5" "$D/h5/"; done
git clone -q --depth 1 --filter=blob:none --sparse https://github.com/njoy/NJOY2016 "$T/njoy"; (cd "$T/njoy" && git sparse-checkout set tests/resources); cp "$T"/njoy/tests/resources/n-*.endf "$D/endf/"
