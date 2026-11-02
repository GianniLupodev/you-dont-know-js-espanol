#!/usr/bin/env python3
"""
You Don't Know JS Yet — Edición en Español
Fábrica de sitio: convierte el markdown traducido (es/) en un sitio HTML
colorido y didáctico (site/), con navegación multipágina.

Sin dependencias externas. Solo stdlib. Funciona offline (file://).

Uso:  python3 build.py
"""

import os
import re
import html
import shutil
import json

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "es")          # markdown traducido
OUT = os.path.join(ROOT, "site")        # HTML generado
IMG_SRC_ROOT = ROOT                      # las imágenes viven en <libro>/images/

# ---------------------------------------------------------------------------
# ESTRUCTURA DE LA SERIE
# Orden de libros y de capítulos dentro de cada libro. El título es el que se
# muestra en la UI. "file" es el nombre del .md dentro de es/<slug>/.
# ---------------------------------------------------------------------------
SERIE = [
    {
        "slug": "get-started",
        "titulo": "Get Started",
        "subtitulo": "Empezando",
        "emoji": "🚀",
        "color": "#6366f1",
        "caps": [
            ("README", "Portada"),
            ("foreword", "Prólogo"),
            ("toc", "Índice"),
            ("ch1", "Cap. 1 · ¿Qué es JavaScript?"),
            ("ch2", "Cap. 2 · Mirando JS por encima"),
            ("ch3", "Cap. 3 · Cavando en las raíces de JS"),
            ("ch4", "Cap. 4 · Los tres pilares"),
            ("apA", "Apéndice A · Explorando más a fondo"),
            ("apB", "Apéndice B · Práctica, práctica, práctica"),
        ],
    },
    {
        "slug": "scope-closures",
        "titulo": "Scope & Closures",
        "subtitulo": "Scope y Closures",
        "emoji": "🔭",
        "color": "#0ea5e9",
        "caps": [
            ("README", "Portada"),
            ("foreword", "Prólogo"),
            ("toc", "Índice"),
            ("ch1", "Cap. 1 · ¿Qué es el Scope?"),
            ("ch2", "Cap. 2 · Ilustrando el Scope léxico"),
            ("ch3", "Cap. 3 · El alcance de la cadena de scopes"),
            ("ch4", "Cap. 4 · Scope global"),
            ("ch5", "Cap. 5 · El (no tan) secreto de los closures"),
            ("ch6", "Cap. 6 · Exponer el scope con módulos"),
            ("ch7", "Cap. 7 · Usar los closures"),
            ("ch8", "Cap. 8 · El patrón módulo"),
            ("apA", "Apéndice A · Explorando más a fondo"),
            ("apB", "Apéndice B · Práctica"),
        ],
    },
    {
        "slug": "objects-classes",
        "titulo": "Objects & Classes",
        "subtitulo": "Objetos y Clases",
        "emoji": "🧩",
        "color": "#8b5cf6",
        "caps": [
            ("README", "Portada"),
            ("foreword", "Prólogo"),
            ("toc", "Índice"),
            ("ch1", "Cap. 1 · Objetos"),
            ("ch2", "Cap. 2 · Cómo funcionan los objetos"),
            ("ch3", "Cap. 3 · Clases"),
            ("ch4", "Cap. 4 · Esto es por qué \"this\""),
            ("ch5", "Cap. 5 · Delegación"),
            ("thanks", "Agradecimientos"),
        ],
    },
    {
        "slug": "types-grammar",
        "titulo": "Types & Grammar",
        "subtitulo": "Tipos y Gramática",
        "emoji": "🔡",
        "color": "#ec4899",
        "caps": [
            ("README", "Portada"),
            ("foreword", "Prólogo"),
            ("toc", "Índice"),
            ("ch1", "Cap. 1 · Tipos primitivos"),
            ("ch2", "Cap. 2 · Valores primitivos"),
            ("ch3", "Cap. 3 · Valores de objeto"),
            ("ch4", "Cap. 4 · Coerción de valores"),
            ("thanks", "Agradecimientos"),
        ],
    },
    {
        "slug": "sync-async",
        "titulo": "Sync & Async",
        "subtitulo": "Sincronía y Asincronía",
        "emoji": "⏳",
        "color": "#f59e0b",
        "caps": [
            ("README", "Portada"),
            ("foreword", "Prólogo"),
            ("toc", "Índice"),
            ("ch1", "Cap. 1 · Promesas"),
        ],
    },
    {
        "slug": "es-next-beyond",
        "titulo": "ES.Next & Beyond",
        "subtitulo": "ES.Next y Más Allá",
        "emoji": "🌌",
        "color": "#10b981",
        "caps": [
            ("README", "Portada"),
            ("foreword", "Prólogo"),
            ("toc", "Índice"),
            ("ch1", "Cap. 1 · ES.Next y más allá"),
        ],
    },
]

# ---------------------------------------------------------------------------
# PARSER MARKDOWN → HTML  (a medida de las convenciones de YDKJS)
# ---------------------------------------------------------------------------

