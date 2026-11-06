#!/usr/bin/env python3
"""Typeset an IB Diploma Programme-style examination paper (and optional markscheme) as PDF.

Usage:
    python3 render_ib_paper.py spec.json [output_dir]

Writes into output_dir (default: spec["meta"]["folder"], else the current directory):
    <file_stem> - Question Paper.pdf
    <file_stem> - Markscheme.pdf            (only if the spec has a "markscheme" section)

Dependencies: reportlab (required); Pillow (only for PNG images); matplotlib (only for
"equation" blocks). See references/spec_format.md for the full spec.

Inline markup allowed in every text field:
    `code`  monospace          <b> <i> <u> <sup> <sub> <br/>
    $...$   light maths: single letters italic, \\times ×, \\div ÷, \\pm ±, \\le ≤, \\ge ≥, \\ne ≠,
            \\approx ≈, \\infty ∞, \\pi π, \\theta θ, \\alpha α, \\beta β, \\Delta Δ, \\mu μ, \\lambda λ,
            \\sigma σ, \\degree °, \\sqrt √, \\cdot ·, - → −, x^2 / x^{10} superscript, x_1 / x_{n} subscript
Any other '<', '>' or '&' is escaped automatically.
"""
import json
import os
import re
import sys
import tempfile

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib.fonts import addMapping
from reportlab.lib.pagesizes import A4, LETTER
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas as rl_canvas
from reportlab.platypus import (Flowable, Image, KeepTogether, PageBreak, Paragraph,
                                SimpleDocTemplate, Spacer, Table, TableStyle, XPreformatted)
from reportlab.platypus.doctemplate import Indenter

WARNINGS = []


def warn(msg):
    WARNINGS.append(msg)


# ------------------------------------------------------------------ fonts
SANS_CANDIDATES = [
    ["/System/Library/Fonts/Supplemental/Arial%s.ttf" % s for s in ("", " Bold", " Italic", " Bold Italic")],
    ["C:/Windows/Fonts/%s.ttf" % s for s in ("arial", "arialbd", "ariali", "arialbi")],
    ["/usr/share/fonts/truetype/msttcorefonts/Arial%s.ttf" % s for s in ("", "_Bold", "_Italic", "_Bold_Italic")],
    ["/usr/share/fonts/truetype/liberation/LiberationSans-%s.ttf" % s for s in ("Regular", "Bold", "Italic", "BoldItalic")],
    ["/usr/share/fonts/truetype/liberation2/LiberationSans-%s.ttf" % s for s in ("Regular", "Bold", "Italic", "BoldItalic")],
    ["/usr/share/fonts/truetype/dejavu/DejaVuSans%s.ttf" % s for s in ("", "-Bold", "-Oblique", "-BoldOblique")],
]
MONO_CANDIDATES = [
    ["/System/Library/Fonts/Supplemental/Courier New%s.ttf" % s for s in ("", " Bold", " Italic", " Bold Italic")],
    ["C:/Windows/Fonts/%s.ttf" % s for s in ("cour", "courbd", "couri", "courbi")],
    ["/usr/share/fonts/truetype/liberation/LiberationMono-%s.ttf" % s for s in ("Regular", "Bold", "Italic", "BoldItalic")],
    ["/usr/share/fonts/truetype/liberation2/LiberationMono-%s.ttf" % s for s in ("Regular", "Bold", "Italic", "BoldItalic")],
    ["/usr/share/fonts/truetype/dejavu/DejaVuSansMono%s.ttf" % s for s in ("", "-Bold", "-Oblique", "-BoldOblique")],
]


def _register(name, paths):
    if not all(os.path.exists(p) for p in paths):
        return False
    try:
        for suffix, p in zip(("", "-Bold", "-Italic", "-BoldItalic"), paths):
            pdfmetrics.registerFont(TTFont(name + suffix, p))
    except Exception:
        return False
    for b, i, suf in ((0, 0, ""), (1, 0, "-Bold"), (0, 1, "-Italic"), (1, 1, "-BoldItalic")):
        addMapping(name, b, i, name + suf)
    return True


def _setup_fonts():
    sans = "IBSans" if any(_register("IBSans", c) for c in SANS_CANDIDATES) else None
    mono = "IBMono" if any(_register("IBMono", c) for c in MONO_CANDIDATES) else None
    return sans or "Helvetica", mono or "Courier", sans is not None


SANS, MONO, UNICODE_OK = _setup_fonts()
SANS_BOLD = SANS + "-Bold" if UNICODE_OK else "Helvetica-Bold"
ASCII_FALLBACK = {"−": "-", "≤": "<=", "≥": ">=", "≈": "~", "≠": "!=", "–": "-", "—": "-", "…": "...",
                  "∞": "inf", "π": "pi", "θ": "theta", "α": "alpha", "β": "beta", "Δ": "Delta", "μ": "u",
                  "λ": "lambda", "σ": "sigma", "√": "sqrt", "“": '"', "”": '"', "‘": "'", "’": "'"}

