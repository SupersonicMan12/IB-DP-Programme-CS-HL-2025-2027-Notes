---
name: ib-exam-paper-layout
description: Lays out supplied exam questions, and optionally their markscheme, as IB Diploma Programme-style PDFs for any subject (maths, sciences, computer science, economics, languages and others). Handles cover page and instructions, hanging question numbers, (a)(i) parts with right-aligned [marks], [Maximum mark] headers, sections, figures, tables, code, equations, answer lines, continuation notes, "Turn over" footers, and IB markscheme notation ([1] points, M1/A1/AG). Use when the user wants questions or a mock paper formatted, typeset or exported in IB style. It does not write, solve or mark questions.
---

# IB exam paper layout

This skill turns content the user **already has** into PDFs that look like a real IB Diploma Programme
examination paper and markscheme. It is layout only:

- **Do not** invent, rewrite, solve or extend questions.
- **Do not** write a markscheme. If the user supplies one, lay it out. If they don't, produce only
  the question paper.
- You may make purely typographic changes: proper symbols (× − ≤ °), italic variables, consistent
  part labels, IB-style "[n]" marks. Anything that looks like a content problem (marks that don't
  add up, a missing part, a figure that is referred to but not supplied, a non-IB command term) goes
  in a list for the user. Don't silently fix it.

## Bundled resources
- `references/ib_layout_conventions.md`: how IB papers and markschemes look, for every subject
  (cover, headers, parts and marks, sections, figures, sources, answer lines, markscheme
  notation by subject family, consistency checks). **Read before laying out.**
- `references/spec_format.md`: the JSON spec the renderer reads (all block types, markup, options).
- `scripts/render_ib_paper.py`: renders the spec into `<stem> - Question Paper.pdf` and (optionally)
  `<stem> - Markscheme.pdf`. Needs `reportlab`; `Pillow` for images; `matplotlib` for equations.
- `assets/example_maths.json` (+ `example_math_graph.png`): a sections / answer lines / image /
  equation / M1A1 example.
- `assets/example_computer_science.json`: one long multi-page question with tables, code and a
  detailed [1]-per-point markscheme.

## Workflow

1. **Collect the inputs and settings.**
   - Content: question text (pasted, uploaded document, images of a paper, notes), any figures or
     data, and the markscheme if there is one.
   - Settings: subject, level (HL/SL), paper name, duration or suggested time, instructions,
     whether to show [Maximum mark: n], answer lines or not, output folder/file names, page size.
     Take these from the content where you can. Ask only about things you can't infer and that
     would visibly change the paper. Otherwise use sensible defaults from
     `ib_layout_conventions.md` and say which ones you used.
   - Read `references/ib_layout_conventions.md` and `references/spec_format.md`. Open the example
     closest to the subject.

2. **Map the content to a spec (JSON)** without changing its meaning:
   - Stimulus → `text`/`grid`/`table`/`image`/`code`/`box` blocks, placed exactly where the source
     puts them (between parts, before the parts that use them).
   - Questions → `question` items; parts/sub-parts → `parts` with numeric `marks`.
   - Figures and tables get numbered captions above them; sources go below in small type.
   - Supplied images: save them next to the spec and point to them with `image.path`. If a figure is
     described but not supplied, put a clearly marked placeholder (`box` with
     "[Figure to be inserted: …]") and tell the user.
   - Complex maths → `equation` blocks; short maths → inline `$…$`.
   - Markscheme (if supplied) → `markscheme.questions[].parts[]`, keeping the user's mark points
     and notation (`[1]` points with ";" for sciences/CS, `M1`/`A1`/`AG` strings for maths, level
     tables for essays).
   - For anything long, generate the JSON with a short Python script instead of typing it by hand.

3. **Render.**
   ```bash
   pip install reportlab pillow matplotlib   # only if missing
   python3 scripts/render_ib_paper.py spec.json "<output folder>"
   ```
   Read the warnings: mark totals that don't match, missing images, equations shown as text.

4. **Inspect every page visually.** Convert pages to images (PyMuPDF `page.get_pixmap(dpi=70)` or
   `pdftoppm -r 70 -png`) and check them against the consistency list at the end of
   `ib_layout_conventions.md`: no orphaned headings or captions, marks flush right, figures not split,
   continuation notes only where a question really continues, "Turn over" on every page but the
   last, no blank pages. Move or add `pagebreak` blocks and re-render until it's clean.

5. **Deliver.** Put the PDFs in the folder the user wants (default: a folder named after
   `file_stem`, e.g. `Physics HL P2 - Mock 1/`). Give the paths (or download links in a chat app),
   a summary (pages, questions, total marks), the defaults you assumed, and the list of
   content issues you noticed but didn't change.

## Defaults when the user doesn't say
- A4, Arial-like 11 pt; question numbers as in the source (otherwise 1, 2, 3 …).
- Instructions: "Do not open …", "Answer all questions.", "The maximum mark for this examination
  paper is [N marks]." (N computed from the parts).
- `show_max_mark`: on for mathematics and sciences, off otherwise.
- Answer lines: only if the user asks for a question–answer booklet (about 1.5 lines per mark).
- File names: `<Subject short> <Level> <Paper> - <Title> - Question Paper.pdf` / `- Markscheme.pdf`.
- Practice material is labelled "(practice)". Never present it as an official IB paper or invent
  official paper codes.