CALLOUT_MAP = {
    "NOTE": ("nota", "📝", "NOTA"),
    "NOTA": ("nota", "📝", "NOTA"),
    "TIP": ("tip", "💡", "TIP"),
    "WARNING": ("warning", "⚠️", "ADVERTENCIA"),
    "ADVERTENCIA": ("warning", "⚠️", "ADVERTENCIA"),
    "FUN FACT": ("fun", "🎉", "DATO CURIOSO"),
    "DATO CURIOSO": ("fun", "🎉", "DATO CURIOSO"),
    "DETAIL": ("nota", "🔎", "DETALLE"),
    "DETALLE": ("nota", "🔎", "DETALLE"),
}

INLINE_CODE_RE = re.compile(r"`([^`]+)`")
BOLD_RE = re.compile(r"\*\*([^*]+)\*\*")
ITALIC_RE = re.compile(r"(?<!\*)\*(?!\*)([^*]+?)\*(?!\*)")
LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
IMG_RE = re.compile(r"!\[([^\]]*)\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
FOOTREF_RE = re.compile(r"\[\^([^\]]+)\]")


def esc(text):
    return html.escape(text, quote=False)


def inline(text):
    """Convierte formato inline markdown a HTML. El texto llega SIN escapar."""
    # Proteger código inline primero (no se le aplica otro formato)
    tokens = {}

    def stash(m):
        key = "\x00%d\x00" % len(tokens)
        tokens[key] = "<code>%s</code>" % esc(m.group(1))
        return key

    text = INLINE_CODE_RE.sub(stash, text)

    # Imágenes antes que links
    def img_sub(m):
        return '<img src="%s" alt="%s" loading="lazy">' % (m.group(2), esc(m.group(1)))
    text = IMG_RE.sub(img_sub, text)

    # Escapar el resto del texto
    text = esc(text)

    # Links (operan sobre texto ya escapado; las URLs no suelen tener < > &)
    text = LINK_RE.sub(
        lambda m: '<a href="%s">%s</a>' % (m.group(2), m.group(1)), text
    )

    # Footnote refs
    text = FOOTREF_RE.sub(
        lambda m: '<sup class="fnref"><a href="#fn-%s">[%s]</a></sup>'
        % (m.group(1), m.group(1)),
        text,
    )

    text = BOLD_RE.sub(r"<strong>\1</strong>", text)
    text = ITALIC_RE.sub(r"<em>\1</em>", text)

    # Restaurar código inline
    for key, val in tokens.items():
        text = text.replace(key, val)
    return text


def slugify(text):
    text = re.sub(r"<[^>]+>", "", text)
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text, flags=re.UNICODE)
    text = re.sub(r"[\s]+", "-", text)
    return text


def convert(md, rel_prefix=""):
    """Convierte markdown a (html, lista_de_headings_para_TOC)."""
    lines = md.split("\n")
    out = []
    headings = []
    footnotes = {}
    i = 0
    n = len(lines)

    while i < n:
        line = lines[i]

        # Definición de footnote:  [^id]: texto
        m = re.match(r"^\[\^([^\]]+)\]:\s*(.*)$", line)
        if m:
            footnotes[m.group(1)] = m.group(2)
            i += 1
            continue

        # Bloque de código cercado
        if line.startswith("```"):
            lang = line[3:].strip() or "text"
            code_lines = []
            i += 1
            while i < n and not lines[i].startswith("```"):
                code_lines.append(lines[i])
                i += 1
            i += 1  # saltar el ``` de cierre
            code = esc("\n".join(code_lines))
            out.append(
                '<div class="code-block" data-lang="%s"><button class="copy-btn" '
                'title="Copiar código">Copiar</button><pre><code class="lang-%s">%s</code></pre></div>'
                % (lang, lang, code)
            )
            continue

        # Callout tipo tabla:  | NOTE: |  seguido de  | :--- |  y filas de contenido
        m = re.match(r"^\|\s*([A-Za-zÁÉÍÓÚÑ ]+?):\s*\|\s*$", line)
        if m and i + 1 < n and re.match(r"^\|\s*:?-+:?\s*\|\s*$", lines[i + 1]):
            label = m.group(1).strip().upper()
            if label in CALLOUT_MAP:
                cls, emoji, titulo = CALLOUT_MAP[label]
                i += 2
                body = []
                while i < n and lines[i].startswith("|"):
                    cell = lines[i].strip().strip("|").strip()
                    body.append(cell)
                    i += 1
                body_html = inline(" ".join(body))
                out.append(
                    '<div class="callout callout-%s"><div class="callout-head">'
                    '<span class="callout-ico">%s</span>%s</div>'
                    '<div class="callout-body"><p>%s</p></div></div>'
                    % (cls, emoji, titulo, body_html)
                )
                continue

        # Tabla GFM genérica
        if line.startswith("|") and i + 1 < n and re.match(r"^\|[\s:|-]+\|\s*$", lines[i + 1]):
            header = [c.strip() for c in line.strip().strip("|").split("|")]
            i += 2
            rows = []
            while i < n and lines[i].startswith("|"):
                rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                i += 1
            thead = "".join("<th>%s</th>" % inline(h) for h in header)
            tbody = ""
            for r in rows:
                tbody += "<tr>" + "".join("<td>%s</td>" % inline(c) for c in r) + "</tr>"
            out.append(
                '<div class="table-wrap"><table><thead><tr>%s</tr></thead>'
                "<tbody>%s</tbody></table></div>" % (thead, tbody)
            )
            continue

        # Encabezados
        m = re.match(r"^(#{1,6})\s+(.*)$", line)
        if m:
            level = len(m.group(1))
            text = m.group(2).strip()
            sid = slugify(text)
            content = inline(text)
            if level >= 2 and level <= 3:
                headings.append((level, content, sid))
            out.append('<h%d id="%s">%s</h%d>' % (level, sid, content, level))
            i += 1
            continue

        # Regla horizontal
        if re.match(r"^\s*([-*_])\s*(\1\s*){2,}$", line):
            out.append("<hr>")
            i += 1
            continue

        # Blockquote
        if line.startswith(">"):
            quote = []
            while i < n and lines[i].startswith(">"):
                quote.append(lines[i][1:].lstrip())
                i += 1
            out.append("<blockquote><p>%s</p></blockquote>" % inline(" ".join(quote).strip()))
            continue

        # Listas
        if re.match(r"^\s*[-*+]\s+", line) or re.match(r"^\s*\d+\.\s+", line):
            ordered = bool(re.match(r"^\s*\d+\.\s+", line))
            items = []
            while i < n and (
                re.match(r"^\s*[-*+]\s+", lines[i]) or re.match(r"^\s*\d+\.\s+", lines[i])
            ):
                item = re.sub(r"^\s*(?:[-*+]|\d+\.)\s+", "", lines[i])
                items.append(inline(item))
                i += 1
            tag = "ol" if ordered else "ul"
            out.append(
                "<%s>%s</%s>" % (tag, "".join("<li>%s</li>" % it for it in items), tag)
            )
            continue

        # Línea en blanco
        if line.strip() == "":
            i += 1
            continue

        # Párrafo (junta líneas hasta blanco / próximo bloque)
        para = [line]
        i += 1
        while i < n and lines[i].strip() != "" and not _starts_block(lines[i], lines, i):
            para.append(lines[i])
            i += 1
        out.append("<p>%s</p>" % inline(" ".join(para).strip()))

    # Footnotes al pie
    if footnotes:
        fn = '<div class="footnotes"><hr><ol>'
        for key, val in footnotes.items():
            fn += '<li id="fn-%s">%s</li>' % (key, inline(val))
        fn += "</ol></div>"
        out.append(fn)

    return "\n".join(out), headings


