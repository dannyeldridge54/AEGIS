"""The GCN reader takes the newest circular numbers from the listing page and fetches each as JSON (no network)."""
import io, json, urllib.request
from aegis import anomaly_scanner as A

def test_gcn_recent(monkeypatch):
    html = b'<a href="/circulars/46300">x</a><a href="/circulars/46299">y</a><a href="/circulars/archive.json.tar.gz">z</a>'
    def fake(req, timeout=0):
        u = req.full_url
        if u.endswith(".json"):
            cid = int(u.rsplit("/", 1)[1][:-5])
            if cid == 46298:
                raise OSError("missing")
            return io.BytesIO(json.dumps({"circularId": cid, "subject": f"GRB {cid}"}).encode())
        return io.BytesIO(html)
    monkeypatch.setattr(urllib.request, "urlopen", fake)
    out = A._gcn_recent("https://gcn.nasa.gov/circulars?limit=20", keep=3)
    assert [c["circularId"] for c in out] == [46300, 46299]
    assert A._adapt_gcn(out)[0]["score"] == 1.0
