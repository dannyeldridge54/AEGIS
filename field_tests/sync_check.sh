#!/bin/bash
# Sync check (PC): report work that exists only on this computer, so nothing goes missing again.
# Lists, for every project repo it finds, uncommitted files, commits not pushed, and how old the last push is.
# Read-only: it never commits or pushes anything except its own report (written to field_tests/SYNC.md).
#   bash field_tests/sync_check.sh
HERE="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"
ROOT="$(dirname "$HERE")"
REPOS=("$ROOT" ${TWIST_REPOS:-})
# Usual locations on the PC (WSL view of C:\Users\Danny); missing ones are skipped.
for d in /mnt/c/Users/Danny/.copilot/repos/* /mnt/c/Users/Danny/Desktop/CubeMind* /mnt/c/Users/Danny/Desktop/*twist* \
         "$HOME"/AEGIS "$HOME"/the-twist-torsion-cosmology "$HOME"/aegis-Kronos-syndyr; do
  [ -d "$d/.git" ] && REPOS+=("$d")
done
OUT="$HERE/SYNC.md"
{
  echo "# Sync check ($(date '+%F %T'))"
  echo
  echo "| Repo | Branch | Uncommitted files | Commits not pushed | Last commit |"
  echo "|---|---|---|---|---|"
  for r in $(printf '%s\n' "${REPOS[@]}" | awk '!seen[$0]++'); do
    git -C "$r" fetch -q origin 2>/dev/null
    br=$(git -C "$r" rev-parse --abbrev-ref HEAD 2>/dev/null)
    dirty=$(git -C "$r" status --porcelain 2>/dev/null | wc -l)
    ahead=$(git -C "$r" rev-list --count "@{u}..HEAD" 2>/dev/null || echo "no upstream")
    last=$(git -C "$r" log -1 --format='%ad' --date=relative 2>/dev/null)
    flag=""; { [ "$dirty" != 0 ] || [ "$ahead" != 0 ]; } && flag=" **⚠**"
    echo "| $(basename "$r")$flag | $br | $dirty | $ahead | $last |"
  done
  echo
  echo "⚠ = work that exists only on this PC. Commit and push it (or say why not) so the cloud and the record can see it."
} > "$OUT"
cat "$OUT"
