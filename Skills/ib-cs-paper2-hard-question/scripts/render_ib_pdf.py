#!/usr/bin/env python3
"""Render an IB Computer Science paper 2 practice question and its markscheme to PDF.

Usage:
    python3 render_ib_pdf.py spec.json [output_dir]

Writes two PDFs into output_dir (default: the folder named in spec["meta"]["folder"],
or the current directory):
    <meta.file_stem> - Question Paper (HL P2 Q<n>, <Language>).pdf
    <meta.file_stem> - Markscheme (HL P2 Q<n>, <Language>).pdf

Only dependency: reportlab (pip install reportlab). See references/spec_format.md for the spec.

Inline markup allowed in every text field:
    `code`        monospace (contents are escaped automatically)
    <b>..</b>     bold          <i>..</i>  italic        <sup>..</sup> superscript
    <br/>         line break
    $...$         maths: single letters become italic, \\times -> ×, \\le -> ≤, \\ge -> ≥,
                  - -> −, ^2 or ^{10} -> superscript, \\approx -> ≈, \\log -> log
Any other '<', '>' or '&' is escaped, so "a < b" is safe outside backticks.
"""
import json
import os
import re
import sys

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas as rl_canvas
from reportlab.platypus import (Flowable, KeepTogether, PageBreak, Paragraph,
                                SimpleDocTemplate, Spacer, Table, TableStyle,
                                XPreformatted)
from reportlab.platypus.doctemplate import Indenter
from reportlab.lib.fonts import addMapping

# ---------------------------------------------------------------- fonts
SANS_CANDIDATES = [
    ("/System/Library/Fonts/Supplemental/Arial.ttf", "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
     "/System/Library/Fonts/Supplemental/Arial Italic.ttf", "/System/Library/Fonts/Supplemental/Arial Bold Italic.ttf"),
    ("C:/Windows/Fonts/arial.ttf", "C:/Windows/Fonts/arialbd.ttf", "C:/Windows/Fonts/ariali.ttf", "C:/Windows/Fonts/arialbi.ttf"),
    ("/usr/share/fonts/truetype/msttcorefonts/Arial.ttf", "/usr/share/fonts/truetype/msttcorefonts/Arial_Bold.ttf",
     "/usr/share/fonts/truetype/msttcorefonts/Arial_Italic.ttf", "/usr/share/fonts/truetype/msttcorefonts/Arial_Bold_Italic.ttf"),
    ("/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf", "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
     "/usr/share/fonts/truetype/liberation/LiberationSans-Italic.ttf", "/usr/share/fonts/truetype/liberation/LiberationSans-BoldItalic.ttf"),
    ("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
     "/usr/share/fonts/truetype/dejavu/DejaVuSans-Oblique.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans-BoldOblique.ttf"),
]
MONO_CANDIDATES = [
    ("/System/Library/Fonts/Supplemental/Courier New.ttf", "/System/Library/Fonts/Supplemental/Courier New Bold.ttf",
     "/System/Library/Fonts/Supplemental/Courier New Italic.ttf", "/System/Library/Fonts/Supplemental/Courier New Bold Italic.ttf"),
    ("C:/Windows/Fonts/cour.ttf", "C:/Windows/Fonts/courbd.ttf", "C:/Windows/Fonts/couri.ttf", "C:/Windows/Fonts/courbi.ttf"),
    ("/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf", "/usr/share/fonts/truetype/liberation/LiberationMono-Bold.ttf",
     "/usr/share/fonts/truetype/liberation/LiberationMono-Italic.ttf", "/usr/share/fonts/truetype/liberation/LiberationMono-BoldItalic.ttf"),
    ("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf",
     "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Oblique.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-BoldOblique.ttf"),
]
UNICODE_OK = True


