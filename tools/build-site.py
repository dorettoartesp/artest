#!/usr/bin/env python3
"""Porta os slides do deck (formato do tipo Slides do claude.ai) para reveal.js.

Entrada : uma pasta com `project/deck.json` e `project/slides/<id>.html`
          (a cópia local do artifact de backup).
Saída   : `site/index.html`, HTML estático servido pelo GitHub Pages.

Uso: python3 tools/build-site.py <pasta-do-deck> [site/index.html]

O formato de origem usa elementos próprios (`x-connector`, `x-shape`, `x-icon`)
e imagens `/_blob/<id>`; aqui eles viram SVG inline e arquivos em `site/img/`.
Todo o resto (flex, grid, estilos inline) é CSS comum e passa sem alteração.
"""
import json
import re
import sys
from pathlib import Path

SRC = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("deck")
OUT = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("site/index.html")

BLOBS = {
    "7924e60fcd2711868611dc4e8e6f8f9b": "img/logo-positivo.png",
    "04fff215c35ba1d0825f89980ae58be1": "img/logo-cor-branco.png",
    "20efbd507a608911da287dcdb2827456": "img/logo-negativo.png",
}

# Ícones de linha (24x24, traço 2, estilo Feather). Só os usados no deck.
ICONS = {
    "Database": '<ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M3 5v14c0 1.7 4 3 9 3s9-1.3 9-3V5"/><path d="M3 12c0 1.7 4 3 9 3s9-1.3 9-3"/>',
    "Chart": '<path d="M18 20V10M12 20V4M6 20v-6"/>',
    "Link": '<path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/>',
    "Settings": '<circle cx="12" cy="12" r="3"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3M4.9 4.9l2.1 2.1M17 17l2.1 2.1M4.9 19.1l2.1-2.1M17 7l2.1-2.1"/>',
    "Lock": '<rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/>',
    "Clock": '<circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>',
    "Users": '<circle cx="9" cy="7" r="4"/><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>',
    "Activity": '<polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/>',
    "Verified": '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><polyline points="9 12 11 14 15 10"/>',
    "Code": '<polyline points="16 18 22 12 16 6"/><polyline points="8 6 2 12 8 18"/>',
    "Play": '<polygon points="5 3 19 12 5 21"/>',
    "Book": '<path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/>',
    "Check": '<polyline points="20 6 9 17 4 12"/>',
    "Warning": '<path d="M10.29 3.86 1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/>',
}

marker_seq = 0


def attr(tag, name, default=None):
    m = re.search(r'\b%s="([^"]*)"' % name, tag)
    return m.group(1) if m else default


def style_get(style, prop):
    m = re.search(r'(?:^|;)\s*%s\s*:\s*([^;]+)' % re.escape(prop), style or "")
    return m.group(1).strip() if m else None


def connector(tag):
    """<x-connector x1 y1 x2 y2 head route style> -> SVG absoluto cobrindo o host."""
    global marker_seq
    x1, y1, x2, y2 = (attr(tag, k) for k in ("x1", "y1", "x2", "y2"))
    head = attr(tag, "head", "end")
    style = attr(tag, "style", "")
    color = style_get(style, "color") or "#141414"
    width = (style_get(style, "border-width") or "2px").replace("px", "")
    dashed = (style_get(style, "border-style") or "") == "dashed"
    marker_seq += 1
    mid = "m%d" % marker_seq
    defs = ""
    marker_attr = ""
    if head in ("end", "both"):
        defs = ('<defs><marker id="%s" markerWidth="14" markerHeight="14" refX="13" refY="7" '
                'orient="auto" markerUnits="userSpaceOnUse"><path d="M1 1 L13 7 L1 13 z" fill="%s"/></marker></defs>'
                % (mid, color))
        marker_attr = ' marker-end="url(#%s)"' % mid
        if head == "both":
            marker_attr += ' marker-start="url(#%s)"' % mid
    dash = ' stroke-dasharray="14 10"' if dashed else ""
    return ('<svg class="cx" aria-hidden="true" style="position:absolute;left:0;top:0;width:100%%;height:100%%;'
            'overflow:visible;pointer-events:none">%s<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="%s" '
            'stroke-width="%s" stroke-linecap="round"%s%s/></svg>'
            % (defs, x1, y1, x2, y2, color, width, dash, marker_attr))


