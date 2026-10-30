#!/bin/sh
# Copyright (c) 2012-2026 Danny Lee Eldridge. Licensed under THE AEGIS PEOPLE'S LICENSE (see LICENSE): free for people; no AI use; no military, surveillance or harmful use.
# Check my work on Mac or Linux:  sh check_my_work.sh
cd "$(dirname "$0")"
echo 'CHECK MY WORK - every number, re-derived on your own computer'
python3 -m pip install --quiet --user numpy scipy >/dev/null 2>&1
echo; echo '[1/2] Re-deriving the model numbers from scratch:'
python3 ufe-v2/recheck_math.py
echo; echo '[2/2] Honesty guardrails:'
(cd ufe-v2 && python3 -c "import aegis.guardrails as g; r=g.run_all(); [print(('PASS ' if c['ok'] else 'WAIT ' if c['ok'] is None else 'FAIL '), c['name'], '-', c['plain']) for c in r['checks']]; print(r['passed'],'pass,',r['failed'],'fail,',r['waiting'],'waiting')")
echo; echo 'Found a mistake? Please say so publicly.'
