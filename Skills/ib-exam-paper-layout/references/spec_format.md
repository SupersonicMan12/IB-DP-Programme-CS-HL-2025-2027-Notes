# Spec format for `scripts/render_ib_paper.py`

One JSON file describes the question paper and, optionally, the markscheme.
```
python3 scripts/render_ib_paper.py spec.json "<output folder>"
```
Output: `<file_stem> - Question Paper.pdf`, plus `<file_stem> - Markscheme.pdf` if the spec has a
`markscheme` key. Warnings (mark totals that don't match, missing images, equations falling back to text)
go to stderr, so read them.

Dependencies: `reportlab` (required); `Pillow` for PNG images; `matplotlib` for `equation` blocks.
Fonts: Arial / Courier New if installed, otherwise Liberation or DejaVu, otherwise Helvetica/Courier.

Worked examples: `assets/example_maths.json` (sections, max-mark headers, answer lines, image,
equation, M1/A1 markscheme) and `assets/example_computer_science.json` (one long multi-page
question with tables, code, a restrictions box, and a detailed [1]-per-point markscheme).

## Inline markup (every text field)
| Write | Result |
|---|---|
| `` `code` `` | monospace, escaped automatically |
| `<b> <i> <u> <sup> <sub> <br/>` | bold, italic, underline, superscript, subscript, line break |
| `$f(x) = 2x^2 - 8x + 3$` | *f*(*x*) = 2*x*² − 8*x* + 3 (letters italic, `-` → −) |
| `$S_{20}$`, `$x^{10}$`, `$\\frac{9}{4}$`, `$\\sqrt{3}$` | subscript, superscript, 9/4, √3 |
| `\\times \\div \\pm \\le \\ge \\ne \\approx \\infty \\pi \\theta \\alpha \\beta \\Delta \\mu \\lambda \\sigma \\degree \\cdot` | × ÷ ± ≤ ≥ ≠ ≈ ∞ π θ α β Δ μ λ σ ° · |
| `\n\n` inside a text value | new paragraph |

Inline `$…$` is for short expressions. Use an `equation` block for integrals, stacked fractions, matrices and so on.
In JSON, backslashes are doubled (`"$K \\times K$"`). Literal `<`, `>` and `&` are escaped automatically.

## meta
| key | example | notes |
|---|---|---|
| `subject` | "Mathematics: analysis and approaches" | cover title |
| `level` | "Standard level" | |
| `paper` | "Paper 1 (practice extract)" | |
| `title` | "Option A — Java" | optional extra cover line |
| `duration` / `suggested_time` | "1 hour 30 minutes" | shown on the cover |
| `instructions` | [..] | cover bullets (default: open / answer all / max mark) |
| `total_marks` | 19 | optional; computed from the parts if omitted; warns if it doesn't match |
| `show_max_mark` | true | "[Maximum mark: n]" above every question (n is computed from the parts) |
| `lead_line` | "All code … written in Java." | bold line at the top of page 2 |
| `cover_note` | "…" | paragraph at the bottom of the cover |
| `cover_blocks` | [block, ..] | extra blocks on the cover (e.g. a table of options) |
| `end_text` | "End of examination paper" | after the last question |
| `code_language` | "java" / "python" / "pseudocode" / "sql" / "" | default code highlighting |
| `header_left` / `header_right` | "Practice 2026" | small header text on pages 2+ |
| `markscheme_footer` | "Markscheme — …" | footer text of the markscheme |
| `file_stem` | "Maths AA SL P1 - Practice Extract" | file names |
| `folder` | "Maths AA SL P1 - Practice Extract" | default output folder |
| `page_size` | "A4" / "letter" | default A4 |

## paper (list, in order)
| item | fields |
|---|---|
| `{"type":"section"}` | `title`, optional `text`, optional `new_page` |
| `{"type":"question"}` | `number`, `blocks` [..], optional `max_mark`, `show_max_mark`, `new_page` |
| `{"type":"pagebreak"}` | — |
| any block (below) | rendered at full width, outside any question |

## blocks (inside questions, parts, the cover, or markscheme parts)
| type | fields | notes |
|---|---|---|
| `text` | `text`, optional `align: "center"` | the first text block of a question carries the hanging number |
| `parts` | `parts`: list of part objects (below) | |
| `grid` | `caption`, `col_title`, `row_title`, `col_headers`, `rows` [[label, v..]], `bold_cells` [[r,c]], `cell_width_cm`, `label_width_cm`, `row_labels`, `source` | index-style figure with boxed cells; `""` = blank cell to fill in |
| `table` | `header`, `rows`, `col_fractions`, `align` ["left","center",..], `font_size`, `shade_header`, `caption`, `source` | ruled table (data tables, level descriptors) |
| `image` | `path` (relative to the spec file), `width_cm`, `caption`, `source`, `align` | PNG/JPG |
| `equation` | `latex`, `size` (default 13), `align` ("center"/"left"), `fontset` ("dejavusans", "stix", "cm") | matplotlib mathtext |
| `code` | `code`, `lang` | framed listing; keep lines ≤ 78 characters |
| `box` | `text` | ruled box (restrictions, extracts, instructions) |
| `bullets` | `items`, optional `numbered` | |
| `lines` | `count` | dotted answer lines |
| `spacer` | `height_cm` | |
| `source` | `text` | small right-aligned source line |
| `pagebreak` | — | inside a question: adds the "continues / continued" notes |

**Part object**
```json
{"label": "b", "text": "Hence find …", "marks": 3, "lines": 4}
{"label": "c", "subparts": [
    {"label": "i", "text": "Find the value of", "marks": 3, "blocks": [{"type": "equation", "latex": "…"}]},
    {"label": "ii", "text": "Hence write down …", "marks": 1}]}
```
Optional on parts/sub-parts: `lines` (dotted answer lines), `space_cm` (blank space), `code`,
`blocks` (any blocks rendered inside the part, e.g. a table or image).

## markscheme (optional)
```json
{
  "general": ["…", "…"],                     // bullets under "General marking instructions"
  "general_title": "General marking instructions",
  "abbreviations": [["<b>M</b>", "Method mark …"], …],
  "summary": {"title": "Summary of marks", "header": ["Part","Marks","Skill","Syllabus"],
              "rows": [[…]], "col_fractions": [0.16, 0.09, 0.47, 0.28]},
  "question_totals": true,                   // "Total [n marks]" after each question
  "questions": [
    {"number": 1, "parts": [
      {"label": "(a)", "marks": 2, "intro": "Award <b>[1]</b> for each of the following:",
       "blocks": [
         {"type": "points", "items": [{"text": "…;", "marks": 1}, "point without a mark"]},
         {"type": "points", "bullet": "", "items": [{"text": "$x = 2$", "marks": "A1"}]},
         {"type": "code", "code": "…", "title": "Example answer"},
         {"type": "notes", "items": ["…"], "title": "Notes for examiners:"},
         {"type": "equation", "latex": "…"}, {"type": "table", …}, {"type": "grid", …}, {"type": "text", "text": "…"}
       ]}
    ]}
  ],
  "teacher_notes": ["…"]
}
```
- Numeric marks are shown as `[n]`. Strings are shown exactly as written: `"M1A1"`, `"(A1)"`,
  `"A1 AG"`, `"[2 max]"`.
- The `marks` of a part (numeric) feed the question totals and the cover total.
- A part heading always stays on the same page as its first block.

## Tips
- For long or repetitive content, write the JSON from a small Python script (for example, read code or data
  from files so they match the source exactly).
- After rendering, convert the pages to PNG and look at every page (`pdftoppm -r 70 -png file.pdf
  page`, or PyMuPDF: `page.get_pixmap(dpi=70).save(...)`). Fix page breaks by moving or adding
  `pagebreak` blocks, then re-render.