def _starts_block(line, lines, i):
    if line.startswith(("#", ">", "```", "|")):
        return True
    if re.match(r"^\s*[-*+]\s+", line) or re.match(r"^\s*\d+\.\s+", line):
        return True
    if re.match(r"^\s*([-*_])\s*(\1\s*){2,}$", line):
        return True
    return False


# ---------------------------------------------------------------------------
# GENERACIÓN DEL SITIO
# ---------------------------------------------------------------------------

def build_sidebar(active_slug, active_file):
    parts = ['<nav class="sidebar-nav">']
    for libro in SERIE:
        existe_algo = any(
            os.path.exists(os.path.join(SRC, libro["slug"], f + ".md"))
            for f, _ in libro["caps"]
        )
        open_attr = " open" if libro["slug"] == active_slug else ""
        parts.append('<details class="book-group"%s>' % open_attr)
        parts.append(
            '<summary style="--book-color:%s"><span class="book-emoji">%s</span>'
            '<span class="book-name">%s</span></summary>'
            % (libro["color"], libro["emoji"], libro["titulo"])
        )
        parts.append('<ul class="chap-list">')
        for f, titulo in libro["caps"]:
            path = os.path.join(SRC, libro["slug"], f + ".md")
            href = "../%s/%s.html" % (libro["slug"], f)
            if not os.path.exists(path):
                parts.append('<li class="chap pending">%s</li>' % titulo)
            else:
                cls = "chap active" if (libro["slug"] == active_slug and f == active_file) else "chap"
                parts.append('<li class="%s"><a href="%s">%s</a></li>' % (cls, href, titulo))
        parts.append("</ul></details>")
    parts.append("</nav>")
    return "\n".join(parts)


def flat_chapter_list():
    """Lista plana [(slug, file, titulo, libro)] solo de capítulos existentes, en orden."""
    flat = []
    for libro in SERIE:
        for f, titulo in libro["caps"]:
            if os.path.exists(os.path.join(SRC, libro["slug"], f + ".md")):
                flat.append((libro["slug"], f, titulo, libro))
    return flat


PAGE_TMPL = """<!DOCTYPE html>
<html lang="es" data-theme="light">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} — YDKJS en Español</title>
<link rel="stylesheet" href="../styles.css">
</head>
<body>
<header class="topbar">
  <button class="menu-btn" id="menuBtn" aria-label="Menú">☰</button>
  <a class="brand" href="../index.html"><span class="brand-logo">{{}}</span> You Don't Know JS <span class="brand-es">· Español</span></a>
  <div class="topbar-actions">
    <div class="progress-wrap" title="Progreso de lectura"><div class="progress-bar" id="progressBar"></div></div>
    <button class="theme-btn" id="themeBtn" aria-label="Cambiar tema">🌙</button>
  </div>
</header>
<div class="layout">
  <aside class="sidebar" id="sidebar">
    <div class="sidebar-head" style="--book-color:{book_color}">
      <span class="sidebar-emoji">{book_emoji}</span>
      <div><div class="sidebar-book">{book_title}</div><div class="sidebar-sub">{book_sub}</div></div>
    </div>
    {sidebar}
  </aside>
  <div class="scrim" id="scrim"></div>
  <main class="content">
    <div class="breadcrumb"><a href="../index.html">Inicio</a> <span>/</span> <a href="{book_home}">{book_title}</a> <span>/</span> {chap_title}</div>
    <article class="prose" style="--book-color:{book_color}">
      {content}
    </article>
    <nav class="pager">
      {prev}
      {next}
    </nav>
  </main>
  <aside class="toc" id="toc">
    <div class="toc-title">En esta página</div>
    {toc}
  </aside>
</div>
<button class="top-btn" id="topBtn" title="Volver arriba" aria-label="Volver arriba">↑</button>
<script src="../app.js"></script>
</body>
</html>"""


