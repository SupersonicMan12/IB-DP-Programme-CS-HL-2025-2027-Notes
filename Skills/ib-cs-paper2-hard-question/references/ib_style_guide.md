# IB paper 2 style guide (question paper and markscheme)

## 1. Question paper conventions

**Layout**
- Cover page: "Computer science / Higher level / Paper 2 — Extended-response question (practice)",
  suggested time, *Instructions to candidates* bullets, maximum mark in bold brackets, and a one-line
  note on syllabus coverage.
- Every page after the cover has a centred "– n –" header. "**Turn over**" goes bottom right on
  every page except the last.
- A bold line before the question: "All code that forms part of your response must be written in Java."
- The question number ("6.") hangs in the left margin and all of the question content is indented.
- Where the question runs onto the next page: "(Question 6 continues on the following page)" at the
  bottom, then "(Question 6 continued)" at the top of the next page. Page breaks go at logical points
  (after the stimulus and class code, after the naive parts, before the efficiency stimulus). IB
  papers leave plenty of white space, so a half-empty page is normal.
- Parts are labelled (a), (b) … and sub-parts (i), (ii) …. A part that has sub-parts shows "(a) (i)"
  on the same line. The marks for each answerable part go flush right in brackets: [3].
- Stimulus text sits *between* parts, never inside them. Each new piece of information comes just
  before the parts that need it.
- Figures are captioned **above**: "**Figure 1**: The array `output` for …". Tables have bold index
  headers and boxed data cells. In a "Copy and complete" figure the cells to fill are empty boxes.
- Restrictions go in a ruled box just before the coding parts, for example:
  "In parts (b), (c), (e)(ii) and (f)(ii) you must **not** use any methods of the `Math`, `Arrays` or
  `Collections` classes, or Java streams. Each method you write is part of the `X` class and may use
  the attributes …". Python version: "you must not use the built-in functions `sum()`, `max()`,
  `min()` or `sorted()`, the list method `sort()`, or any imported module. You may use `len()` and
  `range()`."
- Provide a class skeleton (attributes, constructor, and a comment saying where the students'
  methods go). The answer methods are instance methods that use the attributes. This ties the
  question to B3 OOP the way real HL papers do.
- Identifiers go in monospace; maths variables ($R$, $C$, $K$, $N$) in italics; × not "x"; − not "-".

**Language and command terms.** Use only IB command terms, in bold-free sentence case:

| Term | Expectation | Typical marks |
|---|---|---|
| State / Identify | short answer, no explanation | 1 |
| Outline | brief account | 2 |
| Describe | detailed account | 2–4 |
| Explain | give reasons | 2–4 |
| Construct | write code / an algorithm | 2–8 |
| Trace / Copy and complete | trace table or filled-in table | 2–4 |
| Justify / Evaluate / Discuss | reasoning plus a judgement | 2–6 |
| Calculate / Determine | numerical answer | 1–2 |

**Wording patterns to copy**
- "Construct the method `name(params)` that returns … You may assume that …"
- "For example, for the data in Figure 1, `name(2)` outputs row 2, column 3 and returns 28."
  (Always give at least one worked example for every method students construct.)
- "Justifying your answer, state the worst-case time complexity of `name`, in Big O notation, in
  terms of $N$ only."
- "Using your answers to parts (e)(ii) and (f)(i), construct …" (to chain parts together)
- "Your method must be more efficient than …" / "Your method must have a time complexity of O(…)."
- Tie rules and edge cases are stated explicitly ("If two or more … the one found first …",
  "If no such block exists, the method returns −1.").

## 2. Shape of the hardest question (20–25 marks, about 35–40 minutes)

| Stage | Purpose | Marks |
|---|---|---|
| (a) | Read the stimulus: state a value from the figure, count something in terms of the variables | 1–2 |
| (b) | Construct a small helper method (nested loops / string scan) | 2–3 |
| (c) | Construct the naive full solution **using the helper**, with a precise tie rule | 4 |
| (d) | Big O of the naive solution (needs real thought, e.g. worst case at K≈N/2) | 2 |
| new stimulus | Constraint jump ("up to 1000 × 1000") plus the efficient idea, defined but **not** solved | — |
| (e)(i) | Copy and complete / trace the new structure on the small example | 2 |
| (e)(ii) | Construct the structure efficiently | 3 |
| (f)(i) | Explain the key property that makes the fast method correct | 2 |
| (f)(ii) | **Construct the efficient final method** (the Codeforces 1300–1500 step) | 5–6 |
| (f)(iii) | Big O of the final method | 1 |

The early parts give access marks and a working brute force. The end of the question is where the
Codeforces-level insight has to happen. Name the data structure or idea but never give the
formula or the algorithm away: students must find the recurrence, the O(1) query, or the search
bounds themselves.

## 3. Markscheme conventions
- Cover page: "Markscheme", subject, level, paper, "Question n (Java)", total marks.
- General marking instructions: each mark point shown with [1] and awarded once wherever it appears;
  accept equivalent correct algorithms (while vs for, different names, different correct order);
  the syntax policy; the prohibited-function policy.
- **Summary table**: Part | Marks | Skill assessed | Syllabus reference.
- For each part: a bold heading row "(c)" … "[4]". If needed, "Award **[1]** for each of the
  following:". Then dash-bulleted **mark points that end with a semicolon** and have [1] flush right.
  Each mark point must be checkable on its own, describe *what* must be present (not
  "correct code"), and include inclusive/exclusive bounds where they matter.
- **Example answer** in a framed code block. It must be the exact code you compiled and tested.
- *Notes for examiners:* specific wrong answers and what they lose ("Using `>=` instead of `>` …
  do not award the third mark"), alternative methods to accept, caps ("award **[4 max]**" for a
  correct but inefficient method, "**[1 max]**" when the required form is missing), follow-through
  ("Allow follow-through from (f)(ii)"), and test data with expected outputs.
- In completion tables, award [1] for some correct values and [2] for all of them, and show the
  completed table with the filled-in cells in bold.
- Explanation parts: one mark per distinct idea, and say which keyword is required ("The second mark
  requires an explicit reference to the values being non-negative").
- End with "Notes for teachers (not part of the markscheme)": the difficulty claim (which Codeforces
  idea, roughly what rating), operation counts showing why the naive method fails at full size, extra
  check values (especially the ones that test tie rules), and a statement that the answers were
  compiled and tested against brute force.

## 4. Quality checklist (run before rendering)
- [ ] Every value in the figures, examples, tables, test data and teacher notes was **computed by
      code**, not by hand.
- [ ] The model answers were compiled/run and matched a brute force on thousands of random small inputs
      (including edge cases: 1×1, a single row, all zeros, no answer, ties).
- [ ] The tie rule example in the markscheme really distinguishes `>` from `>=` on the given figure.
- [ ] Total marks = sum of part marks = the cover-page total = the summary-table total.
- [ ] Every skill needed is in `syllabus_theme_B.md`. No hash maps, trees, graphs, heaps or branching recursion.
- [ ] Restrictions block every shortcut that would trivialize a part (`Math.min`, `Arrays.sort`,
      streams; Python `sum`/`max`/`min`/`sorted`).
- [ ] The stimulus defines the efficient structure precisely (indices, sizes, borders) without giving
      the recurrence or the algorithm.
- [ ] Each "Construct" has a worked example call with its result.
- [ ] Only the language the user asked for (default: Java only).
