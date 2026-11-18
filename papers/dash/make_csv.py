# AEGIS-FP QG5OY76G5JCBZON6 · (c) Danny Lee Eldridge · AEGIS Community License (business use needs the Commercial License)
"""Ledger upkeep helper (LARGE_LIST item 14). Lists D-notes in the derivation log that the newest ledger CSV doesn't have yet, with their log lines,
so each can be added by hand with its real verdict and key number. (Auto-parsing verdicts and numbers from log lines was tried and mis-read too many
lines — e.g. picking '0.1' from 'KALUZA v0.1' — so the ledger stays hand-curated.)
Usage: python3 papers/dash/make_csv.py papers/dash/dnotes_2026-11-17b.csv D1160"""
import re, sys, csv
have = {r['dnote'] for r in csv.DictReader(open(sys.argv[1]))}; lo = int(sys.argv[2][1:])
for l in open('theory/derivations/DERIVATION_LOG.md', encoding='utf-8'):
    m = re.match(r'^## D(\d+): (.+)', l.strip())
    if m and int(m.group(1)) >= lo and f'D{m.group(1)}' not in have: print(f'D{m.group(1)}: {m.group(2)[:150]}')
