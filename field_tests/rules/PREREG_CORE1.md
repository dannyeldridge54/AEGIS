# PREREG CORE-1 — one core for every AEGIS tool (locked before build/run), 2026-11-23

Danny 10:17: "a program that combines it all in one go ... 1 core scales for all data pathways". Research read 10:25
(MCP tools spec 2025-11-25; AiiDA 1.0, arXiv:2003.12476; Consist provenance-aware caching, LBNL 2026) gives the shape:
1. Every tool describes itself one way: name, title, field, description, inputSchema (JSON Schema, with x-unit per field),
   outputSchema, limits, lock (its PREREG), status (refereed / unrefereed), cost class (fast < 10 s, slow).
2. One call path: validate inputs -> cache lookup (content hash of tool code + args, not file mtimes) -> run in a worker process
   with a timeout -> check outputs (finite numbers, schema) -> result in MCP shape {structuredContent, isError, content}
   -> append a provenance record (tool, args hash, code hash, result hash, time, cached?, parent ids) to a JSONL ledger.
3. Backends: the existing CubeMind registry (subprocess worker, 62 tools) and direct module adapters for the gift toolkits
   not in the registry (Zurvan, Aion, Hyperion J-factor). Existing tools are wrapped, not rewritten.
4. A status board (JSON + HTML) listing every tool: field, status, lock, last run, last error.

Tests (cloud, against the repo copy of the tools; PC run reported separately):
- K1 coverage: every registry tool and every adapter has a spec whose inputSchema validates its own example (100%).
- K2 calls: every tool's example runs through core.call; report pass / isError counts. PASS if every isError carries a message
  and no call crashes the core; the pass rate itself is reported, not gated (some tools need PC-only data).
- K3 cache: a repeated call returns an identical structuredContent marked cached, in <= 20 ms.
- K4 provenance: every call (K2) appends exactly one ledger record with all fields; a cached call links to its source record.
- K5 bad input: wrong type / missing required field returns isError with a message naming the field, without running the tool.
Fails recorded as failed-as-locked; fixes via DEVIATIONS first; one rerun.
