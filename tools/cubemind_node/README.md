# CubeMind Node 1 — Level 0 (set and forget)

One node of the CubeMind neural web that runs by itself, forever, with local models only (no cloud credits).
Ring R1 (SERAPIS-E) at the anchor rho, CubeMind at the centre, three local models around it:
retriever/lens (qwen3:14b), processor (qwen3-coder:30b), referee mirror (gpt-oss:20b). Code decides what is right; models propose.

**Start:** double-click `Start_CubeMind_Node1.bat` (restarts itself if it stops). **Start at every login:** double-click `Install_Autostart.bat` once.
**Watch:** open `node1_data\status.html` (refreshes every minute). **Stop:** close its window.
**Needs:** Python 3 and Ollama running, with the three models pulled. Optional: `pip install psutil` (lets it yield CPU/RAM and run at low priority);
a GitHub token in the environment variable GITHUB_TOKEN raises the search limit (60 -> 5,000 requests/hour).
**Settings:** `node1_config.json` (created on first run): models, cycle time (default 5 minutes), caps.
**Safe to leave:** it never deletes anything but its own old backups (keeps 7), never installs, never changes code, never touches the live CubeMind;
one model loaded at a time; database size cap 2 GB; every result fingerprinted and signed with your key (`%USERPROFILE%\.aegis_owner.key`, back it up).
Tests: `python -m unittest test_node1` (stand-in models, no network).

## Tools and goalposts (25 Nov 2026, v2)
Install the tools once: double-click `Install_CubeMind_Tools.bat`, then restart Node 1. Browse everything it has filed: `Browse_CubeMind.bat`.
New in v2: four research sources (GitHub, arXiv, Semantic Scholar, OpenAlex; plain web requests, no keys); links by meaning (Ollama
`nomic-embed-text`); a daily self-check that re-derives the audit's 18 algebra steps (sympy); GPU memory in the resource check (nvidia-ml-py);
and 12 goalposts on the status page, one per part, each MET or NOT YET.