def shape(tag):
    kind = attr(tag, "kind", "rect")
    style = attr(tag, "style", "")
    bg = style_get(style, "background") or "#141414"
    if kind == "ellipse":
        return '<div style="%s;border-radius:50%%"></div>' % style
    # nas setas o preenchimento vai para o polígono, não para a caixa do SVG
    nobg = re.sub(r'(?:^|;)\s*background\s*:[^;]*', '', style).strip(';')
    if kind == "arrow-down":
        return ('<svg aria-hidden="true" style="%s;flex:none" viewBox="0 0 32 22" preserveAspectRatio="none">'
                '<polygon points="0,0 32,0 16,22" fill="%s"/></svg>' % (nobg, bg))
    if kind == "arrow-right":
        return ('<svg aria-hidden="true" style="%s;flex:none" viewBox="0 0 32 22" preserveAspectRatio="none">'
                '<polygon points="0,0 32,11 0,22" fill="%s"/></svg>' % (nobg, bg))
    return '<div style="%s"></div>' % style


def icon(tag):
    name = attr(tag, "name", "")
    style = attr(tag, "style", "")
    body = ICONS.get(name)
    if body is None:
        raise SystemExit("ícone sem desenho: %s" % name)
    return ('<svg class="ic" aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            'stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="%s;flex:none">%s</svg>'
            % (style, body))


def convert(html):
    # elementos próprios do formato de origem
    html = re.sub(r'<x-connector\b[^>]*>\s*</x-connector>', lambda m: connector(m.group(0)), html)
    html = re.sub(r'<x-shape\b[^>]*>\s*</x-shape>', lambda m: shape(m.group(0)), html)
    html = re.sub(r'<x-icon\b[^>]*>\s*</x-icon>', lambda m: icon(m.group(0)), html)
    # imagens do armazenamento do artifact
    html = re.sub(r'/_blob/([0-9a-f]{32})', lambda m: BLOBS[m.group(1)], html)
    # fundo decorativo (SVG pinado cobrindo a lona) fica atrás do conteúdo em fluxo
    html = html.replace('<svg style="position:absolute;left:0;top:0" width="1920" height="1080"',
                        '<svg class="bg" aria-hidden="true" style="position:absolute;left:0;top:0;z-index:-1" width="1920" height="1080"')
    # comentários de geometria (anotações de trabalho) saem
    html = re.sub(r'<!--.*?-->', '', html, flags=re.S)
    # <section id style data-transition> -> <section data-transition><div class="sl" id style>
    m = re.match(r'\s*<section\b([^>]*)>(.*)</section>\s*$', html, flags=re.S)
    if not m:
        raise SystemExit("slide sem <section> único")
    head, body = m.group(1), m.group(2)
    sid = attr(head, "id")
    style = attr(head, "style", "")
    trans = {"push": "slide", "fade": "fade"}.get(attr(head, "data-transition", "fade"), "fade")
    return ('<section data-transition="%s" data-id="%s">\n<div class="sl" id="%s" style="%s">%s</div>\n</section>\n'
            % (trans, sid, sid, style, body.strip()))


def main():
    deck = json.loads((SRC / "project" / "deck.json").read_text(encoding="utf-8"))
    title = deck.get("title", "Apresentação")
    slides = []
    for sid in deck["order"]:
        f = SRC / "project" / "slides" / ("%s.html" % sid)
        slides.append(convert(f.read_text(encoding="utf-8")))
    tpl = (OUT.parent / "template.html").read_text(encoding="utf-8")
    page = tpl.replace("{{TITLE}}", title).replace("{{SLIDES}}", "".join(slides))
    OUT.write_text(page, encoding="utf-8")
    print("%s: %d slides, %d KB" % (OUT, len(slides), len(page.encode("utf-8")) // 1024))


if __name__ == "__main__":
    main()