# ------------------------------------------------------------------ inline markup
MATH_WORDS = [(r"\times", "×"), (r"\div", "÷"), (r"\pm", "±"), (r"\le", "≤"), (r"\ge", "≥"), (r"\ne", "≠"),
              (r"\approx", "≈"), (r"\infty", "∞"), (r"\pi", "π"), (r"\theta", "θ"), (r"\alpha", "α"),
              (r"\beta", "β"), (r"\Delta", "Δ"), (r"\mu", "μ"), (r"\lambda", "λ"), (r"\sigma", "σ"),
              (r"\degree", "°"), (r"\sqrt", "√"), (r"\cdot", "·"), (r"\log", "log"), (r"\ln", "ln"),
              (r"\sin", "sin"), (r"\cos", "cos"), (r"\tan", "tan"), (r"\min", "min"), (r"\max", "max"),
              (r"\,", " "), (r"\;", " ")]


def _maths(m):
    t = m.group(1).replace(r"\left", "").replace(r"\right", "")
    t = re.sub(r"\\frac\{([^{}]*)\}\{([^{}]*)\}", lambda mm: "%s/%s" % (
        mm.group(1) if len(mm.group(1)) < 2 or mm.group(1).isalnum() else "(%s)" % mm.group(1),
        mm.group(2) if len(mm.group(2)) < 2 or mm.group(2).isalnum() else "(%s)" % mm.group(2)), t)
    for a, b in sorted(MATH_WORDS, key=lambda x: -len(x[0])):
        t = t.replace(a, b)
    t = re.sub(r"√\{([^{}]*)\}", r"√\1", t)
    t = t.replace("-", "−")
    t = re.sub(r"(?<![A-Za-z])([A-NP-Za-z])(?![A-Za-z])", lambda mm: "\x01i\x02" + mm.group(1) + "\x01/i\x02", t)
    t = re.sub(r"\^\{([^}]+)\}|\^(\S)", lambda mm: "\x01sup\x02" + (mm.group(1) or mm.group(2)) + "\x01/sup\x02", t)
    t = re.sub(r"_\{([^}]+)\}|_(\S)", lambda mm: "\x01sub\x02" + (mm.group(1) or mm.group(2)) + "\x01/sub\x02", t)
    return t.replace(" ", "\u00a0")


def md(text, mono_size=None):
    if text is None:
        return ""
    codes = []

    def keep(m):
        codes.append(m.group(1))
        return "\x03%d\x03" % (len(codes) - 1)

    s = re.sub(r"`([^`]*)`", keep, str(text))
    s = re.sub(r"\$([^$]+)\$", _maths, s)
    for tag in ("b", "/b", "i", "/i", "u", "/u", "sup", "/sup", "sub", "/sub", "br/", "br /"):
        s = s.replace("<%s>" % tag, "\x01%s\x02" % tag)
    s = s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    s = s.replace("\x01", "<").replace("\x02", ">")
    s = s.replace("<sup>", "<super>").replace("</sup>", "</super>")

    def put(m):
        c = codes[int(m.group(1))].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace(" ", "\u00a0")
        size = ' size="%s"' % mono_size if mono_size else ""
        return '<font face="%s"%s>%s</font>' % (MONO, size, c)

    s = re.sub("\x03(\\d+)\x03", put, s)
    if not UNICODE_OK:
        for a, b in ASCII_FALLBACK.items():
            s = s.replace(a, b)
    return s


# ------------------------------------------------------------------ styles / geometry
BODY = ParagraphStyle("body", fontName=SANS, fontSize=11, leading=14.5, spaceAfter=6, alignment=TA_LEFT)
SMALL = ParagraphStyle("small", parent=BODY, fontSize=9.6, leading=12.5, spaceAfter=2)
CENTER = ParagraphStyle("center", parent=BODY, alignment=TA_CENTER)
RIGHT = ParagraphStyle("right", parent=BODY, alignment=TA_RIGHT, spaceAfter=0)
CODE = ParagraphStyle("code", fontName=MONO, fontSize=9.2, leading=11.2)
TITLE = ParagraphStyle("title", parent=BODY, fontName=SANS_BOLD, fontSize=17, leading=22, spaceAfter=4)
SUBTITLE = ParagraphStyle("subtitle", parent=BODY, fontSize=13, leading=17, spaceAfter=3)
SOURCE = ParagraphStyle("source", parent=BODY, fontSize=8.5, leading=10.5, alignment=TA_RIGHT,
                        textColor=colors.Color(0.25, 0.25, 0.25))

PAGE_W, PAGE_H = A4
MARGIN_L = MARGIN_R = 2.4 * cm
MARGIN_T, MARGIN_B = 2.3 * cm, 2.4 * cm
FRAME_PAD = 6  # reportlab frames pad 6pt on each side
FRAME_W = PAGE_W - MARGIN_L - MARGIN_R - 2 * FRAME_PAD
Q_INDENT = 0.95 * cm
MARK_W = 1.5 * cm
L1, L2 = 0.95 * cm, 1.0 * cm
SPEC_DIR = "."
TMP_DIR = tempfile.mkdtemp(prefix="ibpaper_")