def _register(name, paths):
    if not all(os.path.exists(p) for p in paths):
        return False
    try:
        for suffix, p in zip(("", "-Bold", "-Italic", "-BoldItalic"), paths):
            pdfmetrics.registerFont(TTFont(name + suffix, p))
    except Exception:
        return False
    addMapping(name, 0, 0, name)
    addMapping(name, 1, 0, name + "-Bold")
    addMapping(name, 0, 1, name + "-Italic")
    addMapping(name, 1, 1, name + "-BoldItalic")
    return True


def setup_fonts():
    global UNICODE_OK
    sans = next(("IBSans" for c in SANS_CANDIDATES if _register("IBSans", c)), None)
    mono = next(("IBMono" for c in MONO_CANDIDATES if _register("IBMono", c)), None)
    if sans is None:
        UNICODE_OK = False
        sans = "Helvetica"
    if mono is None:
        mono = "Courier"
    return sans, mono


SANS, MONO = setup_fonts()
FALLBACK_CHARS = {"−": "-", "≤": "<=", "≥": ">=", "≈": "~", "–": "-", "—": "-", "…": "...", "⁴": "^4", "³": "^3"}

# ---------------------------------------------------------------- markup


def _maths(m):
    t = m.group(1)
    for a, b in ((r"\times", "×"), (r"\le", "≤"), (r"\ge", "≥"), (r"\approx", "≈"), (r"\log", "log"),
                 (r"\min", "min"), (r"\max", "max"), (r"\cdot", "·")):
        t = t.replace(a, b)
    t = t.replace("-", "−")
    t = re.sub(r"(?<![A-Za-z])([A-NP-Za-z])(?![A-Za-z])", lambda mm: "\x01i\x02" + mm.group(1) + "\x01/i\x02", t)
    t = re.sub(r"\^\{([^}]+)\}|\^(\w)", lambda mm: "\x01sup\x02" + (mm.group(1) or mm.group(2)) + "\x01/sup\x02", t)
    return t.replace(" ", "\u00a0")


def md(text, mono_size=None):
    """Convert the spec's light markup into reportlab paragraph markup."""
    if text is None:
        return ""
    codes = []

    def keep_code(m):
        codes.append(m.group(1))
        return "\x03%d\x03" % (len(codes) - 1)

    s = re.sub(r"`([^`]*)`", keep_code, str(text))
    s = re.sub(r"\$([^$]+)\$", _maths, s)
    for tag in ("b", "/b", "i", "/i", "sup", "/sup", "br/", "br /", "u", "/u"):
        s = s.replace("<%s>" % tag, "\x01%s\x02" % tag)
    s = s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    s = s.replace("\x01", "<").replace("\x02", ">").replace("<sup>", "<super>").replace("</sup>", "</super>")

    def put_code(m):
        c = codes[int(m.group(1))].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        c = c.replace(" ", "\u00a0")
        size = ' size="%s"' % mono_size if mono_size else ""
        return '<font face="%s"%s>%s</font>' % (MONO, size, c)

    s = re.sub("\x03(\\d+)\x03", put_code, s)
    if not UNICODE_OK:
        for a, b in FALLBACK_CHARS.items():
            s = s.replace(a, b)
    return s


# ---------------------------------------------------------------- styles
BODY = ParagraphStyle("body", fontName=SANS, fontSize=11, leading=14.5, spaceAfter=6, alignment=TA_LEFT)
BODY_SMALL = ParagraphStyle("small", parent=BODY, fontSize=9.6, leading=12.5, spaceAfter=2)
CENTER = ParagraphStyle("center", parent=BODY, alignment=TA_CENTER)
RIGHT = ParagraphStyle("right", parent=BODY, alignment=TA_RIGHT, spaceAfter=0)
BOLD = ParagraphStyle("bold", parent=BODY, fontName=SANS + "-Bold" if SANS != "Helvetica" else "Helvetica-Bold")
CODE_STYLE = ParagraphStyle("code", fontName=MONO, fontSize=9.2, leading=11.2)
TITLE = ParagraphStyle("title", parent=BOLD, fontSize=17, leading=22, spaceAfter=4)
SUBTITLE = ParagraphStyle("subtitle", parent=BODY, fontSize=13, leading=17, spaceAfter=3)

