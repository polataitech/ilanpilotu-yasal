"""Converts the policy markdown files from the EmlakPilot repo into static HTML (no dependencies)."""
import html, re, sys, pathlib

SRC = pathlib.Path(sys.argv[1])
OUT = pathlib.Path(__file__).parent
PAGES = {"privacy-tr.md": "gizlilik.html", "terms-tr.md": "kosullar.html"}

CSS = """body{font:16px/1.6 -apple-system,system-ui,sans-serif;max-width:720px;margin:2rem auto;padding:0 1rem;color:#1c1c1e}
h1{font-size:1.6rem}h2{font-size:1.15rem;margin-top:1.6rem}a{color:#0b57d0}ul{padding-left:1.2rem}
@media(prefers-color-scheme:dark){body{background:#1c1c1e;color:#f2f2f7}a{color:#8ab4f8}}"""

def inline(t):
    t = html.escape(t)
    return re.sub(r"`([^`]+)`", r"<code>\1</code>", t)

def convert(md):
    # Drop the internal draft note: paragraph starting with "Taslak."
    md = re.sub(r"^Taslak\..*?\n\n", "", md, count=1, flags=re.S | re.M)
    out, para, lst = [], [], None
    def flush():
        nonlocal para, lst
        if para: out.append("<p>" + inline(" ".join(para)) + "</p>"); para = []
        if lst: out.append(f"</{lst}>"); lst = None
    for line in md.splitlines():
        if not line.strip(): flush(); continue
        if line.startswith("# "): flush(); out.append(f"<h1>{inline(line[2:])}</h1>"); continue
        if line.startswith("## "): flush(); out.append(f"<h2>{inline(line[3:])}</h2>"); continue
        m = re.match(r"^\s*(?:[-•]|\d+\.)\s+(.*)", line)
        if m:
            if para: out.append("<p>" + inline(" ".join(para)) + "</p>"); para = []
            if not lst: lst = "ul"; out.append("<ul>")
            out.append(f"<li>{inline(m.group(1))}</li>"); continue
        if lst and line.startswith(" "): out[-1] = out[-1][:-5] + " " + inline(line.strip()) + "</li>"; continue
        para.append(line.strip())
    flush()
    return "\n".join(out)

for src, dst in PAGES.items():
    body = convert((SRC / src).read_text(encoding="utf-8"))
    title = re.search(r"<h1>(.*?)</h1>", body).group(1)
    (OUT / dst).write_text(f'<!doctype html><html lang="tr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title}</title><style>{CSS}</style></head><body>\n{body}\n</body></html>\n', encoding="utf-8")
(OUT / "index.html").write_text('<!doctype html><html lang="tr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>İlan Pilotu</title><style>' + CSS + '</style></head><body><h1>İlan Pilotu</h1><ul><li><a href="gizlilik.html">Gizlilik Politikası</a></li><li><a href="kosullar.html">Kullanım Şartları</a></li></ul></body></html>\n', encoding="utf-8")
