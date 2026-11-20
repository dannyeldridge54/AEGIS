# (c) Danny Lee Eldridge · AEGIS Community License (business use needs the Commercial License)
"""H1a provenance block (module name prov_block: tools/provenance/ is an older, separate package) (19-20 Nov 2026): what made an exported table, so a referee can reproduce it.
provenance(toolkit, settings, sources, dnotes) -> dict with toolkit, version (git short hash of the repo, '+dirty' when the
working tree has changes), UTC timestamp, the input settings, the dataset sources used, and the D-notes that validated
the routines. Exports (Hyperion/Janus export(), CERN+1 scan()) embed it when given prov=...:
  JSON -> {"provenance": {...}, "rows": [...]};  CSV -> '# key: value' comment lines first (pandas: comment='#');
  ECSV -> a 'meta: provenance:' block inside the ECSV YAML header (astropy reads it into table.meta)."""
import datetime, json, os, subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def version():
    try:
        h = subprocess.run(['git', '-C', ROOT, 'rev-parse', '--short', 'HEAD'], capture_output=True, text=True, timeout=5).stdout.strip()
        d = subprocess.run(['git', '-C', ROOT, 'status', '--porcelain', '--untracked-files=no'], capture_output=True, text=True, timeout=5).stdout.strip()
        return (h or 'unknown') + ('+dirty' if d else '')
    except Exception:
        return 'unknown'

def provenance(toolkit, settings=None, sources=None, dnotes=None):
    return {'toolkit': toolkit, 'version': version(),
            'created_utc': datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
            'settings': settings or {}, 'sources': list(sources or []), 'validated_by': list(dnotes or [])}

def comment_lines(prov, prefix='# '):
    return ''.join(f"{prefix}{k}: {json.dumps(v, default=str) if isinstance(v, (dict, list)) else v}\n" for k, v in prov.items())

def ecsv_meta(prov):
    """YAML lines (each starting '# ') for the ECSV header; values written as JSON, which is valid YAML flow style."""
    return '# meta:\n#   provenance:\n' + ''.join(f"#     {k}: {json.dumps(v, default=str)}\n" for k, v in prov.items())