PAGE_W, PAGE_H = A4
MARGIN_L = MARGIN_R = 2.4 * cm
MARGIN_T, MARGIN_B = 2.3 * cm, 2.4 * cm
FRAME_W = PAGE_W - MARGIN_L - MARGIN_R - 12  # reportlab frames pad 6pt each side
Q_INDENT = 0.85 * cm
MARK_W = 1.15 * cm

JAVA_KW = set("""abstract boolean break byte case catch char class continue default do double else enum extends
final finally float for if implements import instanceof int interface long new null package private protected
public return short static super switch this throw throws true false try void while var String""".split())
PY_KW = set("""and as assert break class continue def del elif else except False finally for from global if import
in is lambda None nonlocal not or pass raise return True try while with yield self print len range""".split())


def highlight(line, lang):
    """Return reportlab markup for one code line: keywords bold, comments italic."""
    kw = PY_KW if lang.lower().startswith("py") else JAVA_KW
    cmark = "#" if lang.lower().startswith("py") else "//"
    out, i, in_str = [], 0, None
    code_part, comment = line, ""
    for j, ch in enumerate(line):
        if in_str:
            if ch == in_str and line[j - 1] != "\\":
                in_str = None
        elif ch in "\"'":
            in_str = ch
        elif line.startswith(cmark, j):
            code_part, comment = line[:j], line[j:]
            break

    def esc(x):
        return x.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

    for tok in re.split(r"(\"[^\"]*\"|'[^']*'|\b[A-Za-z_]\w*\b)", code_part):
        if not tok:
            continue
        if tok in kw and not tok.startswith(("\"", "'")):
            out.append("<b>%s</b>" % esc(tok))
        else:
            out.append(esc(tok))
    if comment:
        out.append("<i>%s</i>" % esc(comment))
    return "".join(out) if out else " "


def code_block(code, lang, width):
    lines = code.rstrip("\n").split("\n")
    rows = [[XPreformatted(highlight(l, lang), CODE_STYLE) if l.strip() else Spacer(1, CODE_STYLE.leading)]
            for l in lines]
    t = Table(rows, colWidths=[width], hAlign="LEFT")
    t.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 0.6, colors.Color(0.45, 0.45, 0.45)),
        ("LEFTPADDING", (0, 0), (-1, -1), 7), ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 0), ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, 0), 5), ("BOTTOMPADDING", (0, -1), (-1, -1), 5),
    ]))
    return [Spacer(1, 3), t, Spacer(1, 7)]


def grid_table(spec, width):
    """Figure-style table: optional column/row titles, header row/col in bold, boxed data cells."""
    col_headers = spec.get("col_headers", [])
    rows = spec["rows"]
    row_title = spec.get("row_title", "")
    col_title = spec.get("col_title", "")
    has_row_labels = spec.get("row_labels", True)
    data = []
    if col_title:
        data.append([""] + [Paragraph("<i>%s</i>" % md(col_title), CENTER)] + [""] * (len(col_headers) - 1))
    if col_headers:
        data.append([""] + [Paragraph("<b>%s</b>" % md(h), CENTER) for h in col_headers])
    first = len(data)
    bold_cells = set(tuple(x) for x in spec.get("bold_cells", []))
    for ri, r in enumerate(rows):
        lab = r[0] if has_row_labels else ""
        if has_row_labels and ri == 0 and row_title:
            lab_txt = "<i>%s</i> <b>%s</b>" % (md(row_title), md(lab))
        else:
            lab_txt = "<b>%s</b>" % md(lab)
        cells = r[1:] if has_row_labels else r
        row = [Paragraph(lab_txt, RIGHT)]
        for ci, v in enumerate(cells):
            txt = md(v)
            if (ri, ci) in bold_cells:
                txt = "<b>%s</b>" % txt
            row.append(Paragraph(txt, CENTER))
        data.append(row)
    ncols = len(data[-1])
    cw = spec.get("cell_width_cm", 0.95) * cm
    lw = spec.get("label_width_cm", 1.6 if row_title else 0.9) * cm
    t = Table(data, colWidths=[lw] + [cw] * (ncols - 1), hAlign="CENTER")
    st = [("GRID", (1, first), (-1, -1), 0.6, colors.black), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
          ("TOPPADDING", (0, 0), (-1, -1), 2), ("BOTTOMPADDING", (0, 0), (-1, -1), 4)]
    if col_title:
        st.append(("SPAN", (1, 0), (-1, 0)))
    t.setStyle(TableStyle(st))
    out = []
    if spec.get("caption"):
        out.append(Paragraph(md(spec["caption"]), ParagraphStyle("cap", parent=CENTER, spaceAfter=4)))
    out += [t, Spacer(1, 8)]
    return [KeepTogether(out)]


