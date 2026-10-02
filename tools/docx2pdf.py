#!/usr/bin/env python3
"""Converte um .docx em PDF sem LibreOffice: docx -> HTML simples -> Chrome headless.

Uso: python3 tools/docx2pdf.py <entrada.docx> <saida.pdf> [título]

Preserva títulos (estilos Heading/Título N), parágrafos, negrito, itálico,
listas numeradas/marcadas (como recuo) e tabelas. Não reproduz a diagramação
exata do Word (cabeçalhos de página, numeração automática, imagens).
"""
import html
import re
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
CHROME = "google-chrome"

CSS = """
@page { size: A4; margin: 22mm 20mm 22mm 20mm; }
body { font-family: Georgia, 'Times New Roman', serif; font-size: 11pt; line-height: 1.45; color: #111; }
h1 { font-size: 17pt; margin: 18pt 0 8pt; page-break-after: avoid; }
h2 { font-size: 14pt; margin: 16pt 0 6pt; page-break-after: avoid; }
h3 { font-size: 12pt; margin: 14pt 0 6pt; page-break-after: avoid; }
h4, h5, h6 { font-size: 11pt; margin: 12pt 0 4pt; page-break-after: avoid; }
p { margin: 0 0 7pt; text-align: justify; }
p.li { margin-left: 1.6em; }
p.li2 { margin-left: 3.2em; }
table { border-collapse: collapse; width: 100%; margin: 8pt 0 10pt; font-size: 9.5pt; page-break-inside: auto; }
td, th { border: 1px solid #999; padding: 3pt 5pt; vertical-align: top; }
.capa { font-size: 9pt; color: #555; border-bottom: 1px solid #999; padding-bottom: 6pt; margin-bottom: 14pt; }
"""


def run_html(r):
    text = "".join(t.text or "" for t in r.iter(W + "t"))
    if not text:
        if r.find(W + "br") is not None or r.find(W + "tab") is not None:
            return " "
        return ""
    s = html.escape(text)
    rpr = r.find(W + "rPr")
    if rpr is not None:
        if rpr.find(W + "b") is not None and (rpr.find(W + "b").get(W + "val") not in ("0", "false")):
            s = "<b>%s</b>" % s
        if rpr.find(W + "i") is not None and (rpr.find(W + "i").get(W + "val") not in ("0", "false")):
            s = "<i>%s</i>" % s
    return s


def para_html(p):
    inner = "".join(run_html(r) for r in p.iter(W + "r")).strip()
    if not inner:
        return ""
    ppr = p.find(W + "pPr")
    style = ""
    level = None
    if ppr is not None:
        ps = ppr.find(W + "pStyle")
        if ps is not None:
            style = ps.get(W + "val") or ""
        num = ppr.find(W + "numPr")
        if num is not None:
            il = num.find(W + "ilvl")
            level = int(il.get(W + "val")) if il is not None and il.get(W + "val") else 0
    m = re.match(r"(?:Heading|Ttulo|Título|Title)(\d)?", style)
    if m:
        n = int(m.group(1)) if m.group(1) else 1
        return "<h%d>%s</h%d>" % (min(n, 6), inner, min(n, 6))
    if level is not None:
        return '<p class="%s">%s</p>' % ("li2" if level >= 1 else "li", inner)
    return "<p>%s</p>" % inner


def table_html(tbl):
    rows = []
    for tr in tbl.findall(W + "tr"):
        cells = []
        for tc in tr.findall(W + "tc"):
            cells.append("<td>%s</td>" % "".join(para_html(p) for p in tc.findall(W + "p")))
        rows.append("<tr>%s</tr>" % "".join(cells))
    return "<table>%s</table>" % "".join(rows)


def docx_to_html(path, title):
    root = ET.fromstring(zipfile.ZipFile(path).read("word/document.xml"))
    body = root.find(W + "body")
    parts = []
    for el in body:
        if el.tag == W + "p":
            parts.append(para_html(el))
        elif el.tag == W + "tbl":
            parts.append(table_html(el))
    cover = '<p class="capa">%s — convertido do original .docx para PDF; a diagramação do Word não é reproduzida.</p>' % html.escape(title)
    return "<!DOCTYPE html><html lang='pt-BR'><head><meta charset='utf-8'><title>%s</title><style>%s</style></head><body>%s%s</body></html>" % (
        html.escape(title), CSS, cover, "\n".join(parts))


def main():
    src, dst = Path(sys.argv[1]), Path(sys.argv[2])
    title = sys.argv[3] if len(sys.argv) > 3 else src.stem
    page = docx_to_html(src, title)
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as f:
        f.write(page)
        tmp = f.name
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-sandbox", "--no-pdf-header-footer",
                    "--virtual-time-budget=20000", "--print-to-pdf=%s" % dst.resolve(), "file://%s" % tmp],
                   check=True, capture_output=True)
    print("%s: %d KB" % (dst, dst.stat().st_size // 1024))


if __name__ == "__main__":
    main()