def render_toc(headings):
    if not headings:
        return '<p class="toc-empty">—</p>'
    out = ['<ul class="toc-list">']
    for level, text, sid in headings:
        out.append('<li class="toc-l%d"><a href="#%s">%s</a></li>' % (level, sid, text))
    out.append("</ul>")
    return "\n".join(out)


def build():
    if os.path.exists(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)

    # Assets
    write_asset("styles.css", STYLES)
    write_asset("app.js", APP_JS)

    flat = flat_chapter_list()
    index_of = {(s, f): idx for idx, (s, f, _, _) in enumerate(flat)}

    built = 0
    for libro in SERIE:
        out_dir = os.path.join(OUT, libro["slug"])
        src_dir = os.path.join(SRC, libro["slug"])
        # copiar imágenes del libro si existen
        img_dir = os.path.join(IMG_SRC_ROOT, libro["slug"], "images")
        if os.path.isdir(img_dir):
            shutil.copytree(img_dir, os.path.join(out_dir, "images"))
        for f, titulo in libro["caps"]:
            src = os.path.join(src_dir, f + ".md")
            if not os.path.exists(src):
                continue
            os.makedirs(out_dir, exist_ok=True)
            with open(src, encoding="utf-8") as fh:
                md = fh.read()
            content, headings = convert(md)

            idx = index_of[(libro["slug"], f)]
            prev_html = ""
            next_html = ""
            if idx > 0:
                ps, pf, pt, pl = flat[idx - 1]
                prev_html = (
                    '<a class="pager-btn prev" href="../%s/%s.html">'
                    '<span class="pager-dir">← Anterior</span>'
                    '<span class="pager-name">%s</span></a>' % (ps, pf, pt)
                )
            else:
                prev_html = '<span class="pager-btn disabled"></span>'
            if idx < len(flat) - 1:
                ns, nf, nt, nl = flat[idx + 1]
                next_html = (
                    '<a class="pager-btn next" href="../%s/%s.html">'
                    '<span class="pager-dir">Siguiente →</span>'
                    '<span class="pager-name">%s</span></a>' % (ns, nf, nt)
                )
            else:
                next_html = '<span class="pager-btn disabled"></span>'

            page = PAGE_TMPL.replace("{{}}", libro["emoji"]).format(
                title=titulo,
                book_color=libro["color"],
                book_emoji=libro["emoji"],
                book_title=libro["titulo"],
                book_sub=libro["subtitulo"],
                book_home="../%s/README.html" % libro["slug"],
                chap_title=titulo,
                sidebar=build_sidebar(libro["slug"], f),
                content=content,
                prev=prev_html,
                next=next_html,
                toc=render_toc(headings),
            )
            with open(os.path.join(out_dir, f + ".html"), "w", encoding="utf-8") as fh:
                fh.write(page)
            built += 1

    write_index(flat)
    print("✓ Sitio generado en %s — %d páginas de capítulo." % (OUT, built))


def write_asset(name, content):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as fh:
        fh.write(content)


def write_index(flat):
    cards = []
    for libro in SERIE:
        existentes = [
            (f, t) for f, t in libro["caps"]
            if os.path.exists(os.path.join(SRC, libro["slug"], f + ".md"))
        ]
        total = len([c for c in libro["caps"] if c[0] not in ("README", "toc", "foreword", "thanks")])
        hechos = len([f for f, _ in existentes if f not in ("README", "toc", "foreword", "thanks")])
        pct = int(hechos / total * 100) if total else 0
        if existentes:
            primero = existentes[0][0]
            href = "%s/%s.html" % (libro["slug"], primero)
            disabled = ""
        else:
            href = "#"
            disabled = " disabled"
        cards.append(
            '<a class="book-card%s" href="%s" style="--book-color:%s">'
            '<div class="book-card-emoji">%s</div>'
            '<div class="book-card-title">%s</div>'
            '<div class="book-card-sub">%s</div>'
            '<div class="book-card-prog"><div class="book-card-prog-bar" style="width:%d%%"></div></div>'
            '<div class="book-card-pct">%d%% traducido</div>'
            "</a>"
            % (disabled, href, libro["color"], libro["emoji"], libro["titulo"], libro["subtitulo"], pct, pct)
        )
    idx = INDEX_TMPL.format(cards="\n".join(cards))
    with open(os.path.join(OUT, "index.html"), "w", encoding="utf-8") as fh:
        fh.write(idx)