def simple_table(spec, width):
    """Plain table with a bold header row (used for summaries)."""
    header = spec["header"]
    rows = spec["rows"]
    fs = ParagraphStyle("t", parent=BODY, fontSize=9.6, leading=12, spaceAfter=0)
    data = [[Paragraph("<b>%s</b>" % md(h), fs) for h in header]]
    for r in rows:
        data.append([Paragraph(md(c), fs) for c in r])
    fr = spec.get("col_fractions")
    cws = [width * f for f in fr] if fr else None
    t = Table(data, colWidths=cws, hAlign="CENTER", repeatRows=1)
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.5, colors.Color(0.4, 0.4, 0.4)),
                           ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                           ("TOPPADDING", (0, 0), (-1, -1), 2), ("BOTTOMPADDING", (0, 0), (-1, -1), 3)]))
    return [t, Spacer(1, 8)]


class BottomNote(Flowable):
    """Consumes the rest of the frame and prints a centred note at its bottom."""

    def __init__(self, text):
        super().__init__()
        self.text = text

    def wrap(self, aw, ah):
        self.aw, self.ah = aw, ah
        return aw, max(ah - 1, 0)

    def draw(self):
        p = Paragraph(md(self.text), CENTER)
        w, h = p.wrap(self.aw, self.ah)
        p.drawOn(self.canv, 0, 2)


def mark_cell(marks):
    if marks in (None, ""):
        return ""
    return Paragraph("[%s]" % marks, RIGHT)


def paras(text, style=BODY):
    return [Paragraph(md(p), style) for p in str(text).split("\n\n")]


# ---------------------------------------------------------------- question paper
def question_parts(block, width, lang):
    out = []
    L1, L2 = 0.95 * cm, 1.0 * cm
    for part in block["parts"]:
        lab = "(%s)" % part["label"]
        if part.get("subparts"):
            for k, sp in enumerate(part["subparts"]):
                cell = paras(sp["text"])
                if sp.get("code"):
                    cell += code_block(sp["code"], lang, width - L1 - L2 - MARK_W - 10)
                row = [Paragraph(lab if k == 0 else "", BODY), Paragraph("(%s)" % sp["label"], BODY), cell, mark_cell(sp.get("marks"))]
                t = Table([row], colWidths=[L1, L2, width - L1 - L2 - MARK_W, MARK_W])
                t.setStyle(TableStyle([("VALIGN", (0, 0), (2, 0), "TOP"), ("VALIGN", (3, 0), (3, 0), "BOTTOM"),
                                       ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                                       ("TOPPADDING", (0, 0), (-1, -1), 0), ("BOTTOMPADDING", (0, 0), (-1, -1), 2)]))
                out += [t, Spacer(1, 5)]
        else:
            cell = paras(part["text"])
            if part.get("code"):
                cell += code_block(part["code"], lang, width - L1 - MARK_W - 10)
            t = Table([[Paragraph(lab, BODY), cell, mark_cell(part.get("marks"))]],
                      colWidths=[L1, width - L1 - MARK_W, MARK_W])
            t.setStyle(TableStyle([("VALIGN", (0, 0), (1, 0), "TOP"), ("VALIGN", (2, 0), (2, 0), "BOTTOM"),
                                   ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                                   ("TOPPADDING", (0, 0), (-1, -1), 0), ("BOTTOMPADDING", (0, 0), (-1, -1), 2)]))
            out += [t, Spacer(1, 5)]
    return out