KEYWORDS = {
    "java": set("""abstract boolean break byte case catch char class continue default do double else enum extends
final finally float for if implements import instanceof int interface long new null package private protected
public return short static super switch this throw throws true false try void while var String""".split()),
    "python": set("""and as assert break class continue def del elif else except False finally for from global if
import in is lambda None nonlocal not or pass raise return True try while with yield self print len range""".split()),
    "pseudocode": set("""if then else end loop while until for from to output input return and or not mod div""".split()),
    "sql": set("""SELECT FROM WHERE JOIN ON GROUP BY ORDER HAVING INSERT INTO VALUES UPDATE SET DELETE CREATE
TABLE PRIMARY KEY FOREIGN REFERENCES AND OR NOT NULL IS AS DISTINCT COUNT SUM AVG MIN MAX LIKE IN""".split()),
}
COMMENT_MARK = {"java": "//", "python": "#", "pseudocode": "//", "sql": "--"}


def esc(x):
    return x.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def highlight(line, lang):
    lang = (lang or "").lower()
    kw = KEYWORDS.get(lang)
    if kw is None:
        return esc(line)
    cmark = COMMENT_MARK.get(lang, "//")
    code_part, comment, in_str = line, "", None
    for j, ch in enumerate(line):
        if in_str:
            if ch == in_str and line[j - 1] != "\\":
                in_str = None
        elif ch in "\"'":
            in_str = ch
        elif line.startswith(cmark, j):
            code_part, comment = line[:j], line[j:]
            break
    out = []
    for tok in re.split(r"(\"[^\"]*\"|'[^']*'|\b[A-Za-z_]\w*\b)", code_part):
        if tok:
            out.append("<b>%s</b>" % esc(tok) if tok in kw else esc(tok))
    if comment:
        out.append("<i>%s</i>" % esc(comment))
    return "".join(out) or " "


# ------------------------------------------------------------------ flowables
class DottedLines(Flowable):
    """IB question-answer booklet style dotted answer lines."""

    def __init__(self, n, width, gap=0.85 * cm):
        super().__init__()
        self.n, self.width, self.gap = n, width, gap

    def wrap(self, aw, ah):
        self.width = min(self.width, aw)
        return self.width, self.n * self.gap + 4

    def draw(self):
        c = self.canv
        c.setDash(1, 2.2)
        c.setLineWidth(0.6)
        c.setStrokeColor(colors.Color(0.35, 0.35, 0.35))
        for k in range(self.n):
            y = self.n * self.gap - (k + 1) * self.gap + 4
            c.line(0, y, self.width, y)
        c.setDash()


class BreakUnlessTop(Flowable):
    """Starts a new page unless the current page is still (almost) empty."""

    def wrap(self, aw, ah):
        full = PAGE_H - MARGIN_T - MARGIN_B - 2 * FRAME_PAD
        return (0, 0) if ah > full - 24 else (aw, ah)

    def draw(self):
        pass


class BottomNote(Flowable):
    """Fills the rest of the frame and prints a centred note at its bottom."""

    def __init__(self, text):
        super().__init__()
        self.text = text

    def wrap(self, aw, ah):
        self.aw, self.ah = aw, ah
        return aw, max(ah - 1, 0)

    def draw(self):
        p = Paragraph(md(self.text), CENTER)
        p.wrap(self.aw, self.ah)
        p.drawOn(self.canv, 0, 2)


def mark_label(m):
    """Numbers are shown as [n]; strings (e.g. "M1A1", "(A1)", "[1 max]") are shown as written."""
    if m in (None, ""):
        return ""
    return "[%s]" % fmt_num(float(m)) if numeric(m) is not None else str(m)


def mark_cell(m, bold=False):
    lab = mark_label(m)
    if not lab:
        return ""
    return Paragraph("<b>%s</b>" % esc(lab) if bold else esc(lab), RIGHT)


def paras(text, style=BODY):
    return [Paragraph(md(p), style) for p in str(text).split("\n\n")]


def numeric(m):
    try:
        return float(m)
    except (TypeError, ValueError):
        return None


def fmt_num(x):
    return str(int(x)) if x == int(x) else str(x)


# ------------------------------------------------------------------ blocks
def code_block(code, lang, width):
    lines = code.rstrip("\n").split("\n")
    rows = [[XPreformatted(highlight(l, lang), CODE) if l.strip() else Spacer(1, CODE.leading)] for l in lines]
    t = Table(rows, colWidths=[width], hAlign="LEFT")
    t.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 0.6, colors.Color(0.45, 0.45, 0.45)),
        ("LEFTPADDING", (0, 0), (-1, -1), 7), ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 0), ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, 0), 5), ("BOTTOMPADDING", (0, -1), (-1, -1), 5)]))
    return [Spacer(1, 3), t, Spacer(1, 7)]


