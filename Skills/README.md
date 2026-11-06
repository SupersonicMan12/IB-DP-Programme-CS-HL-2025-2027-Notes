# Skills

Two independent skills in the open `SKILL.md` format. Each zip contains one top-level folder with
`SKILL.md` inside, and each skill is self-contained: neither depends on this folder or on the other skill.

| Zip | What it does |
|---|---|
| `ib-cs-paper2-hard-question.zip` | **Writes** an original IB CS HL Paper 2 (2027 syllabus) "hardest question" (Codeforces ~1300–1500, no complex data structures), tests the model answers, and produces the question paper and markscheme PDFs. Default: Java only. |
| `ib-exam-paper-layout.zip` | **Layout only**, for any IB subject: turns questions (and a markscheme, if you supply one) into IB-style PDFs. It does not write, solve or mark anything. Supports sections, [Maximum mark] headers, figures and images, tables, code, equations, dotted answer lines, continuation notes, and IB markscheme notation ([1] points, M1/A1/AG). |

Example prompts:
- *"Write the hardest IB CS HL paper 2 question, Java, with markscheme PDFs."*
- *"Lay out these three physics questions as an IB HL Paper 2 mock with answer lines; here is the markscheme too."*

## Installing

### Claude (claude.ai / desktop app)
1. Settings → Capabilities: turn on **Code execution and file creation**.
2. Customize → Skills → **+** → Create skill → **Upload a skill** → choose the zip.
3. Turn the skill on and ask as normal.

### Claude Code
Copy the skill folder to `~/.claude/skills/<skill-name>/` (or to `.claude/skills/` in a project).

### ChatGPT
- **Business / Enterprise / Edu (Skills enabled):** sidebar → Plugins → Skills tab → Create →
  **Upload from your computer** → choose the zip. Wait for the scan, then ask as normal (or type `@` to pick the skill).
- **Codex:** put the folder in your Codex skills directory and mention it with `$<skill-name>`.
- **Plus / Free (no skill upload):** create a **Project**. Paste the contents of `SKILL.md` (without
  the `---` header) into the project instructions, and upload every file from `references/`,
  `assets/` and `scripts/` as project files. Then ask in a chat inside that project.

## Notes
- Both renderers need `reportlab` (the layout skill also uses `Pillow` for images and `matplotlib`
  for equations). These are usually already in the Claude and ChatGPT sandboxes; if not, the skill tells the model
  to `pip install` them.
- The renderers use Arial / Courier New when available, otherwise Liberation or DejaVu, otherwise Helvetica/Courier.