def render_blocks(blocks, width, lang, qnum=None):
    story = []
    first_text = True
    for b in blocks:
        t = b["type"]
        if t == "text":
            for p in str(b["text"]).split("\n\n"):
                if first_text and qnum is not None:
                    st = ParagraphStyle("qfirst", parent=BODY, bulletIndent=-Q_INDENT, bulletFontName=BOLD.fontName)
                    story.append(Paragraph(md(p), st, bulletText="%s." % qnum))
                    first_text = False
                else:
                    story.append(Paragraph(md(p), BODY))
        elif t == "code":
            story += code_block(b["code"], b.get("lang", lang), width - 10)
        elif t == "grid":
            story += grid_table(b, width)
        elif t == "table":
            story += simple_table(b, width)
        elif t == "box":
            tb = Table([[paras(b["text"], ParagraphStyle("bx", parent=BODY, spaceAfter=2))]], colWidths=[width])
            tb.setStyle(TableStyle([("BOX", (0, 0), (-1, -1), 0.7, colors.black), ("LEFTPADDING", (0, 0), (-1, -1), 6),
                                    ("RIGHTPADDING", (0, 0), (-1, -1), 6), ("TOPPADDING", (0, 0), (-1, -1), 4),
                                    ("BOTTOMPADDING", (0, 0), (-1, -1), 4)]))
            story += [tb, Spacer(1, 8)]
        elif t == "bullets":
            st = ParagraphStyle("bul", parent=BODY, leftIndent=14, bulletIndent=3, spaceAfter=3)
            for it in b["items"]:
                story.append(Paragraph(md(it), st, bulletText="•"))
            story.append(Spacer(1, 3))
        elif t == "parts":
            story += question_parts(b, width, lang)
        elif t == "spacer":
            story.append(Spacer(1, b.get("height_cm", 0.4) * cm))
        elif t == "pagebreak":
            story.append(("PAGEBREAK", None))
        else:
            raise ValueError("unknown block type: %s" % t)
    return story


class NumberedCanvas(rl_canvas.Canvas):
    """Adds '– n –' headers and footers once the total page count is known."""

    footer_mode = "turnover"
    footer_text = ""

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
        if self.footer_mode == "turnover" and p < total:
            self.setFont(BOLD.fontName, 10.5)
            self.drawRightString(PAGE_W - MARGIN_R - 6, 1.3 * cm, "Turn over")
        elif self.footer_mode == "text":
            self.setFont(SANS, 9)
            self.drawCentredString(PAGE_W / 2, 1.3 * cm, self.footer_text)


def cover(meta, extra_title=None):
    s = [Spacer(1, 1.2 * cm)]
    if extra_title:
        s.append(Paragraph(extra_title, TITLE))
        s.append(Spacer(1, 4))
    s += [Paragraph(md(meta.get("subject", "Computer science")), TITLE),
          Paragraph(md(meta.get("level", "Higher level")), SUBTITLE),
          Paragraph(md(meta.get("paper", "Paper 2 — Extended-response question (practice)")), SUBTITLE)]
    return s


def hrule(width, thickness=0.6):
    t = Table([[""]], colWidths=[width], rowHeights=[2])
    t.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, -1), thickness, colors.Color(0.35, 0.35, 0.35))]))
    return t


def expand_pagebreaks(story, qnum):
    out = []
    for f in story:
        if isinstance(f, tuple) and f[0] == "PAGEBREAK":
            out += [BottomNote("(Question %s continues on the following page)" % qnum), PageBreak(),
                    Indenter(left=-Q_INDENT), Paragraph("(Question %s continued)" % qnum, BODY),
                    Indenter(left=Q_INDENT), Spacer(1, 4)]
        else:
            out.append(f)
    return out