def caption_para(text):
    return Paragraph(md(text), ParagraphStyle("cap", parent=CENTER, spaceAfter=4))


def grid_table(b, width):
    col_headers = b.get("col_headers", [])
    rows = b["rows"]
    row_title, col_title = b.get("row_title", ""), b.get("col_title", "")
    has_labels = b.get("row_labels", True)
    data = []
    if col_title:
        data.append([""] + [Paragraph("<i>%s</i>" % md(col_title), CENTER)] + [""] * (max(len(col_headers), 1) - 1))
    if col_headers:
        data.append([""] + [Paragraph("<b>%s</b>" % md(h), CENTER) for h in col_headers])
    first = len(data)
    bold = set(tuple(x) for x in b.get("bold_cells", []))
    for ri, r in enumerate(rows):
        cells = r[1:] if has_labels else r
        lab = r[0] if has_labels else ""
        lab_txt = ("<i>%s</i> " % md(row_title) if (ri == 0 and row_title) else "") + ("<b>%s</b>" % md(lab) if lab != "" else "")
        row = [Paragraph(lab_txt, RIGHT)]
        for ci, v in enumerate(cells):
            txt = md(v)
            row.append(Paragraph("<b>%s</b>" % txt if (ri, ci) in bold else txt, CENTER))
        data.append(row)
    ncols = len(data[-1])
    cw = b.get("cell_width_cm", 0.95) * cm
    lw = b.get("label_width_cm", (1.6 if row_title else 0.9) if has_labels else 0.1) * cm
    t = Table(data, colWidths=[lw] + [cw] * (ncols - 1), hAlign="CENTER")
    st = [("GRID", (1, first), (-1, -1), 0.6, colors.black), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
          ("TOPPADDING", (0, 0), (-1, -1), 2), ("BOTTOMPADDING", (0, 0), (-1, -1), 4)]
    if col_title:
        st.append(("SPAN", (1, 0), (-1, 0)))
    t.setStyle(TableStyle(st))
    out = [caption_para(b["caption"])] if b.get("caption") else []
    out.append(t)
    if b.get("source"):
        out.append(Paragraph(md(b["source"]), SOURCE))
    return [KeepTogether(out), Spacer(1, 8)]


def simple_table(b, width):
    fs = ParagraphStyle("t", parent=BODY, fontSize=b.get("font_size", 9.8), leading=b.get("font_size", 9.8) * 1.25, spaceAfter=0)
    align = {"left": TA_LEFT, "center": TA_CENTER, "right": TA_RIGHT}
    col_align = b.get("align")
    data = []
    if b.get("header"):
        data.append([Paragraph("<b>%s</b>" % md(h), fs) for h in b["header"]])
    for r in b["rows"]:
        row = []
        for ci, c in enumerate(r):
            st = fs
            if col_align and ci < len(col_align):
                st = ParagraphStyle("ta%d" % ci, parent=fs, alignment=align[col_align[ci]])
            row.append(Paragraph(md(c), st))
        data.append(row)
    fr = b.get("col_fractions")
    t = Table(data, colWidths=[width * f for f in fr] if fr else None, hAlign="CENTER",
              repeatRows=1 if b.get("header") else 0)
    st = [("GRID", (0, 0), (-1, -1), 0.5, colors.Color(0.4, 0.4, 0.4)), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
          ("TOPPADDING", (0, 0), (-1, -1), 2), ("BOTTOMPADDING", (0, 0), (-1, -1), 3)]
    if b.get("header") and b.get("shade_header", False):
        st.append(("BACKGROUND", (0, 0), (-1, 0), colors.Color(0.9, 0.9, 0.9)))
    t.setStyle(TableStyle(st))
    out = [caption_para(b["caption"])] if b.get("caption") else []
    out.append(t)
    if b.get("source"):
        out.append(Paragraph(md(b["source"]), SOURCE))
    return ([KeepTogether(out)] if len(b["rows"]) < 25 else out) + [Spacer(1, 8)]


def image_block(b, width):
    path = b["path"]
    if not os.path.isabs(path):
        path = os.path.join(SPEC_DIR, path)
    if not os.path.exists(path):
        warn("image not found: %s" % path)
        return [Paragraph("<i>[missing image: %s]</i>" % esc(b["path"]), CENTER)]
    iw, ih = ImageReader(path).getSize()
    w = min(b.get("width_cm", 10) * cm, width)
    h = w * ih / iw
    img = Image(path, width=w, height=h)
    img.hAlign = b.get("align", "CENTER").upper()
    out = [caption_para(b["caption"])] if b.get("caption") else []
    out.append(img)
    if b.get("source"):
        out.append(Paragraph(md(b["source"]), SOURCE))
    return [KeepTogether(out), Spacer(1, 8)]


_eq_count = [0]


