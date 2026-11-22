"""Gece Usturlabı derleyicisi.

src/app.html (uygulama) + src/sky-data.js (gömülü gökyüzü verisi) birleştirilir:
  index.html          -> tek başına açılan tam sayfa (GitHub Pages, çift tıklama)
  dist/artifact.html  -> claude.ai artifact sürümü (iskeletsiz)
Kullanım: python3 tools/build.py
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
app = (ROOT / "src" / "app.html").read_text(encoding="utf-8")
data = (ROOT / "src" / "sky-data.js").read_text(encoding="utf-8")
body = app.replace("/*DATA*/", data, 1)

(ROOT / "dist").mkdir(exist_ok=True)
(ROOT / "dist" / "artifact.html").write_text(body, encoding="utf-8")

page = (
    '<!doctype html>\n<html lang="tr">\n<head>\n<meta charset="utf-8">\n'
    '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
    '<meta name="description" content="Türkiye\'nin 81 ilinden o gece görünen yıldızlar, gezegenler ve takımyıldızlar; Türkçe halk adları ve hikâyeleriyle.">\n'
    "<style>:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}"
    "body{margin:0}img{max-width:100%}[hidden]{display:none!important}</style>\n"
    "</head>\n<body>\n" + body + "\n</body>\n</html>\n"
)
(ROOT / "index.html").write_text(page, encoding="utf-8")
print(f"index.html {len(page)//1024} KB, dist/artifact.html {len(body)//1024} KB")