INDEX_TMPL = """<!DOCTYPE html>
<html lang="es" data-theme="light">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>You Don't Know JS Yet — Edición en Español</title>
<link rel="stylesheet" href="styles.css">
</head>
<body class="home">
<header class="topbar">
  <a class="brand" href="index.html"><span class="brand-logo">📖</span> You Don't Know JS <span class="brand-es">· Español</span></a>
  <button class="theme-btn" id="themeBtn" aria-label="Cambiar tema">🌙</button>
</header>
<section class="hero">
  <div class="hero-badge">Traducción al español · 2ª edición</div>
  <h1>You Don't Know <span class="hero-js">JS</span> Yet</h1>
  <p class="hero-lead">La serie completa de Kyle Simpson para dominar JavaScript desde sus cimientos. Traducida al español, con un lector colorido y pensado para estudiar.</p>
  <blockquote class="hero-quote">"No sabés JS, todavía. Yo tampoco, no del todo. Ninguno lo sabe. Pero todos podemos empezar a conocerlo mejor."</blockquote>
</section>
<main class="books-grid">
{cards}
</main>
<footer class="home-footer">
  <p>Contenido original © 2019-2025 Kyle Simpson · Licencia <a href="https://creativecommons.org/licenses/by-nc-nd/4.0/">CC BY-NC-ND 4.0</a>.</p>
  <p>Traducción al español con fines educativos.</p>
</footer>
<script src="app.js"></script>
</body>
</html>"""