def equation_block(b, width):
    latex = b["latex"]
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        from matplotlib import rcParams
        rcParams["mathtext.fontset"] = b.get("fontset", "dejavusans")
        _eq_count[0] += 1
        path = os.path.join(TMP_DIR, "eq%d.png" % _eq_count[0])
        fig = plt.figure(figsize=(0.01, 0.01))
        fig.text(0, 0, "$%s$" % latex, fontsize=b.get("size", 13))
        fig.savefig(path, dpi=300, bbox_inches="tight", pad_inches=0.04, transparent=True)
        plt.close(fig)
        iw, ih = ImageReader(path).getSize()
        w, h = iw * 72.0 / 300, ih * 72.0 / 300
        if w > width:
            w, h = width, h * width / w
        img = Image(path, width=w, height=h)
        img.hAlign = b.get("align", "CENTER").upper()
        return [Spacer(1, 2), img, Spacer(1, 6)]
    except Exception as e:  # matplotlib missing or bad LaTeX
        warn("equation rendered as text (%s): %s" % (type(e).__name__, latex))
        return [Paragraph("<i>%s</i>" % esc(latex), CENTER)]


def render_parts(b, width, lang):
    out = []
    for part in b["parts"]:
        lab = "(%s)" % part["label"]
        subs = part.get("subparts")
        items = subs if subs else [part]
        for k, sp in enumerate(items):
            text_w = width - L1 - (L2 if subs else 0) - MARK_W
            cell = paras(sp.get("text", "")) if sp.get("text") else []
            if sp.get("code"):
                cell += code_block(sp["code"], sp.get("lang", lang), text_w - 6)
            if sp.get("blocks"):
                cell += render_blocks(sp["blocks"], text_w, lang)
            if subs:
                row = [Paragraph(lab if k == 0 else "", BODY), Paragraph("(%s)" % sp["label"], BODY), cell, mark_cell(sp.get("marks"))]
                cws = [L1, L2, text_w, MARK_W]
            else:
                row = [Paragraph(lab, BODY), cell, mark_cell(sp.get("marks"))]
                cws = [L1, text_w, MARK_W]
            t = Table([row], colWidths=cws)
            t.setStyle(TableStyle([("VALIGN", (0, 0), (-2, 0), "TOP"), ("VALIGN", (-1, 0), (-1, 0), "BOTTOM"),
                                   ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                                   ("TOPPADDING", (0, 0), (-1, -1), 0), ("BOTTOMPADDING", (0, 0), (-1, -1), 2)]))
            out.append(t)
            indent = L1 + (L2 if subs else 0)
            if sp.get("lines"):
                out += [Indenter(left=indent), Spacer(1, 2), DottedLines(int(sp["lines"]), width - indent), Indenter(left=-indent)]
            if sp.get("space_cm"):
                out.append(Spacer(1, sp["space_cm"] * cm))
            out.append(Spacer(1, 5))
    return out


def render_blocks(blocks, width, lang, qnum=None):
    story, first_text = [], True
    for b in blocks:
        t = b["type"]
        if t == "text":
            style = BODY
            if b.get("align") == "center":
                style = CENTER
            for p in str(b["text"]).split("\n\n"):
                if first_text and qnum is not None:
                    st = ParagraphStyle("qf", parent=style, bulletIndent=-Q_INDENT, bulletFontName=SANS_BOLD)
                    story.append(Paragraph(md(p), st, bulletText="%s." % qnum))
                else:
                    story.append(Paragraph(md(p), style))
                first_text = False
        elif t == "code":
            story += code_block(b["code"], b.get("lang", lang), width - 6)
        elif t == "grid":
            story += grid_table(b, width)
        elif t == "table":
            story += simple_table(b, width)
        elif t == "image":
            story += image_block(b, width)
        elif t == "equation":
            story += equation_block(b, width)
        elif t == "box":
            tb = Table([[paras(b["text"], ParagraphStyle("bx", parent=BODY, spaceAfter=2))]], colWidths=[width])
            tb.setStyle(TableStyle([("BOX", (0, 0), (-1, -1), 0.7, colors.black), ("LEFTPADDING", (0, 0), (-1, -1), 6),
                                    ("RIGHTPADDING", (0, 0), (-1, -1), 6), ("TOPPADDING", (0, 0), (-1, -1), 4),
                                    ("BOTTOMPADDING", (0, 0), (-1, -1), 4)]))
            story += [tb, Spacer(1, 8)]
        elif t == "bullets":
            st = ParagraphStyle("bul", parent=BODY, leftIndent=14, bulletIndent=3, spaceAfter=3)
            for k, it in enumerate(b["items"]):
                bullet = "%d." % (k + 1) if b.get("numbered") else "•"
                story.append(Paragraph(md(it), st, bulletText=bullet))
            story.append(Spacer(1, 3))
        elif t == "parts":
            story += render_parts(b, width, lang)
        elif t == "lines":
            story += [DottedLines(int(b.get("count", 4)), width), Spacer(1, 6)]
        elif t == "spacer":
            story.append(Spacer(1, b.get("height_cm", 0.4) * cm))
        elif t == "source":
            story.append(Paragraph(md(b["text"]), SOURCE))
        elif t == "pagebreak":
            story.append(("PAGEBREAK", None))
        else:
            raise ValueError("unknown block type: %s" % t)
    return story


