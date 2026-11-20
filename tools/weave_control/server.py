# (c) Danny Lee Eldridge · AEGIS Community License (business use needs the Commercial License)
"""Weave Control local server (W3). Run: python3 -m tools.weave_control.server [port]  → open http://127.0.0.1:8790/
GET /           the control panel (ui/index.html)
POST /api/run   JSON params → engine.run(params) + knobs + provenance
GET /api/finder?target=M31&field=6  → PNG finder chart (Mapper)
Binds to 127.0.0.1 only."""
import io, json, os, sys, tempfile, urllib.parse
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from tools.weave_control import engine as E
UI = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ui')

def run_payload(params):
    from tools.prov_block import provenance
    r = E.run(params); r['knobs'] = E.knobs(); r['provenance'] = provenance('Weave Control', r['params'], [], ['PREREG_W2_LINKS', 'D1725', 'D1322'])
    return json.dumps(r, default=lambda o: float(o) if hasattr(o, '__float__') else str(o))

class H(BaseHTTPRequestHandler):
    def _send(self, code, body, ctype):
        b = body if isinstance(body, bytes) else body.encode()
        self.send_response(code); self.send_header('Content-Type', ctype); self.send_header('Content-Length', str(len(b)))
        self.send_header('Cache-Control', 'no-store'); self.end_headers(); self.wfile.write(b)
    def log_message(self, *a): pass
    def do_GET(self):
        u = urllib.parse.urlparse(self.path)
        if u.path in ('/', '/index.html'): return self._send(200, open(os.path.join(UI, 'index.html'), 'rb').read(), 'text/html; charset=utf-8')
        if u.path == '/api/run': return self._send(200, run_payload({}), 'application/json')
        if u.path == '/api/finder':
            q = urllib.parse.parse_qs(u.query); t = q.get('target', ['M31'])[0]; fld = float(q.get('field', ['6'])[0])
            from tools.mapper import finder
            with tempfile.TemporaryDirectory() as d:
                out = os.path.join(d, 'f.png')
                try: finder.chart(t, field_deg=max(0.5, min(fld, 40)), fov_arcmin=(60,), out=out, invert=False)
                except Exception as e: return self._send(400, json.dumps(dict(error=str(e))), 'application/json')
                return self._send(200, open(out, 'rb').read(), 'image/png')
        self._send(404, 'not found', 'text/plain')
    def do_POST(self):
        if self.path != '/api/run': return self._send(404, 'not found', 'text/plain')
        n = int(self.headers.get('Content-Length', 0) or 0)
        try: params = json.loads(self.rfile.read(n) or b'{}')
        except Exception: return self._send(400, json.dumps(dict(error='bad JSON')), 'application/json')
        clean = {k: v for k, v in params.items() if k in E.DEFAULTS}
        try: self._send(200, run_payload(clean), 'application/json')
        except Exception as e: self._send(500, json.dumps(dict(error=repr(e))), 'application/json')

if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8790
    print(f'Weave Control on http://127.0.0.1:{port}/'); ThreadingHTTPServer(('127.0.0.1', port), H).serve_forever()