# ---------------------------------------------------------------------------
# ASSETS (CSS / JS)  — inlined para mantener el proyecto autocontenido
# ---------------------------------------------------------------------------
STYLES = r"""/* YDKJS Español — diseño colorido y didáctico */
:root{
  --bg:#f7f8fc; --surface:#ffffff; --surface-2:#f1f3f9; --text:#1f2430;
  --text-soft:#5b6472; --border:#e4e8f0; --brand:#6366f1;
  --code-bg:#1e293b; --code-text:#e2e8f0; --shadow:0 1px 3px rgba(16,24,40,.08),0 8px 24px rgba(16,24,40,.06);
  --radius:14px; --book-color:#6366f1;
}
[data-theme="dark"]{
  --bg:#0f141c; --surface:#161d28; --surface-2:#1c2533; --text:#e6eaf2;
  --text-soft:#9aa6b8; --border:#27313f; --code-bg:#0b1120; --code-text:#e2e8f0;
  --shadow:0 1px 3px rgba(0,0,0,.4),0 8px 28px rgba(0,0,0,.35);
}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;background:var(--bg);color:var(--text);
  font-family:system-ui,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
  line-height:1.65;-webkit-font-smoothing:antialiased;transition:background .3s,color .3s}

/* Topbar */
.topbar{position:sticky;top:0;z-index:40;display:flex;align-items:center;gap:14px;
  padding:0 18px;height:58px;background:var(--surface);border-bottom:1px solid var(--border);
  box-shadow:0 1px 0 rgba(0,0,0,.02)}
.brand{display:flex;align-items:center;gap:9px;font-weight:800;color:var(--text);
  text-decoration:none;font-size:1.02rem;letter-spacing:-.01em}
.brand-logo{font-size:1.3rem}
.brand-es{color:var(--book-color,var(--brand));font-weight:700}
.topbar-actions{margin-left:auto;display:flex;align-items:center;gap:14px}
.menu-btn,.theme-btn{background:var(--surface-2);border:1px solid var(--border);color:var(--text);
  width:40px;height:40px;border-radius:10px;font-size:1.15rem;cursor:pointer;
  display:flex;align-items:center;justify-content:center;transition:transform .15s,background .2s}
.menu-btn{display:none}
.theme-btn:hover,.menu-btn:hover{transform:translateY(-1px);background:var(--border)}
.progress-wrap{width:120px;height:7px;background:var(--surface-2);border-radius:99px;overflow:hidden;border:1px solid var(--border)}
.progress-bar{height:100%;width:0;background:linear-gradient(90deg,#6366f1,#ec4899);transition:width .15s}

/* Layout */
.layout{display:grid;grid-template-columns:288px minmax(0,1fr) 230px;gap:0;
  max-width:1500px;margin:0 auto;align-items:start}
.sidebar{position:sticky;top:58px;height:calc(100vh - 58px);overflow-y:auto;
  background:var(--surface);border-right:1px solid var(--border);padding:18px 12px 60px}
.sidebar-head{display:flex;gap:12px;align-items:center;padding:12px 10px 16px;margin-bottom:8px;
  border-bottom:1px solid var(--border)}
.sidebar-emoji{font-size:1.9rem;filter:drop-shadow(0 2px 6px rgba(0,0,0,.15))}
.sidebar-book{font-weight:800;font-size:1.05rem;color:var(--book-color)}
.sidebar-sub{font-size:.8rem;color:var(--text-soft)}

.book-group{margin:2px 0;border-radius:10px}
.book-group>summary{list-style:none;cursor:pointer;display:flex;align-items:center;gap:9px;
  padding:9px 10px;border-radius:9px;font-weight:700;font-size:.9rem;color:var(--text);
  transition:background .15s;user-select:none}
.book-group>summary::-webkit-details-marker{display:none}
.book-group>summary:hover{background:var(--surface-2)}
.book-group>summary::before{content:"▸";color:var(--book-color);font-size:.8rem;transition:transform .2s}
.book-group[open]>summary::before{transform:rotate(90deg)}
.book-emoji{font-size:1.05rem}
.chap-list{list-style:none;margin:2px 0 10px;padding:0 0 0 14px}
.chap{margin:1px 0}
.chap a{display:block;padding:7px 11px;border-radius:8px;color:var(--text-soft);
  text-decoration:none;font-size:.86rem;border-left:2px solid transparent;transition:all .15s}
.chap a:hover{background:var(--surface-2);color:var(--text)}
.chap.active a{background:color-mix(in srgb,var(--book-color) 14%,transparent);
  color:var(--book-color);font-weight:700;border-left-color:var(--book-color)}
.chap.pending{padding:7px 11px;font-size:.84rem;color:var(--text-soft);opacity:.45;font-style:italic}
.chap.pending::after{content:" · pronto"}

/* Content */
.content{padding:30px 48px 90px;min-width:0}
.breadcrumb{font-size:.82rem;color:var(--text-soft);margin-bottom:22px}
.breadcrumb a{color:var(--book-color);text-decoration:none}
.breadcrumb a:hover{text-decoration:underline}
.breadcrumb span{margin:0 7px;opacity:.5}

.prose{max-width:780px}
.prose h1{font-size:2.1rem;line-height:1.2;letter-spacing:-.02em;margin:.2em 0 .6em;
  padding-bottom:.35em;border-bottom:3px solid var(--book-color);display:inline-block}
.prose h2{font-size:1.55rem;margin:1.9em 0 .5em;letter-spacing:-.01em;
  padding-left:14px;border-left:5px solid var(--book-color)}
.prose h3{font-size:1.22rem;margin:1.5em 0 .4em;color:var(--text)}
.prose h4{font-size:1.05rem;margin:1.3em 0 .3em;color:var(--text-soft);text-transform:uppercase;letter-spacing:.04em}
.prose p{margin:0 0 1.15em}
.prose a{color:var(--book-color);text-decoration:none;border-bottom:1px solid color-mix(in srgb,var(--book-color) 40%,transparent)}
.prose a:hover{border-bottom-width:2px}
.prose strong{font-weight:700;color:var(--text)}
.prose code{font-family:"SF Mono",ui-monospace,"Cascadia Code",Menlo,Consolas,monospace;
  font-size:.88em;background:color-mix(in srgb,var(--book-color) 12%,var(--surface-2));
  color:var(--book-color);padding:.12em .42em;border-radius:6px;border:1px solid color-mix(in srgb,var(--book-color) 18%,transparent)}
.prose img{max-width:100%;border-radius:12px;margin:1em 0;box-shadow:var(--shadow)}
.prose hr{border:none;border-top:1px solid var(--border);margin:2.4em 0}
.prose ul,.prose ol{margin:0 0 1.2em;padding-left:1.4em}
.prose li{margin:.35em 0}
.prose li::marker{color:var(--book-color)}

/* Code blocks */
.code-block{position:relative;margin:1.4em 0;border-radius:12px;overflow:hidden;
  box-shadow:var(--shadow);border:1px solid var(--border)}
.code-block::before{content:attr(data-lang);position:absolute;top:0;left:0;
  font-size:.68rem;font-weight:700;letter-spacing:.08em;text-transform:uppercase;
  color:#94a3b8;background:rgba(148,163,184,.12);padding:4px 12px;border-bottom-right-radius:8px}
.code-block pre{margin:0;background:var(--code-bg);color:var(--code-text);
  padding:38px 18px 18px;overflow-x:auto;font-size:.86rem;line-height:1.6}
.code-block code{font-family:"SF Mono",ui-monospace,"Cascadia Code",Menlo,Consolas,monospace;
  background:none;border:none;color:inherit;padding:0}
.copy-btn{position:absolute;top:6px;right:8px;z-index:2;background:rgba(148,163,184,.15);
  border:1px solid rgba(148,163,184,.25);color:#cbd5e1;font-size:.72rem;font-weight:600;
  padding:4px 10px;border-radius:7px;cursor:pointer;transition:all .15s}
.copy-btn:hover{background:rgba(148,163,184,.3);color:#fff}
.copy-btn.done{background:#10b981;color:#fff;border-color:#10b981}

/* Callouts */
.callout{margin:1.5em 0;border-radius:12px;overflow:hidden;border:1px solid var(--cl-border);
  background:var(--cl-bg);box-shadow:var(--shadow)}
.callout-head{display:flex;align-items:center;gap:9px;padding:10px 16px;font-weight:800;
  font-size:.76rem;letter-spacing:.09em;color:var(--cl-fg);background:var(--cl-head)}
.callout-ico{font-size:1.1rem}
.callout-body{padding:4px 18px}
.callout-body p{margin:.7em 0;color:var(--text)}
.callout-nota{--cl-bg:color-mix(in srgb,#3b82f6 7%,var(--surface));--cl-head:color-mix(in srgb,#3b82f6 16%,var(--surface));--cl-border:color-mix(in srgb,#3b82f6 30%,transparent);--cl-fg:#3b82f6}
.callout-tip{--cl-bg:color-mix(in srgb,#10b981 7%,var(--surface));--cl-head:color-mix(in srgb,#10b981 16%,var(--surface));--cl-border:color-mix(in srgb,#10b981 30%,transparent);--cl-fg:#059669}
.callout-warning{--cl-bg:color-mix(in srgb,#f59e0b 9%,var(--surface));--cl-head:color-mix(in srgb,#f59e0b 20%,var(--surface));--cl-border:color-mix(in srgb,#f59e0b 34%,transparent);--cl-fg:#d97706}
.callout-fun{--cl-bg:color-mix(in srgb,#ec4899 8%,var(--surface));--cl-head:color-mix(in srgb,#ec4899 17%,var(--surface));--cl-border:color-mix(in srgb,#ec4899 30%,transparent);--cl-fg:#db2777}

/* Blockquote */
blockquote{margin:1.5em 0;padding:4px 22px;border-left:4px solid var(--book-color);
  background:var(--surface-2);border-radius:0 10px 10px 0;font-style:italic;color:var(--text-soft)}

/* Tablas */
.table-wrap{overflow-x:auto;margin:1.4em 0;border-radius:12px;border:1px solid var(--border);box-shadow:var(--shadow)}
table{border-collapse:collapse;width:100%;font-size:.9rem}
th,td{padding:10px 14px;text-align:left;border-bottom:1px solid var(--border)}
th{background:var(--surface-2);font-weight:700;color:var(--book-color)}
tr:last-child td{border-bottom:none}

/* Footnotes */
.footnotes{margin-top:3em;font-size:.86rem;color:var(--text-soft)}
.footnotes ol{padding-left:1.3em}
.fnref a{color:var(--book-color);text-decoration:none;font-weight:700}

/* Pager */
.pager{display:flex;gap:16px;margin-top:3.5em;max-width:780px}
.pager-btn{flex:1;display:flex;flex-direction:column;gap:4px;padding:16px 20px;
  border:1px solid var(--border);border-radius:13px;background:var(--surface);
  text-decoration:none;transition:all .18s;box-shadow:var(--shadow)}
.pager-btn:not(.disabled):hover{transform:translateY(-2px);border-color:var(--book-color)}
.pager-btn.next{text-align:right}
.pager-btn.disabled{visibility:hidden}
.pager-dir{font-size:.76rem;font-weight:700;color:var(--book-color);text-transform:uppercase;letter-spacing:.05em}
.pager-name{font-weight:600;color:var(--text);font-size:.95rem}

/* TOC derecha */
.toc{position:sticky;top:58px;height:calc(100vh - 58px);overflow-y:auto;padding:30px 18px;font-size:.84rem}
.toc-title{font-weight:800;font-size:.72rem;letter-spacing:.1em;text-transform:uppercase;
  color:var(--text-soft);margin-bottom:12px}
.toc-list{list-style:none;margin:0;padding:0;border-left:2px solid var(--border)}
.toc-list a{display:block;padding:5px 0 5px 14px;margin-left:-2px;color:var(--text-soft);
  text-decoration:none;border-left:2px solid transparent;transition:all .15s;line-height:1.35}
.toc-list a:hover{color:var(--book-color)}
.toc-list a.active{color:var(--book-color);font-weight:700;border-left-color:var(--book-color)}
.toc-l3{padding-left:14px;font-size:.95em;opacity:.85}
.toc-empty{color:var(--text-soft);opacity:.5}

/* Botón volver arriba */
.top-btn{position:fixed;bottom:26px;right:26px;width:46px;height:46px;border-radius:50%;
  background:var(--book-color);color:#fff;border:none;font-size:1.3rem;cursor:pointer;
  box-shadow:0 6px 20px rgba(99,102,241,.4);opacity:0;pointer-events:none;transition:opacity .25s,transform .2s;z-index:30}
.top-btn.show{opacity:1;pointer-events:auto}
.top-btn:hover{transform:translateY(-3px)}

.scrim{display:none}

/* Home */
body.home{background:
  radial-gradient(1200px 500px at 50% -10%,color-mix(in srgb,#6366f1 14%,transparent),transparent),
  var(--bg)}
.hero{max-width:820px;margin:0 auto;padding:72px 24px 30px;text-align:center}
.hero-badge{display:inline-block;background:color-mix(in srgb,#6366f1 14%,transparent);
  color:#6366f1;font-weight:700;font-size:.82rem;padding:6px 16px;border-radius:99px;margin-bottom:22px}
.hero h1{font-size:3.4rem;line-height:1.05;letter-spacing:-.03em;margin:0 0 18px;font-weight:900}
.hero-js{background:linear-gradient(120deg,#6366f1,#ec4899);-webkit-background-clip:text;
  background-clip:text;color:transparent}
.hero-lead{font-size:1.18rem;color:var(--text-soft);max-width:640px;margin:0 auto 26px}
.hero-quote{font-style:italic;color:var(--text-soft);border-left:4px solid #6366f1;
  background:var(--surface);max-width:560px;margin:0 auto;padding:14px 22px;border-radius:0 12px 12px 0;box-shadow:var(--shadow)}
.books-grid{max-width:1040px;margin:30px auto;padding:0 24px;display:grid;
  grid-template-columns:repeat(auto-fill,minmax(290px,1fr));gap:22px}
.book-card{display:block;background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);
  padding:26px 24px;text-decoration:none;color:var(--text);box-shadow:var(--shadow);
  transition:transform .2s,box-shadow .2s,border-color .2s;position:relative;overflow:hidden}
.book-card::before{content:"";position:absolute;top:0;left:0;right:0;height:5px;background:var(--book-color)}
.book-card:not(.disabled):hover{transform:translateY(-5px);border-color:var(--book-color);
  box-shadow:0 14px 40px color-mix(in srgb,var(--book-color) 22%,transparent)}
.book-card.disabled{opacity:.5;cursor:not-allowed}
.book-card-emoji{font-size:2.6rem;margin-bottom:10px}
.book-card-title{font-size:1.3rem;font-weight:800;color:var(--book-color)}
.book-card-sub{color:var(--text-soft);font-size:.92rem;margin-bottom:18px}
.book-card-prog{height:8px;background:var(--surface-2);border-radius:99px;overflow:hidden;margin-bottom:7px}
.book-card-prog-bar{height:100%;background:var(--book-color);border-radius:99px;transition:width .4s}
.book-card-pct{font-size:.78rem;color:var(--text-soft);font-weight:600}
.home-footer{text-align:center;padding:50px 24px;color:var(--text-soft);font-size:.84rem}
.home-footer a{color:var(--book-color)}

/* Responsive */
@media(max-width:1200px){.layout{grid-template-columns:270px minmax(0,1fr)}.toc{display:none}}
@media(max-width:880px){
  .menu-btn{display:flex}
  .layout{grid-template-columns:1fr}
  .sidebar{position:fixed;top:58px;left:0;width:300px;z-index:35;transform:translateX(-105%);
    transition:transform .28s;box-shadow:0 10px 40px rgba(0,0,0,.25)}
  .sidebar.open{transform:translateX(0)}
  .scrim.show{display:block;position:fixed;inset:58px 0 0;background:rgba(0,0,0,.45);z-index:34}
  .content{padding:24px 20px 80px}
  .progress-wrap{display:none}
  .hero h1{font-size:2.4rem}
}
"""

