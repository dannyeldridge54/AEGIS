# AEGIS-FP 27DB5QS2TZAWKREB · (c) Danny Lee Eldridge · AEGIS Community License (business use needs the Commercial License)
"""SERAPIS prediction tracker: re-score the frozen predictions against tools/scorecard's constraints.yaml.
Run from the repo root:  python tools/tracker/track.py   -> docs/tracker/STATUS.md and docs/tracker/index.html
Adding a data release = adding a line to constraints.yaml (with a 'date' field after the freeze to count as a test)."""
import datetime as dt, html, pathlib, yaml
from inflation_scorecard import core

HERE = pathlib.Path(__file__).parent
P = yaml.safe_load((HERE / "predictions.yaml").read_text(encoding="utf-8"))
import sys
C = core.load_constraints(sys.argv[sys.argv.index("--data") + 1] if "--data" in sys.argv else None)
FREEZE = str(P["freeze_date"])

def era(d):
    return "after freeze (TEST)" if str(d.get("date", "")) > FREEZE else "pre-freeze (consistency)"

def status_ns(lo, hi):
    out = []
    for d in C["ns_releases"]:
        near, _ = core.band_distance(lo, hi, d["value"], d["sigma"])
        s = "KILL" if near > 3 else ("tension" if near > 2 else "consistent")
        out.append((d["name"], f"{d['value']} ± {d['sigma']} → {near:.2f}σ from band", s, era(d)))
    return out

def status_r(lo, hi):
    out = []
    for d in C["r_limits"]:
        s = "consistent" if d["limit95"] > hi else ("KILL" if d["limit95"] < lo else "tension")
        out.append((d["name"], f"r < {d['limit95']} (95%) vs band {lo:.1e}–{hi:.1e}: not yet sensitive" if d["limit95"] > hi else f"r < {d['limit95']}", s, era(d)))
    return out

def status_alpha(lo, hi):
    out = []
    for d in C["running"]:
        kill = d["value"] - 3 * d["sigma"] > -3e-4
        mid = 0.5 * (lo + hi); p = (mid - d["value"]) / d["sigma"]
        s = "KILL" if kill else core.verdict(p)
        out.append((d["name"], f"{d['value']} ± {d['sigma']} → {p:+.2f}σ", s, era(d)))
    return out

def status_caps(lo, hi):
    out = []
    for d in C["ns_releases"]:
        s = "KILL" if d["value"] - 3 * d["sigma"] > 0.985 else "consistent"
        out.append((d["name"], f"n_s {d['value']} vs cap 0.985", s, era(d)))
    return out

def status_mnu(v):
    out = []
    for d in C["neutrino_mass_sum_eV"]:
        s = "consistent" if d["limit95"] > v else "pressure (excludes the NO floor)"
        out.append((d["name"], f"< {d['limit95']} eV vs {v}", s, era(d)))
    return out

def status_fnl(v):
    return [(d["name"], f"{d['value']} ± {d['sigma']} vs {v}", "consistent" if abs(d["value"]) - 3 * d["sigma"] < 5 else "KILL", era(d)) for d in C["fnl_local"]]

def build():
    rows = []
    for pr in P["predictions"]:
        f = {"ns": lambda: status_ns(*pr["band"]), "r": lambda: status_r(*pr["band"]), "alpha": lambda: status_alpha(*pr["band"]),
             "caps": lambda: status_caps(*pr["band"]), "mnu": lambda: status_mnu(pr["value"]), "fnl": lambda: status_fnl(pr["value"])}[pr["id"]]
        rows.append((pr, f()))
    return rows

def overall(checks):
    ss = [c[2] for c in checks]
    return "KILL" if "KILL" in ss else ("tension" if any(s.startswith(("tension", "pressure", "fail")) for s in ss) else "alive")

def main():
    today = dt.date.today().isoformat(); rows = build()
    out = pathlib.Path(sys.argv[sys.argv.index("--out") + 1]) if "--out" in sys.argv else pathlib.Path("docs/tracker"); out.mkdir(parents=True, exist_ok=True)
    md = [f"# SERAPIS prediction tracker — status {today}", "",
          f"Predictions frozen {FREEZE} (locks in field_tests/rules). Data file version {C['version']}. Only data dated after the freeze count as tests; earlier data show consistency only.", "",
          "| Prediction | Frozen value | Kill condition | Status |", "|---|---|---|---|"]
    for pr, ch in rows:
        val = f"{pr['band'][0]:g} – {pr['band'][1]:g}" if "band" in pr else f"{pr['value']:g}"
        md.append(f"| {pr['name']} | {val} | {pr['kill']} | **{overall(ch)}** |")
    for pr, ch in rows:
        md += ["", f"## {pr['name']} ({pr['locks']})", "", "| Dataset | Comparison | Status | Counts as |", "|---|---|---|---|"]
        md += [f"| {a} | {b} | {c} | {d} |" for a, b, c, d in ch]
    text = "\n".join(md) + "\n"
    (out / "STATUS.md").write_text(text, encoding="utf-8")
    body = []
    for line in md:
        if line.startswith("# "): body.append(f"<h1>{html.escape(line[2:])}</h1>")
        elif line.startswith("## "): body.append(f"<h2>{html.escape(line[3:])}</h2>")
        elif line.startswith("|---"): continue
        elif line.startswith("|"):
            cells = [c.strip() for c in line.strip("|").split("|")]
            tag = "th" if cells[0] in ("Prediction", "Dataset") else "td"
            cls = lambda c: ' class="kill"' if "KILL" in c else (' class="warn"' if ("tension" in c or "pressure" in c) else (' class="ok"' if ("alive" in c or c == "consistent") else ""))
            body.append("<tr>" + "".join(f"<{tag}{cls(c)}>{html.escape(c.replace('**',''))}</{tag}>" for c in cells) + "</tr>")
        elif line: body.append(f"<p>{html.escape(line)}</p>")
    page = []; in_table = False
    for b in body:
        if b.startswith("<tr>") and not in_table: page.append("<table>"); in_table = True
        if not b.startswith("<tr>") and in_table: page.append("</table>"); in_table = False
        page.append(b)
    if in_table: page.append("</table>")
    css = ("body{font-family:system-ui,sans-serif;max-width:960px;margin:2rem auto;padding:0 16px;background:#fff;color:#1b1b1b}"
           "table{border-collapse:collapse;width:100%;margin:.5rem 0 1.5rem}td,th{border-bottom:1px solid #ddd;padding:.35rem .5rem;text-align:left;font-size:.92rem}"
           ".ok{color:#1e6b34;font-weight:600}.warn{color:#9a6200;font-weight:600}.kill{color:#b00020;font-weight:700}"
           "@media (prefers-color-scheme:dark){body{background:#121212;color:#e8e8e8}td,th{border-color:#333}.ok{color:#6fd18b}.warn{color:#f0b54a}.kill{color:#ff6b7a}}")
    (out / "index.html").write_text(f"<!doctype html><html><head><meta charset=utf-8><meta name=viewport content='width=device-width,initial-scale=1'><title>SERAPIS tracker</title><style>{css}</style></head><body>{''.join(page)}</body></html>", encoding="utf-8")
    print(f"wrote {out}/STATUS.md and index.html; overall: " + ", ".join(f"{pr['id']}={overall(ch)}" for pr, ch in rows))

if __name__ == "__main__":
    main()
