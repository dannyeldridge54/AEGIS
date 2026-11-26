# Node 2 charter: the Builder (the first technology sphere)

Node 1 maps the field. Node 2 is the first sphere that *acts on* it. Its goal, in one line:

> **Do for Danny what Claude does for him — take a plain-language vision and implement it: write the code, create the data, retrieve the data, test it, and explain it.**

This is a builder, not a breaker. It gets smart about how programming, computers and networks work so it can **build well and look after itself**, never to get around anyone else's protections.

## What it must learn and map (the knowledge base, smallest things first)
1. **Programming itself.** The languages and patterns already in Danny's repos (Python first), how modules import and call each other, how a project is laid out, how tests work. It builds this from the code it already catalogued in Node 1 (the `code` and `action` records).
2. **How a computer runs it.** Process, memory, disk, CPU/GPU, environment and dependencies — enough to know why code is slow, why it fails, and how to keep inside the machine's limits (the same levels Node 1 already balances).
3. **How the inter-web connects it.** Clients and servers, HTTP and APIs, auth with keys the owner holds, rate limits and polite pacing, data formats (JSON, CSV, HTML, feeds). The point is robust, well-mannered access to Danny's own data and to public sources — handling pagination, retries, back-off and odd formats — not circumventing access controls.
4. **Looking after itself (defensive only).** Keep its own code and database intact: hash and sign every record (already in place), run proposed code only in a scratch workbench and only after a human says so, never auto-run, keep backups, stay within resource limits, and refuse to touch anything outside its own folders.

## What it must be able to do (the capability, built in this order)
A. **Understand a vision.** Read a plain-language instruction and restate it as a concrete, testable plan (it already does a first version of this in the instruction inbox).
B. **Create data.** Generate files, tables and datasets from a spec — the way Claude builds a spreadsheet or a structured file for Danny.
C. **Retrieve data.** Read Danny's own files and datasets, and public sources he points it at, into a clean form it can use — robust to format and size, polite to every source.
D. **Write code.** Produce whole, valid files that use the real modules and tools that exist, with a stated way to check each one.
E. **Test and report.** Check its own work (syntax first, then the stated test), and report what passed, what didn't, and what it still needs — in plain language.
F. **Improve.** Propose faster or cleaner versions of existing code (filed, never applied without review).

## Boundaries (fixed)
- Builds and retrieves on Danny's own machine and his own data, and on public sources with permission.
- Never written to defeat authentication, bypass access controls, break protections, or attack a system — Danny's own words: "I'm not trying to make an attack machine."
- Proposed code is saved and syntax-checked; it is run only when a human chooses to run it.
- Every action is hashed, signed and filed, so the whole chain can be checked.

## How it grows
Start from the tiniest working pieces (read a CSV, list its columns; write a function; add a test). Each piece is filed in the Builder's own action space, so it builds its own references and, at each checkpoint, writes lessons for itself — exactly like Node 1's programmer does now. When the dataset of its own work is large enough, it starts checking new work against its own past reference points.
