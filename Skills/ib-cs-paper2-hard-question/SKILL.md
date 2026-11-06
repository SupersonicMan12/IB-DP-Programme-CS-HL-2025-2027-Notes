---
name: ib-cs-paper2-hard-question
description: Writes an original IB Diploma Computer Science HL Paper 2 (first assessment 2027) programming question at the level of the hardest question on the paper (Codeforces ~1300-1500, no complex data structures), with a full IB-style markscheme, both delivered as PDFs in a named folder. Use when the user asks for an IB CS paper 2 question, a mock or practice exam question, a hard IB programming problem, or an IB markscheme for a programming question.
---

# IB CS HL Paper 2: hardest-question generator

You produce **two PDFs**, a question paper and a markscheme, in a properly named folder. Together
they should be hard to tell apart from the final, hardest question on a real IB DP Computer Science
HL paper 2 (2027 syllabus). The algorithmic core should be a Codeforces 1300–1500 idea, built only
from syllabus tools (arrays, loops, selection, methods, a class, Big O, binary search, simple sorts).

## Defaults (unless the user says otherwise)
- Language: **Java only** (one option, no Python version). If the user wants Python, write the
  whole question in Python. Only write both versions (Option A Java Q6 / Option B Python Q12, same
  context) if they explicitly ask for both.
- Level: HL, question number 6, about **20–25 marks**, suggested time ≈ 1.5 min per mark.
- Output folder: `HL Paper 2 Hardest Question - <Context Name>/` containing
  `<Context Name> - Question Paper (HL P2 Q6, Java).pdf` and
  `<Context Name> - Markscheme (HL P2 Q6, Java).pdf`. If the user has a practice-sets folder,
  put it there. Deliver only the two PDFs in the folder; keep working files elsewhere.

## Bundled resources
- `references/syllabus_theme_B.md`: the 2027 syllabus for theme B and the Paper 2 rules. **Read first.**
- `references/ib_style_guide.md`: question/markscheme conventions, the 20–25 mark structure,
  command terms, and the quality checklist. **Read before writing.**
- `references/problem_patterns.md`: a menu of Codeforces 1300–1500 ideas that fit the syllabus.
- `references/spec_format.md`: the JSON format for the PDF renderer.
- `assets/example_solar_farm.json`: a complete, finished exemplar (2D prefix sums + binary
  search on the answer, 25 marks). Match its tone, density, scaffolding and markscheme detail.
- `assets/example_solution/`: the exemplar's tested Java model answer (`SolarFarm.java`), a
  brute-force random tester (`TestSolarFarm.java`), and a Python mirror test (`mirror_test.py`)
  for sandboxes without Java.
- `scripts/render_ib_pdf.py`: renders the JSON spec into both PDFs (needs only `reportlab`).

## Workflow

1. **Read the references** listed above, and skim the exemplar JSON so you know the target quality.
   If the user uploaded their own syllabus, past papers or notes, check them too and follow them
   where they differ from the bundled references.

2. **Design the problem** (think it through before writing anything):
   - Pick one core insight from `problem_patterns.md` (or an equivalent one). Use a new real-world
     context, not the solar farm, unless asked.
   - Lay out the scaffold from the style guide: stimulus → (a) read the figure → (b) helper →
     (c) naive solution with a precise tie rule → (d) Big O → new stimulus with a size constraint
     and a precisely *defined* efficient structure → (e) trace + build it → (f) explain the key
     property, construct the efficient method, give its Big O.
   - Write a class skeleton (attributes + constructor). The student methods are instance methods.
   - Decide the restrictions box (ban `Math`, `Arrays`, `Collections`, streams; in Python ban
     `sum/max/min/sorted/sort`/imports) so that no part can be trivialized.
   - Check every required skill against `syllabus_theme_B.md`. No hash maps as the key idea, no
     trees, graphs, heaps or branching recursion.

3. **Write and verify the model answers**:
   - Write the full class with every method the student must construct, exactly as it will appear in
     the markscheme (IB-readable: plain loops, clear names, lines ≤ 78 characters, no library shortcuts).
   - Write a brute-force reference and a random tester (see `assets/example_solution/`). Run thousands
     of small random cases, including edge cases (1×1, a single row/element, all zeros, no answer, ties),
     plus one large case to confirm the efficient method is fast.
   - If `javac` is available, compile and run the Java. If not, translate the Java line for line into a
     Python mirror, test the mirror, then re-read the Java against it to check that the two match.
   - **Compute every number** that appears anywhere (figure data, worked examples, tie-rule
     demonstrations, completed tables, test data, operation counts) with code. Never by hand.
   - Choose the small figure so that a tie and a "no answer" case really happen, and so that `>` vs
     `>=` gives a different output.

4. **Write the markscheme** following the style guide: general instructions, a summary table with
   syllabus references, and for each part mark points ending in ";" with [1], the tested example
   answer, and examiner notes (common errors with the exact mark lost, accepted alternatives,
   [n max] caps for inefficient methods, follow-through, test data). Finish with teacher notes
   (difficulty claim, operation counts, extra check values, testing statement).

5. **Build the JSON spec** (best done with a small Python script that reads the tested source file and
   computes the tables), then render it:
   ```bash
   pip install reportlab   # if missing
   python3 scripts/render_ib_pdf.py spec.json "HL Paper 2 Hardest Question - <Context Name>"
   ```
   Put `pagebreak` blocks at logical points: after the stimulus and class skeleton, after the naive
   parts, before the efficient-structure stimulus.

6. **Inspect the result visually.** Convert every page to an image and look at it: page breaks and
   continuation notes, marks aligned right, no heading left alone at the bottom of a page, tables
   centred, code inside the frame, "Turn over" on every page except the last. Fix and re-render
   until it's clean. Run the quality checklist in `ib_style_guide.md`.

7. **Deliver**: give the user the folder/PDF paths (or download links in a chat interface) and a short
   summary: the core idea, the part-by-part marks, what was verified and how, and anything they might
   want to change (for example, which parts to drop to bring the total to 20 marks).

## Non-negotiables
- The final construct must need real algorithmic insight (Codeforces 1300–1500), not just more code.
- The stimulus defines the efficient structure but never gives away its recurrence, query formula
  or search bounds.
- Every numeric claim is backed by code that was actually run. The markscheme code is the tested code.
- IB tone: neutral, precise, command terms, no hints in bold, no emojis, no mention of Codeforces in
  the question paper (only in the teacher notes).