APP_JS = r"""// YDKJS Español — interacción del lector
(function(){
  var root = document.documentElement;
  var saved = localStorage.getItem('ydkjs-theme');
  if(saved){ root.setAttribute('data-theme', saved); }
  function syncThemeIcon(){
    var dark = root.getAttribute('data-theme') === 'dark';
    document.querySelectorAll('#themeBtn').forEach(function(b){ b.textContent = dark ? '☀️' : '🌙'; });
  }
  syncThemeIcon();
  document.querySelectorAll('#themeBtn').forEach(function(btn){
    btn.addEventListener('click', function(){
      var dark = root.getAttribute('data-theme') === 'dark';
      var next = dark ? 'light' : 'dark';
      root.setAttribute('data-theme', next);
      localStorage.setItem('ydkjs-theme', next);
      syncThemeIcon();
    });
  });

  // Menú móvil
  var menuBtn = document.getElementById('menuBtn');
  var sidebar = document.getElementById('sidebar');
  var scrim = document.getElementById('scrim');
  function closeMenu(){ if(sidebar) sidebar.classList.remove('open'); if(scrim) scrim.classList.remove('show'); }
  if(menuBtn){ menuBtn.addEventListener('click', function(){
    sidebar.classList.toggle('open'); scrim.classList.toggle('show');
  });}
  if(scrim){ scrim.addEventListener('click', closeMenu); }

  // Botón copiar código
  document.querySelectorAll('.copy-btn').forEach(function(btn){
    btn.addEventListener('click', function(){
      var code = btn.parentElement.querySelector('code');
      navigator.clipboard.writeText(code.innerText).then(function(){
        btn.textContent = '¡Copiado!'; btn.classList.add('done');
        setTimeout(function(){ btn.textContent = 'Copiar'; btn.classList.remove('done'); }, 1600);
      });
    });
  });

  // Barra de progreso + botón arriba
  var progress = document.getElementById('progressBar');
  var topBtn = document.getElementById('topBtn');
  function onScroll(){
    var h = document.documentElement;
    var scrolled = h.scrollTop / (h.scrollHeight - h.clientHeight);
    if(progress) progress.style.width = (scrolled*100) + '%';
    if(topBtn){ if(h.scrollTop > 500) topBtn.classList.add('show'); else topBtn.classList.remove('show'); }
    highlightTOC();
  }
  window.addEventListener('scroll', onScroll, {passive:true});
  if(topBtn){ topBtn.addEventListener('click', function(){ window.scrollTo({top:0,behavior:'smooth'}); }); }

  // Resaltar sección activa en el TOC
  var tocLinks = Array.prototype.slice.call(document.querySelectorAll('.toc-list a'));
  var targets = tocLinks.map(function(a){ return document.getElementById(a.getAttribute('href').slice(1)); });
  function highlightTOC(){
    if(!tocLinks.length) return;
    var pos = window.scrollY + 120, idx = 0;
    for(var i=0;i<targets.length;i++){ if(targets[i] && targets[i].offsetTop <= pos) idx = i; }
    tocLinks.forEach(function(a,i){ a.classList.toggle('active', i===idx); });
  }
  onScroll();
})();
"""


if __name__ == "__main__":
    build()
