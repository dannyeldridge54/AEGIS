#!/bin/sh
# Claim the next free D-number before writing a note, so parallel sessions never reuse one.
# Usage (repo root):  sh tools/dnotes/claim_d.sh "short title"   -> prints the claimed number, e.g. D714
set -e
F=theory/pending_docs/NEXT_D.txt
for attempt in 1 2 3 4 5; do
  git pull -q --rebase origin "$(git rev-parse --abbrev-ref HEAD)"
  N=$(head -1 "$F" | tr -dc '0-9')
  echo "$((N + 1))" > "$F"
  echo "D$N  $(date -u +%Y-%m-%dT%H:%MZ)  ${1:-untitled}" >> theory/pending_docs/D_CLAIMS.log
  git add "$F" theory/pending_docs/D_CLAIMS.log
  git commit -q -m "Claim D$N: ${1:-untitled}"
  if git push -q origin HEAD 2>/dev/null; then echo "D$N"; exit 0; fi
  git reset -q --hard HEAD~1   # someone else claimed first: drop our claim commit and retry
done
echo "could not claim a number after 5 attempts" >&2; exit 1