# ------------------------------------------------------------------ marks bookkeeping
def part_marks(blocks):
    total, has = 0.0, False
    for b in blocks:
        if b["type"] != "parts":
            continue
        for p in b["parts"]:
            for sp in (p.get("subparts") or [p]):
                v = numeric(sp.get("marks"))
                if v is not None:
                    total += v
                    has = True
    return total if has else None


# ------------------------------------------------------------------ page decoration
class NumberedCanvas(rl_canvas.Canvas):
    footer_mode = "turnover"
    footer_text = ""
    header_left = ""
    header_right = ""

    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        self._saved = []

    def showPage(self):
        self._saved.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        n = len(self._saved)
        for st in self._saved:
            self.__dict__.update(st)
            self._decorate(n)
            super().showPage()
        super().save()

    def _decorate(self, total):
        p = self._pageNumber
        if p == 1:
            return
        self.setFont(SANS, 10.5)
        self.drawCentredString(PAGE_W / 2, PAGE_H - 1.35 * cm, ("– %d –" if UNICODE_OK else "- %d -") % p)
        self.setFont(SANS, 8.5)
        if self.header_left:
            self.drawString(MARGIN_L + FRAME_PAD, PAGE_H - 1.35 * cm, self.header_left)
        if self.header_right:
            self.drawRightString(PAGE_W - MARGIN_R - FRAME_PAD, PAGE_H - 1.35 * cm, self.header_right)
        if self.footer_mode == "turnover" and p < total:
            self.setFont(SANS_BOLD, 10.5)
            self.drawRightString(PAGE_W - MARGIN_R - FRAME_PAD, 1.3 * cm, "Turn over")
        elif self.footer_mode == "text" and self.footer_text:
            self.setFont(SANS, 9)
            self.drawCentredString(PAGE_W / 2, 1.3 * cm, self.footer_text)


def hrule(width, thickness=0.6):
    t = Table([[""]], colWidths=[width], rowHeights=[2])
    t.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, -1), thickness, colors.Color(0.35, 0.35, 0.35))]))
    return t


def cover(meta, extra_title=None):
    s = [Spacer(1, 1.2 * cm)]
    if extra_title:
        s += [Paragraph(extra_title, TITLE), Spacer(1, 4)]
    s.append(Paragraph(md(meta.get("subject", "Subject")), TITLE))
    for key in ("level", "paper", "title"):
        if meta.get(key):
            s.append(Paragraph(md(meta[key]), SUBTITLE))
    return s


def make_doc(path, title):
    return SimpleDocTemplate(path, pagesize=PAGE_SIZE, leftMargin=MARGIN_L, rightMargin=MARGIN_R,
                             topMargin=MARGIN_T, bottomMargin=MARGIN_B, title=title)


def canvas_class(mode, meta, footer_text=""):
    class C(NumberedCanvas):
        pass
    C.footer_mode = mode
    C.footer_text = footer_text
    C.header_left = meta.get("header_left", "")
    C.header_right = meta.get("header_right", "")
    return C


