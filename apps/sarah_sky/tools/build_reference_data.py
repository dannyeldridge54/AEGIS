"""Build the app's compact reference data from d3-celestial 0.7.35 (BSD-3-Clause) GeoJSON.
Usage: python tools/build_reference_data.py <path to d3-celestial/data>  -> data/constellations.json, data/messier.json, data/stars.json"""
import json, sys, pathlib
src = pathlib.Path(sys.argv[1]); out = pathlib.Path(__file__).resolve().parents[1] / "data"
ra = lambda lon: round(lon % 360, 4)
names = json.load(open(src / "constellations.json", encoding="utf-8"))
lines = {f["id"]: f["geometry"]["coordinates"] for f in json.load(open(src / "constellations.lines.json", encoding="utf-8"))["features"]}
cons = []
for f in names["features"]:
    p = f["properties"]; lon, lat = f["geometry"]["coordinates"]
    cons.append({"id": f["id"], "name": p.get("en") or p["name"], "latin": p["name"], "rank": int(p.get("rank", 3)),
                 "label": [ra(lon), round(lat, 4)],
                 "lines": [[[ra(a), round(b, 4)] for a, b in seg] for seg in lines.get(f["id"], [])]})
json.dump({"source": "d3-celestial 0.7.35 (BSD-3-Clause), IAU constellations; lines after Stellarium", "constellations": cons},
          open(out / "constellations.json", "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
TYPES = {"gc": "Globular cluster", "oc": "Open cluster", "pn": "Planetary nebula", "snr": "Supernova remnant", "en": "Emission nebula",
         "rn": "Reflection nebula", "bn": "Bright nebula", "dn": "Dark nebula", "sg": "Spiral galaxy", "eg": "Elliptical galaxy",
         "ig": "Irregular galaxy", "lg": "Lenticular galaxy", "sp": "Spiral galaxy", "pg": "Peculiar galaxy", "bs": "Asterism", "ds": "Double star",
         "**": "Double star", "as": "Asterism", "cl": "Cluster with nebulosity", "s0": "Lenticular galaxy", "sd": "Dwarf spheroidal galaxy",
         "i": "Irregular galaxy", "e": "Elliptical galaxy", "s": "Spiral galaxy", "pos": "Star field"}
mes = []
for f in json.load(open(src / "messier.json", encoding="utf-8"))["features"]:
    p = f["properties"]; lon, lat = f["geometry"]["coordinates"]
    mes.append({"id": p["name"], "ngc": p.get("desig", ""), "common": p.get("alt", ""), "type": TYPES.get(p.get("type", ""), p.get("type", "")),
                "mag": p.get("mag"), "ra": ra(lon), "dec": round(lat, 4)})
json.dump({"source": "d3-celestial 0.7.35 (BSD-3-Clause), Messier catalogue", "objects": mes},
          open(out / "messier.json", "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
sn = json.load(open(src / "starnames.json", encoding="utf-8"))
stars = []
for f in json.load(open(src / "stars.6.json", encoding="utf-8"))["features"]:
    hip = str(f["id"]); p = f["properties"]; n = sn.get(hip, {})
    if not n.get("name") or float(p["mag"]) > 4.5: continue
    lon, lat = f["geometry"]["coordinates"]
    desig = (n.get("bayer") or n.get("flam") or "") + (" " + n["c"] if n.get("c") else "")
    stars.append({"name": n["name"], "desig": desig.strip(), "hip": int(hip), "mag": float(p["mag"]), "bv": p.get("bv"), "ra": ra(lon), "dec": round(lat, 4)})
stars.sort(key=lambda s: s["mag"])
json.dump({"source": "d3-celestial 0.7.35 (BSD-3-Clause): Hipparcos positions and IAU star names, V < 4.5", "stars": stars},
          open(out / "stars.json", "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
print(len(cons), "constellations,", len(mes), "Messier,", len(stars), "named stars")
