# PREREG CM-NUCLEAR: wire Chronos into CubeMind (registry + Janus "Ask" panel), locked 2026-11-23 ~09:40 CT
Danny: "wire this all into CubeMind ... type in their questions ... present the data, charts, graphs".
Build: tools/gifts/chronos/chronos_cm.py (one dispatcher: chronos_<tool>(args) -> numbers + an optional chart spec
{title, x_label, y_label, logy, series[{name, x, y}]}); CubeMind registry entries chronos_* (aegis_tools/registry.py WORKER
branch, TOOL_NODE 'nuclear'); Janus app Api.ask(question): the local CubeMind model (Ollama) answers through TOOL: lines,
the app runs them through the same registry, feeds RESULT lines back (max 4 rounds), shows the answer, every engine call,
and draws any returned chart. Guards: answers must quote tool results; refusal text for dose/shielding/clinical questions.
Locked checks (cloud, before deploy):
C1 every chronos_* tool reproduces the referee-cleared numbers (D2189, A2, A3) to 1e-9 relative:
   make_now F-18 370 MBq @ 2.5 h = 954.0195616592; generator Mo-99 peak 22.84702241 h, ratio 0.9637427150;
   release_age Cs 0.05/1 = 9.58362825 y; nickel_mass tail 1e41 @200 d t0 40 = 0.5956508450; white_dwarf_merger 765 s
   0.26/0.50 = 1.10932051 Myr; ac225 Bi-213 @6 h from 10 MBq = 9.81445395 MBq; pu_age 0.02 = 9.82615890 y;
   tritium 1000 g 1 y left = 945.29148768 g; star_age Th/Eu -0.52/0.45 = 8.05559322 Gyr (JS values from Chronos Live).
C2 every curve tool returns a chart whose series are finite and whose x is increasing.
C3 the registry worker on the PC returns the same numbers as C1 (run once after deploy).