# ------------------------------------------------------------------ question paper
def build_question_paper(spec, path):
    meta = spec["meta"]
    lang = meta.get("code_language", "")
    items = spec["paper"]
    q_totals = {}
    for it in items:
        if it.get("type") == "question":
            computed = part_marks(it["blocks"])
            q_totals[str(it["number"])] = it.get("max_mark", computed)
            if it.get("max_mark") is not None and computed is not None and numeric(it["max_mark"]) != computed:
                warn("question %s: max_mark %s but parts add up to %s" % (it["number"], it["max_mark"], fmt_num(computed)))
    computed_total = sum(numeric(v) or 0 for v in q_totals.values())
    total = meta.get("total_marks", fmt_num(computed_total) if computed_total else None)
    if meta.get("total_marks") is not None and computed_total and numeric(meta["total_marks"]) != computed_total:
        warn("meta.total_marks is %s but questions add up to %s" % (meta["total_marks"], fmt_num(computed_total)))

    story = cover(meta)
    story += [Spacer(1, 10), hrule(FRAME_W), Spacer(1, 14)]
    for key, label in (("duration", "Duration"), ("suggested_time", "Suggested time")):
        if meta.get(key):
            story += [Paragraph("<b>%s: %s</b>" % (label, md(meta[key])), BODY), Spacer(1, 4)]
    story.append(Paragraph("<b>Instructions to candidates</b>", BODY))
    st = ParagraphStyle("ins", parent=BODY, leftIndent=14, bulletIndent=3, spaceAfter=4)
    default_ins = ["Do not open this examination paper until instructed to do so.", "Answer all questions."]
    if total:
        default_ins.append("The maximum mark for this examination paper is <b>[%s marks]</b>." % total)
    for it in meta.get("instructions", default_ins):
        story.append(Paragraph(md(it), st, bulletText="•"))
    for b in meta.get("cover_blocks", []):
        story += render_blocks([b], FRAME_W, lang)
    if meta.get("cover_note"):
        story += [Spacer(1, 14), Paragraph(md(meta["cover_note"]), BODY)]
    story.append(PageBreak())
    if meta.get("lead_line"):
        story += [Paragraph("<b>%s</b>" % md(meta["lead_line"]), BODY), Spacer(1, 4)]

    for it in items:
        kind = it.get("type")
        if kind == "section":
            if it.get("new_page"):
                story.append(BreakUnlessTop())
            story.append(Paragraph("<b>%s</b>" % md(it["title"]), ParagraphStyle("sec", parent=BODY, fontSize=13, leading=17, spaceBefore=6)))
            if it.get("text"):
                story += paras(it["text"])
            story.append(Spacer(1, 4))
        elif kind == "question":
            qn = it["number"]
            if it.get("new_page"):
                story.append(BreakUnlessTop())
            show_max = it.get("show_max_mark", meta.get("show_max_mark", False))
            head = []
            if show_max and q_totals.get(str(qn)) is not None:
                head.append(Paragraph("[Maximum mark: %s]" % fmt_num(numeric(q_totals[str(qn)]) or 0)
                                      if numeric(q_totals[str(qn)]) is not None else "[Maximum mark: %s]" % q_totals[str(qn)], RIGHT))
                head.append(Spacer(1, 4))
            story += head
            story.append(Indenter(left=Q_INDENT))
            for f in render_blocks(it["blocks"], FRAME_W - Q_INDENT, lang, qn):
                if isinstance(f, tuple):
                    story += [BottomNote("(Question %s continues on the following page)" % qn), PageBreak(),
                              Indenter(left=-Q_INDENT), Paragraph("(Question %s continued)" % qn, BODY),
                              Indenter(left=Q_INDENT), Spacer(1, 4)]
                else:
                    story.append(f)
            story += [Indenter(left=-Q_INDENT), Spacer(1, 10)]
        elif kind == "pagebreak":
            story.append(PageBreak())
        else:
            story += [f for f in render_blocks([it], FRAME_W, lang) if not isinstance(f, tuple)]
    if meta.get("end_text"):
        story += [Spacer(1, 6), Paragraph("<b>%s</b>" % md(meta["end_text"]), CENTER)]
    doc = make_doc(path, "%s — %s" % (meta.get("subject", ""), meta.get("title", meta.get("paper", ""))))
    doc.build(story, canvasmaker=canvas_class("turnover", meta))


# ------------------------------------------------------------------ markscheme
def ms_blocks(blocks, lang):
    W, out = FRAME_W, []
    for blk in blocks:
        kind = blk["type"]
        if kind == "points":
            bullet = blk.get("bullet", "–" if UNICODE_OK else "-")
            bw = 0.6 * cm if bullet else 0.0
            for pt in blk["items"]:
                pt = {"text": pt} if isinstance(pt, str) else pt
                cell = paras(pt["text"], ParagraphStyle("pt", parent=BODY, spaceAfter=0))
                row = ([Paragraph(bullet, BODY)] if bullet else []) + [cell, mark_cell(pt.get("marks"))]
                t = Table([row], colWidths=([bw] if bullet else []) + [W - bw - MARK_W, MARK_W])
                t.setStyle(TableStyle([("VALIGN", (0, 0), (-2, 0), "TOP"), ("VALIGN", (-1, 0), (-1, 0), "BOTTOM"),
                                       ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                                       ("TOPPADDING", (0, 0), (-1, -1), 1), ("BOTTOMPADDING", (0, 0), (-1, -1), 4)]))
                out.append(t)
        elif kind == "notes":
            out.append(Paragraph("<i>%s</i>" % md(blk.get("title", "Notes for examiners:")), ParagraphStyle("nh", parent=BODY, spaceAfter=3)))
            st = ParagraphStyle("nb", parent=SMALL, leftIndent=14, bulletIndent=3, spaceAfter=4)
            for it in blk["items"]:
                out.append(Paragraph(md(it), st, bulletText="•"))
        elif kind == "code":
            if blk.get("title", "Example answer"):
                out.append(Paragraph("<b>%s</b>" % md(blk.get("title", "Example answer")), BODY))
            out += code_block(blk["code"], blk.get("lang", lang), W - 6)
        else:
            out += [f for f in render_blocks([blk], W, lang) if not isinstance(f, tuple)]
    return out


