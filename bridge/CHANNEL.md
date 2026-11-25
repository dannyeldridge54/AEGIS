# Bridge channel — two-way updates between the local agents and the cloud coordinator (set up 25 Nov 2026, 15:40 CST)

Danny: "Have them open a way to fully communicate and update you." This is that channel. Everything goes through GitHub, AEGIS branch
`unify-bg`, folder `bridge/`. Nothing here sends email or posts anywhere public beyond this repo.

## Two files
| File | Who writes | Who reads | Rule |
|---|---|---|---|
| `bridge/INBOX_CLOUD.md` | the local agents | the cloud coordinator (Claude) | append a new entry at the TOP for every update; never edit an old entry |
| `bridge/OUTBOX_CLOUD.md` | the cloud coordinator | the local agents | same: newest at the top, old entries never edited |
Longer work still goes in `bridge/REPORTS/`; the entry links to it.

## Entry format (both directions)
```
### <ID> — <YYYY-MM-DD HH:MM CST> — <from> — <KIND>
<1-5 lines: what changed / what is asked>
Files: <paths and commit>
Needs: <nothing | Danny: ... | cloud: ...>
```
IDs: agents `A001, A002, ...`; cloud `C001, C002, ...`. KIND is one of: UPDATE, RESULT, PLAN (a locked test plan, with its .sha256),
QUESTION, BLOCKED, ANSWER, DONE.
A QUESTION is answered by an ANSWER entry that names the question's ID.

## Rhythm
- **Agents:** read `OUTBOX_CLOUD.md` at the start of every scheduled cycle (your 30-minute schedule), act on entries newer than the last one
  you handled, and write an INBOX entry at the end of every cycle that changed anything. Push after each entry. A cycle that changed nothing
  writes nothing.
- **Cloud:** reads `INBOX_CLOUD.md` whenever Danny says "check the bridge", or on a schedule if Danny sets one; answers QUESTIONs and checks
  PLANs in the outbox.
- **Anything that needs Danny** is marked `Needs: Danny: ...` so it is easy to find; the cloud coordinator brings it to him.

## Standing orders in force (latest wins)
C6 (send derivation, plans, results here) · C7 (Danny's GO to derive and test, lock-before-run rules) · C8 (research loop: anchor points,
modular/fractal/adjustable grid, goal stability; Danny picks the cells to flip).
