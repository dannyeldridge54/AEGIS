"""The GCN daily-archive reader keeps the newest circulars (synthetic tarball, no network)."""
import io, json, tarfile, urllib.request
from aegis import anomaly_scanner as A

def test_gcn_archive_latest(monkeypatch, tmp_path):
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w:gz") as tar:
        for cid in (5, 50, 7, 49):
            data = json.dumps({"circularId": cid, "subject": f"GRB {cid}"}).encode()
            ti = tarfile.TarInfo(f"archive.json/{cid}.json"); ti.size = len(data); tar.addfile(ti, io.BytesIO(data))
    buf.seek(0)
    monkeypatch.setattr(urllib.request, "urlopen", lambda req, timeout=0: buf)
    out = A._gcn_archive_latest("https://example.org/archive.json.tar.gz", keep=2)
    assert [c["circularId"] for c in out] == [50, 49]
    assert A._adapt_gcn(out)[0]["time_tag"] == "50"
