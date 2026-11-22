"""src/sky-data.js dosyasını d3-celestial verisinden üretir.

d3-celestial (Olaf Frohn, BSD-3, bkz. third_party/) npm paketini indirip açtıktan sonra:
  python3 tools/make_data.py <paket>/data
Yıldızlar 5,3 kadire kadar; adlı yıldızlar (≤2,6 kadir + birkaç ünlü yıldız);
88 takımyıldız (Türkçe adlar, çizgiler, merkez); Samanyolu'nun iki katmanı (seyreltilmiş).
"""
import json
import sys
from pathlib import Path

src = Path(sys.argv[1])
out = Path(__file__).resolve().parent.parent / "src" / "sky-data.js"
load = lambda name: json.loads((src / name).read_text(encoding="utf-8"))
ra360 = lambda x: x + 360 if x < 0 else x
EXTRA = {65378, 95947, 17702, 11767, 14576, 87833, 69673, 1067, 8903, 113881}

names = load("starnames.json")
stars, named = [], {}
for f in load("stars.6.json")["features"]:
    mag = f["properties"]["mag"]
    if mag > 5.3:
        continue
    ra, dec = f["geometry"]["coordinates"]
    ra = ra360(ra)
    try:
        bv = float(f["properties"]["bv"])
    except (TypeError, ValueError):
        bv = 0.6
    stars.append([round(ra, 2), round(dec, 2), round(mag, 1), round(bv, 1)])
    n = names.get(str(f["id"]), {})
    if n.get("name") and (mag <= 2.6 or f["id"] in EXTRA):
        named[f["id"]] = [n["name"], n.get("c", ""), round(ra, 2), round(dec, 2), round(mag, 1)]

cons = {}
for f in load("constellations.json")["features"]:
    p = f["properties"]
    lon, lat = f["geometry"]["coordinates"]
    cons[f["id"]] = {"tr": p["tr"].replace(" ", " "), "la": p["name"],
                     "c": [round(ra360(lon), 1), round(lat, 1)], "r": int(p["rank"])}
for f in load("constellations.lines.json")["features"]:
    cons.setdefault(f["id"], {})["l"] = [
        [[round(ra360(x), 2), round(y, 2)] for x, y in line] for line in f["geometry"]["coordinates"]]

mw = []
for f in load("mw.json")["features"][:2]:
    for poly in f["geometry"]["coordinates"]:
        for ring in poly:
            step = max(1, len(ring) // 120)
            pts = [[round(ra360(x), 1), round(y, 1)] for x, y in ring[::step]]
            if len(pts) > 6:
                mw.append([f["id"][-1], pts])

data = {"stars": stars, "named": named, "cons": cons, "mw": mw}
out.write_text("window.SKY=" + json.dumps(data, separators=(",", ":"), ensure_ascii=False) + ";", encoding="utf-8")
print(f"{len(stars)} yıldız, {len(named)} adlı, {len(cons)} takımyıldız, {len(mw)} Samanyolu halkası -> {out}")
