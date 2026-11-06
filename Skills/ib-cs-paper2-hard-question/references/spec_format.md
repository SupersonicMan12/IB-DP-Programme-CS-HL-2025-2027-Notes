# Spec format for `scripts/render_ib_pdf.py`

One JSON file describes both PDFs. The complete worked example is `assets/example_solar_farm.json`:
copy it and edit it.

```
python3 scripts/render_ib_pdf.py my_question.json "<output folder>"
```
The only dependency is `reportlab` (`pip install reportlab`). The script uses Arial / Courier New if
they're installed, otherwise Liberation or DejaVu, otherwise Helvetica/Courier (with ASCII fallbacks for − ≤ ≥).

## Inline markup (every text field)
| Write | Get |
|---|---|
| `` `code` `` | monospace (escaped automatically, so `` `a < b` `` is fine) |
| `<b>…</b>` `<i>…</i>` `<sup>…</sup>` `<br/>` | bold, italic, superscript, line break |
| `$K \\times K$` | *K* × *K* (in JSON, backslashes are doubled) |
| `$1 \\le i \\le R$`, `$O(N^2 \\log N)$`, `$6 \\times 10^{10}$` | ≤, superscripts, upright "log", O stays upright |
| `\n\n` inside a text value | new paragraph |

Write the minus sign as `−` (U+2212) in plain text, e.g. "returns −1". Inside `$…$`, `-` is converted for you.

## Top level
```json
{
  "meta": { ... },
  "question": [ block, ... ],
  "markscheme": { ... }
}
```

### meta
| key | example | notes |
|---|---|---|
| `context` | "Solar Farm Grid" | used in the PDF title |
| `file_stem` | "Solar Farm Grid" | file names: `<stem> - Question Paper (HL P2 Q6, Java).pdf` |
| `folder` | "HL Paper 2 Hardest Question - Solar Farm Grid" | default output folder |
| `language` | "Java" | or "Python" (changes syntax highlighting and the cover instruction) |
| `question_number` | 6 | IB HL P2 Java option is Q1–6, so the last/hardest is 6 |
| `total_marks` | 25 | must equal the sum of the part marks |
| `suggested_time` | "40 minutes" | ≈ 1.5 min per mark |
| `cover_note` | "This question is written to the style of …" | optional |
| `instructions` | [..] | optional override of the cover bullets |
| `subject`, `level`, `paper` | | optional overrides |

### question blocks
| type | fields | renders |
|---|---|---|
| `text` | `text` | paragraphs. The **first** text block gets the hanging question number |
| `grid` | `caption`, `col_title`, `row_title`, `col_headers` [..], `rows` [[label, v1, v2..], ..], optional `bold_cells` [[r,c]..], `cell_width_cm`, `row_labels` (default true) | an IB figure table; use `""` for blank cells to complete |
| `table` | `header` [..], `rows` [[..]], optional `col_fractions` | plain ruled table |
| `code` | `code`, optional `lang` | framed listing with bold keywords and italic comments |
| `box` | `text` | ruled box (use for restrictions) |
| `bullets` | `items` [..] | bullet list |
| `parts` | `parts`: [{`label`:"b", `text`, `marks`, optional `code`} or {`label`:"a", `subparts`:[{`label`:"i", `text`, `marks`}, ..]}] | lettered parts with right-aligned marks |
| `spacer` | `height_cm` | vertical space |
| `pagebreak` | — | "(Question n continues on the following page)" → new page → "(Question n continued)" |

### markscheme
```json
{
  "general": ["Each mark point is shown followed by <b>[1]</b> ...", ...],
  "summary": [["(a)(i)", "1", "Skill", "B2.2.2"], ..., ["<b>Total</b>", "<b>25</b>", "", ""]],
  "parts": [
    {"label": "(c)", "marks": 4, "intro": "Award <b>[1]</b> for each of the following:",
     "blocks": [
       {"type": "points", "items": [{"text": "loops over ...;", "marks": 1}, "point without a mark"]},
       {"type": "code", "code": "public int bestBlock(int k) {...}", "title": "Example answer"},
       {"type": "grid", ...}, {"type": "table", ...}, {"type": "text", "text": "..."},
       {"type": "notes", "items": ["Using `>=` ... do not award the third mark.", ...]}
     ]}
  ],
  "teacher_notes": ["<b>Difficulty.</b> ...", ...]
}
```
A part heading is always kept on the same page as its first block.

## Tips
- Generate the JSON from a small Python script. Read the model answers from the tested `.java`
  file so the markscheme code is byte-for-byte the code you tested, and compute the figure and
  table values in the same script.
- After rendering, convert the pages to PNG (e.g. `pdftoppm -r 70 -png file.pdf page`, or PyMuPDF if
  it's available) and look at every page: page breaks, headings left alone at the bottom of a page,
  tables, long code lines (keep code lines ≤ 78 characters).