def build_question(spec, path):
    meta = spec["meta"]
    lang = meta.get("language", "Java")
    qnum = meta.get("question_number", 6)
    story = cover(meta)
    story += [Spacer(1, 10), hrule(FRAME_W), Spacer(1, 14)]
    if meta.get("suggested_time"):
        story.append(Paragraph("<b>Suggested time: %s</b>" % md(meta["suggested_time"]), BODY))
        story.append(Spacer(1, 6))
    story.append(Paragraph("<b>Instructions to candidates</b>", BODY))
    st = ParagraphStyle("ins", parent=BODY, leftIndent=14, bulletIndent=3, spaceAfter=4)
    for it in meta.get("instructions", [
            "Do not open this examination paper until instructed to do so.",
            "Answer all parts of the question.",
            "All code that forms part of your response must be written in %s." % lang,
            "The maximum mark for this examination paper is <b>[%s marks]</b>." % meta["total_marks"]]):
        story.append(Paragraph(md(it), st, bulletText="•"))
    if meta.get("cover_note"):
        story += [Spacer(1, 14), Paragraph(md(meta["cover_note"]), BODY)]
    story.append(PageBreak())
    story.append(Paragraph("<b>All code that forms part of your response must be written in %s.</b>" % lang, BODY))
    story.append(Spacer(1, 4))
    story.append(Indenter(left=Q_INDENT))
    story += expand_pagebreaks(render_blocks(spec["question"], FRAME_W - Q_INDENT, lang, qnum), qnum)
    story.append(Indenter(left=-Q_INDENT))
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=MARGIN_L, rightMargin=MARGIN_R, topMargin=MARGIN_T,
                            bottomMargin=MARGIN_B, title="Question %s — %s" % (qnum, meta.get("context", "")),
                            author=meta.get("author", ""))

    class C(NumberedCanvas):
        footer_mode = "turnover"
    doc.build(story, canvasmaker=C)