def build_markscheme(spec, path):
    meta, ms = spec["meta"], spec["markscheme"]
    lang = meta.get("code_language", "")
    story = cover(meta, extra_title="Markscheme")
    story += [Spacer(1, 8), hrule(FRAME_W), Spacer(1, 10)]
    q_sum = 0.0
    for q in ms.get("questions", []):
        for p in q.get("parts", []):
            q_sum += numeric(p.get("marks")) or 0
    total = meta.get("total_marks", fmt_num(q_sum) if q_sum else None)
    if total:
        story.append(Paragraph("<b>Total: [%s marks]</b>" % total, BODY))
    if ms.get("general"):
        story += [Spacer(1, 4), Paragraph("<b>%s</b>" % md(ms.get("general_title", "General marking instructions")), BODY)]
        st = ParagraphStyle("gm", parent=BODY, leftIndent=14, bulletIndent=3, spaceAfter=5)
        for it in ms["general"]:
            story.append(Paragraph(md(it), st, bulletText="•"))
    if ms.get("abbreviations"):
        story += [Spacer(1, 4), Paragraph("<b>Abbreviations</b>", BODY)]
        story += simple_table({"rows": ms["abbreviations"], "col_fractions": [0.18, 0.82]}, FRAME_W)
    if ms.get("summary"):
        sm = ms["summary"]
        story += [Spacer(1, 6), Paragraph("<b>%s</b>" % md(sm.get("title", "Summary of marks")), BODY)]
        story += simple_table(sm, FRAME_W)
    story.append(PageBreak())
    show_totals = ms.get("question_totals", True)
    for q in ms.get("questions", []):
        story.append(Paragraph("<b>Question %s</b>" % q["number"], ParagraphStyle("qh", parent=BODY, fontSize=13, leading=17, spaceBefore=6)))
        qt = 0.0
        for p in q.get("parts", []):
            qt += numeric(p.get("marks")) or 0
            head = Table([[Paragraph("<b>%s</b>" % md(p.get("label", "")), BODY), mark_cell(p.get("marks"), bold=True)]],
                         colWidths=[FRAME_W - MARK_W, MARK_W])
            head.setStyle(TableStyle([("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                                      ("TOPPADDING", (0, 0), (-1, -1), 0), ("BOTTOMPADDING", (0, 0), (-1, -1), 0)]))
            first = [Spacer(1, 10), head, Spacer(1, 4)]
            if p.get("intro"):
                first += paras(p["intro"])
            body = ms_blocks(p.get("blocks", []), lang)
            story.append(KeepTogether(first + body[:1]))
            story += body[1:]
        if show_totals and qt:
            story += [Spacer(1, 4), Paragraph("<b>Total [%s marks]</b>" % fmt_num(qt), RIGHT), Spacer(1, 6)]
        if q.get("new_page_after"):
            story.append(PageBreak())
    if ms.get("teacher_notes"):
        story += [Spacer(1, 14), hrule(FRAME_W, 0.4), Spacer(1, 6),
                  Paragraph("<b>%s</b>" % md(ms.get("teacher_notes_title", "Notes for teachers (not part of the markscheme)")), BODY)]
        st = ParagraphStyle("tn", parent=BODY, leftIndent=14, bulletIndent=3, spaceAfter=5)
        for it in ms["teacher_notes"]:
            story.append(Paragraph(md(it), st, bulletText="•"))
    footer = meta.get("markscheme_footer", "Markscheme — %s %s" % (meta.get("subject", ""), meta.get("paper", ""))).strip()
    doc = make_doc(path, "Markscheme — %s" % meta.get("subject", ""))
    doc.build(story, canvasmaker=canvas_class("text", meta, footer))


PAGE_SIZE = A4


def main():
    global SPEC_DIR, PAGE_SIZE, PAGE_W, PAGE_H, FRAME_W
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    spec_path = sys.argv[1]
    SPEC_DIR = os.path.dirname(os.path.abspath(spec_path))
    spec = json.load(open(spec_path, encoding="utf-8"))
    meta = spec["meta"]
    if str(meta.get("page_size", "A4")).lower() == "letter":
        PAGE_SIZE = LETTER
        PAGE_W, PAGE_H = LETTER
        FRAME_W = PAGE_W - MARGIN_L - MARGIN_R - 2 * FRAME_PAD
    out_dir = sys.argv[2] if len(sys.argv) > 2 else meta.get("folder", ".")
    os.makedirs(out_dir, exist_ok=True)
    stem = meta.get("file_stem", "%s %s" % (meta.get("subject", "IB"), meta.get("paper", "Paper"))).strip()
    qp = os.path.join(out_dir, "%s - Question Paper.pdf" % stem)
    build_question_paper(spec, qp)
    print(qp)
    if spec.get("markscheme"):
        mp = os.path.join(out_dir, "%s - Markscheme.pdf" % stem)
        build_markscheme(spec, mp)
        print(mp)
    if not UNICODE_OK:
        warn("no TrueType font found; used Helvetica/Courier with ASCII fallbacks for symbols")
    for w in WARNINGS:
        print("warning: " + w, file=sys.stderr)


if __name__ == "__main__":
    main()