# ---------------------------------------------------------------- markscheme
def ms_part(p, lang):
    W = FRAME_W
    out = []
    head = Table([[Paragraph("<b>%s</b>" % md(p["label"]), BODY), Paragraph("<b>[%s]</b>" % p["marks"], RIGHT)]],
                 colWidths=[W - MARK_W, MARK_W])
    head.setStyle(TableStyle([("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                              ("TOPPADDING", (0, 0), (-1, -1), 0), ("BOTTOMPADDING", (0, 0), (-1, -1), 0)]))
    first = [Spacer(1, 10), head, Spacer(1, 4)]
    if p.get("intro"):
        first += paras(p["intro"])
    body = []
    for blk in p.get("blocks", []):
        kind = blk["type"]
        if kind == "points":
            for pt in blk["items"]:
                if isinstance(pt, str):
                    pt = {"text": pt}
                row = [Paragraph("–" if UNICODE_OK else "-", BODY), paras(pt["text"], ParagraphStyle("pt", parent=BODY, spaceAfter=0)),
                       mark_cell(pt.get("marks"))]
                t = Table([row], colWidths=[0.6 * cm, W - 0.6 * cm - MARK_W, MARK_W])
                t.setStyle(TableStyle([("VALIGN", (0, 0), (1, 0), "TOP"), ("VALIGN", (2, 0), (2, 0), "BOTTOM"),
                                       ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                                       ("TOPPADDING", (0, 0), (-1, -1), 1), ("BOTTOMPADDING", (0, 0), (-1, -1), 4)]))
                body.append(t)
        elif kind == "text":
            body += paras(blk["text"])
        elif kind == "code":
            if blk.get("title", "Example answer"):
                body.append(Paragraph("<b>%s</b>" % md(blk.get("title", "Example answer")), BODY))
            body += code_block(blk["code"], blk.get("lang", lang), W - 10)
        elif kind == "grid":
            body += grid_table(blk, W)
        elif kind == "table":
            body += simple_table(blk, W)
        elif kind == "notes":
            body.append(Paragraph("<i>Notes for examiners:</i>", ParagraphStyle("nh", parent=BODY, spaceAfter=3)))
            st = ParagraphStyle("nb", parent=BODY_SMALL, leftIndent=14, bulletIndent=3, spaceAfter=4)
            for it in blk["items"]:
                body.append(Paragraph(md(it), st, bulletText="•"))
        else:
            raise ValueError("unknown markscheme block: %s" % kind)
    # keep the heading with the first block so headings never sit alone at a page bottom
    if body:
        out.append(KeepTogether(first + body[:1]))
        out += body[1:]
    else:
        out += first
    return out


def build_markscheme(spec, path):
    meta = spec["meta"]
    ms = spec["markscheme"]
    lang = meta.get("language", "Java")
    qnum = meta.get("question_number", 6)
    story = cover(meta, extra_title="Markscheme")
    story.append(Paragraph("Question %s (%s)" % (qnum, lang), SUBTITLE))
    story += [Spacer(1, 8), hrule(FRAME_W), Spacer(1, 10)]
    story.append(Paragraph("<b>Total: [%s marks]</b>" % meta["total_marks"], BODY))
    story += [Spacer(1, 4), Paragraph("<b>General marking instructions</b>", BODY)]
    st = ParagraphStyle("gm", parent=BODY, leftIndent=14, bulletIndent=3, spaceAfter=5)
    for it in ms.get("general", []):
        story.append(Paragraph(md(it), st, bulletText="•"))
    if ms.get("summary"):
        story += [Spacer(1, 6), Paragraph("<b>Summary of marks and syllabus coverage</b>", BODY)]
        story += simple_table({"header": ["Part", "Marks", "Skill assessed", "Syllabus"], "rows": ms["summary"],
                               "col_fractions": [0.16, 0.09, 0.47, 0.28]}, FRAME_W)
    story.append(PageBreak())
    story.append(Paragraph("<b>Question %s</b>" % qnum, ParagraphStyle("qh", parent=BODY, fontSize=13, leading=17)))
    for p in ms["parts"]:
        story += ms_part(p, lang)
    if ms.get("teacher_notes"):
        story += [Spacer(1, 14), hrule(FRAME_W, 0.4), Spacer(1, 6),
                  Paragraph("<b>Notes for teachers (not part of the markscheme)</b>", BODY)]
        st = ParagraphStyle("tn", parent=BODY, leftIndent=14, bulletIndent=3, spaceAfter=5)
        for it in ms["teacher_notes"]:
            story.append(Paragraph(md(it), st, bulletText="•"))
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=MARGIN_L, rightMargin=MARGIN_R, topMargin=MARGIN_T,
                            bottomMargin=MARGIN_B, title="Markscheme — Question %s" % qnum)

    class C(NumberedCanvas):
        footer_mode = "text"
        footer_text = "Markscheme — HL paper 2 practice question (Question %s, %s)" % (qnum, lang)
    doc.build(story, canvasmaker=C)


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    spec = json.load(open(sys.argv[1], encoding="utf-8"))
    meta = spec["meta"]
    out_dir = sys.argv[2] if len(sys.argv) > 2 else meta.get("folder", ".")
    os.makedirs(out_dir, exist_ok=True)
    lang = meta.get("language", "Java")
    qnum = meta.get("question_number", 6)
    stem = meta.get("file_stem", meta.get("context", "IB CS Question"))
    tag = "(HL P2 Q%s, %s)" % (qnum, lang)
    qp = os.path.join(out_dir, "%s - Question Paper %s.pdf" % (stem, tag))
    mp = os.path.join(out_dir, "%s - Markscheme %s.pdf" % (stem, tag))
    build_question(spec, qp)
    build_markscheme(spec, mp)
    if not UNICODE_OK:
        print("warning: no TrueType font found; used Helvetica with ASCII fallbacks for − ≤ ≥", file=sys.stderr)
    print(qp)
    print(mp)


if __name__ == "__main__":
    main()
