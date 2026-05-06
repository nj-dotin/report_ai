# Report AI Plan

## Goal
Build a workflow that helps us fill the college project and internship LaTeX report template in Overleaf faster from inside VS Code.

The idea is to create an MCP server that can:
- Access Overleaf through a browser-based automation tool
- Read the LaTeX template and project files
- Help upload images and edit report content
- Reduce manual back-and-forth between VS Code, files, and Overleaf

## Core Idea, Refined
The rough idea is possible, but the best version should be smaller and safer:
- Use MCP for orchestration and helper actions
- Use browser automation for Overleaf interaction
- Keep the user in control for final review and submission
- Avoid trying to fully automate everything at once

A practical setup is:
1. VS Code runs the MCP server.
2. The MCP server exposes tools for reading files, extracting content, and controlling a browser session.
3. The browser tool opens Overleaf and performs guided actions like upload, navigation, and text entry.
4. The user reviews the final report manually before submission.

## What Is Possible
Possible in an MVP:
- Open Overleaf from VS Code
- Upload images and assets
- Read local project files and draft content
- Paste or update LaTeX sections
- Help fill repetitive report sections
- Keep notes of chapters, references, and placeholders

Harder or risky:
- Fully automatic editing of every Overleaf page without user review
- Reliable DOM-based control if Overleaf changes its UI often
- Handling login or captcha flows automatically
- Making perfect LaTeX decisions from vague project notes alone

## MVP Scope
The first version should do only these things:
- Start an MCP server
- Provide a browser tool for Overleaf
- Provide file access tools for local report assets
- Support image upload workflow
- Support basic text replacement in the template
- Keep logs of actions and errors

## Build Plan

### Phase 1: Define the workflow
- Confirm what files the college gives us
- Identify the exact Overleaf workflow
- List common report sections:
  - title page
  - certificate
  - abstract
  - introduction
  - problem statement
  - methodology
  - results
  - conclusion
  - references
- Decide which parts are manual and which parts should be assisted by the MCP server

### Phase 2: Build the MCP server
- Create the server project
- Add tools for:
  - reading local files
  - listing report assets
  - uploading or staging images
  - opening the browser
  - interacting with Overleaf pages
- Add clean logging so we can see what the server did

### Phase 3: Add browser automation
- Use a browser automation layer that can work inside VS Code
- Make it able to:
  - open Overleaf
  - locate project files
  - upload images
  - edit text fields
  - save changes
- Keep actions explicit and inspectable

### Phase 4: Add report helpers
- Add helpers for common LaTeX tasks:
  - section filling
  - placeholder replacement
  - figure insertion
  - caption formatting
  - reference formatting
- Optionally add a content helper that turns rough notes into cleaner report text

### Phase 5: Test with a real template
- Use the college template zip
- Try a small report section first
- Verify images upload correctly
- Check if line breaks, escaping, and LaTeX syntax stay valid
- Fix the workflow before scaling up

### Phase 6: Polish the workflow
- Add a simple command or prompt flow in VS Code
- Make the server easier to reuse for future reports
- Add clear failure messages when Overleaf interaction breaks
- Document the steps for project and internship reports

## Suggested Architecture
- MCP server: Node.js or TypeScript
- Browser automation: Playwright-based tool or similar
- Local file handling: direct workspace file access
- Optional helper layer: prompts or templates for report text

## Risks
- Overleaf UI may change and break selectors
- Browser automation can be brittle if the page loads slowly
- Auto-editing LaTeX can introduce syntax errors
- Login/session handling may require manual steps
- A vague project idea may still need human input for accurate content

## Best First Version
The smartest first version is not full automation. It should only:
- Open Overleaf
- Upload assets
- Help place text into the template
- Keep the user in control

That gives a useful tool quickly without overbuilding.

## Next Steps
1. Confirm the exact tech stack you want for the MCP server.
2. Decide whether to use Playwright or another browser layer.
3. Inspect the template zip and report documents.
4. Build the first MCP tool set.
5. Test one full section in Overleaf.

## Recommended Setup Path For You
Since you are new to MCP and already have useful servers in your VS Code profile, start with the simplest path:

1. Use the existing MCP servers first.
  - Playwright MCP for browser actions.
  - Chrome DevTools MCP for debugging.
  - GitHub MCP only if you need repo or task support.

2. Do not build a custom MCP server yet.
  - First check whether the existing tools can already handle your Overleaf workflow.
  - A custom server only makes sense after you find a repeated gap.

3. Prepare the Overleaf report workflow.
  - Keep the college template zip in the workspace.
  - Extract the template locally if needed.
  - Collect images, figures, and reference files in one folder.

4. Test one small report action.
  - Open Overleaf.
  - Upload one image.
  - Edit one section of text.
  - Confirm the LaTeX still compiles.

5. Only then decide if a custom MCP server is needed.
  - If the browser tools work, keep it simple.
  - If you need repeated file parsing, text generation, or batch image handling, then build a custom server later.

## What To Keep In Mind
- Overleaf is usually better handled by browser automation than by trying to sync everything with a custom integration.
- The safest workflow is: draft locally, push small edits into Overleaf, compile, then review.
- For your project and internship reports, the real value is not full automation; it is reducing manual copy-paste and repeated formatting.

---
---

# 📋 WORK LOG — Everything Done So Far

> This section documents every step taken in this project from creation to current state.
> Last updated: **2026-05-04 18:14 IST**

---

## 🗓️ Phase 0 — Project Initialization (Apr 28, 2026)

### What happened:
- Created the `report_ai` git repo at `d:\Internship Report\report_ai\`
- First commit (`db4e805`): Just the `plan.md` file (135 lines)
- The plan outlined the original idea: build an MCP server that can interact with Overleaf to fill LaTeX report templates from VS Code
- Workflow was: MCP server → Browser automation → Overleaf → LaTeX compilation
- This was the brainstorming phase — no code yet

### Files created:
- `plan.md` — Initial project plan (the content above this section)

### Git:
```
db4e805 — "start" — Apr 28, 2026
```

---

## 🗓️ Phase 1 — Template & Documentation Setup (May 3, 2026 morning)

### What happened:
- Second commit (`0e33041`): Added LaTeX report templates and MCP setup docs
- Uploaded the reference template PDF (`Internship_Report.pdf`) — the official VIT internship report format
- Created documentation files explaining the architecture

### Files created:
- `Internship_Report.pdf` — Official VIT internship report template (reference PDF, ~1MB)
- `Internship_Report_latex.md` — LaTeX source extracted/documented from the template (409 lines)
- `INSTALL_MIKTEX.md` — Guide for installing MiKTeX (LaTeX compiler)
- `MCP_SETUP.md` — MCP server configuration guide
- `QUICK_REFERENCE.md` — Quick reference for the report structure
- `README.md` — Project README (92 lines)
- `WORKFLOW.md` — Step-by-step workflow documentation
- `sample_report.tex` — Sample LaTeX source file
- `mcp-latex-server/` — MCP server submodule (for LaTeX tools)
- `.vscode/mcp.json` — MCP server configuration for VS Code

### Git:
```
0e33041 — "Add LaTeX report templates and MCP setup documentation" — May 3, 2026
```

---

## 🗓️ Phase 2 — Pivot: Overleaf → Local Dashboard (May 3, 2026 afternoon)

### The pivot decision:
- Original plan was Overleaf + browser automation
- Realized this was brittle (Overleaf DOM changes, login issues, captchas)
- **Pivoted to**: Build a local Flask web dashboard that takes user input and generates the PDF directly — no Overleaf needed!

### Architecture designed:
```
Flask Web Dashboard (app.py)
    └─ POST /api/generate
         └─ builder.py → generates .tex file
              └─ tectonic.exe → compiles to PDF
                   └─ Download link
```

### User clarification questions answered:
1. Output format: **PDF via LaTeX** (not DOCX)
2. Template: **VIT college template** (from `Internship_Report.pdf`)
3. Scope: **Internship Reports only** (not project reports)
4. Input method: User **pastes text** into form fields (no file upload for content)
5. AI role: AI generates a **prompt** that user gives to ChatGPT/Gemini → gets back chapter text → pastes into dashboard
6. Images: User uploads figures with captions

---

## 🗓️ Phase 3 — Flask Dashboard Built (May 3, 2026)

### What was built:
- Complete Flask web app with a modern dark-theme UI
- Multi-step form wizard for data entry
- AI prompt generator that creates a customized prompt based on user info

### Files created:
- `app.py` — Flask server (179 lines)
  - Routes: `/` (dashboard), `/api/upload`, `/api/generate-prompt`, `/api/generate`, `/download/<session_id>`
  - Handles image uploads, logo uploads
  - Runs tectonic compiler
  - Serves generated PDF for download
- `builder.py` — LaTeX template generator (536 lines)
  - `generate_latex(data)` function
  - Generates full `.tex` source with all report sections
  - Handles title page, certificate, acknowledgement, abstract, TOC, chapters 1-5
- `prompt_generator.py` — AI prompt generator (150+ lines)
  - Creates a detailed prompt for ChatGPT/Gemini based on user's company + role info
  - Output is a structured prompt the user copies
- `setup_tectonic.py` — Auto-downloads tectonic compiler binary
- `static/style.css` — Dark theme CSS for the dashboard
- `static/app.js` — Frontend JavaScript (form handling, API calls)
- `templates/index.html` — Dashboard HTML template
- `combo_tracker.json` — Tracks unique company+department combos

### Tech stack:
- **Backend**: Flask (Python 3)
- **Frontend**: Vanilla HTML/CSS/JS (dark theme, multi-step wizard)
- **LaTeX compiler**: tectonic (portable binary, no MiKTeX needed)
- **Server**: `http://127.0.0.1:5050`

---

## 🗓️ Phase 4 — Tectonic Compiler Setup (May 3, 2026)

### Problem:
- MiKTeX installation was huge and complex
- Needed a portable, zero-install LaTeX compiler

### Solution:
- Used **tectonic** — a single-binary LaTeX compiler
- Created `setup_tectonic.py` to auto-download it
- Binary placed at `bin/tectonic.exe`
- tectonic auto-downloads LaTeX packages on first compile

### Files:
- `bin/tectonic.exe` — Tectonic binary (portable)
- `setup_tectonic.py` — Download script

---

## 🗓️ Phase 5 — Logo Identification & Asset Bundling (May 4, 2026 morning)

### Problem:
- The template PDF uses **3 different logos** on different pages
- Originally the UI only had 1 "Department Logo" upload slot
- We needed to identify which logo goes where

### Investigation:
- Used **PyMuPDF (fitz)** to extract images from the template PDF
- Identified all 3 logos:

| Logo | File | Where Used |
|------|------|------------|
| VTU University Seal | `assets/vtu_logo.png` (154KB) | Title page — top center |
| VIT College Logo | `assets/vit_logo.png` (342KB) | Title page — below name + Certificate page watermark |
| Department Seal | `assets/dept_seal.png` (25KB) | Certificate page — top center, has "Accredited by NBA" |

### Solution:
- Bundled all 3 logos as fixed assets in `assets/` folder
- VTU and VIT logos are **hardcoded** (same for all students)
- Department logo is bundled too (same for all ECE students)
- Removed redundant logo upload from UI

### Files created:
- `assets/vtu_logo.png` — VTU university seal
- `assets/vit_logo.png` — VIT college logo (colorful V with laurel)
- `assets/dept_seal.png` — ECE department seal with NBA accreditation

---

## 🗓️ Phase 6 — Template Format Extraction (May 4, 2026)

### What happened:
- Created `extract_format.py` to analyze every formatting detail in the template PDF
- Used PyMuPDF to extract:
  - Font names, sizes, colors for every text block
  - Exact positions (x, y coordinates)
  - Border/line coordinates and thicknesses
  - Image positions and dimensions

### Key formatting rules discovered:

**Page dimensions:** 595 × 842 pt (A4)

**Title page:**
- VTU heading: bold, ~14pt
- "INTERNSHIP REPORT" text: bold, ~17pt
- Student name/USN: bold, ~14pt
- Double border (inner 0.28pt, outer 0.56pt)

**Certificate page:**
- Department name in **BLUE** (#0000ff)
- Date range in **RED** (#ff0000)
- VIT logo watermark (opacity reduced)
- Signature block: 4-column layout

**All front-matter pages (Title → List of Figures):**
- Double border on every page
- Roman numeral page numbers (i, ii, iii, iv, v, vi)
- No headers/footers

**All main content pages (Chapter 1 → end):**
- NO border
- Header: `{Internship Title}` (left) | `{CHAPTER NAME}` (right) with `\hrule`
- Footer: `Dept. of ECE, Vemana IT` (left) | `2025-26` (center) | `Page X of Y` (right) with `\hrule`
- Arabic page numbers (1, 2, 3...)

### Files:
- `extract_format.py` — Format extraction script (3720 bytes)

---

## 🗓️ Phase 7 — Builder.py Refactoring (May 4, 2026)

### Major refactor of `builder.py`:
This was the core work — rewriting the entire LaTeX template generator to match the official VIT format.

### Changes made:

1. **Double border implementation**
   - Used `tikz` to draw double borders (inner + outer rectangles)
   - Created `\addBorder` macro that can be toggled per page
   - Borders only applied to front-matter pages

2. **Title page layout**
   - VTU logo at top (from `assets/vtu_logo.png`)
   - University name, Belagavi address
   - "INTERNSHIP REPORT ON" heading
   - Company name, student details (name + USN)
   - Semester, academic year
   - VIT logo below
   - Department name (blue), college name, year

3. **Certificate page**
   - Department seal at top
   - "DEPARTMENT OF {dept}" in blue
   - "CERTIFICATE" heading
   - Certificate text with date range in red
   - 4-column signature layout
   - VIT logo watermark (low opacity)
   - Tight spacing to fit on single page

4. **Acknowledgement page**
   - Structured thank-you paragraphs
   - Name + USN at bottom

5. **Abstract page**
   - User-provided abstract text
   - Minimal top spacing (fixed excessive `\vspace`)

6. **Table of Contents + List of Figures**
   - Auto-generated from LaTeX `\tableofcontents` and `\listoffigures`

7. **Chapters 1-5**
   - Introduction (4 subsections)
   - Organisation Profile (5 subsections)
   - Work Done / Methodology (6 subsections)
   - Results and Discussion (3 subsections)
   - Conclusion (3 subsections)
   - Each chapter supports user-provided text

8. **Page numbering**
   - Front-matter: Roman numerals (i, ii, iii...)
   - Main content: Arabic numerals (1, 2, 3...)

9. **Figure/image support**
   - User-uploaded images placed within chapters
   - Captions and labels auto-generated
   - Added to List of Figures

### Current builder.py stats:
- **536 lines** of Python
- **18,211 bytes**
- Generates ~15-page PDF

---

## 🗓️ Phase 8 — PDF Comparison & Gap Analysis (May 4, 2026 afternoon)

### What happened:
- User generated a test PDF and compared it against the template
- Used PyMuPDF to extract every page of both PDFs as PNG images
- Did a page-by-page visual comparison

### Comparison output directory:
```
generated/pdf_compare/
├── tmpl_p1.png through tmpl_p22.png  (template pages)
├── gen_p1.png through gen_p15.png    (generated pages)
└── extracted_images/                  (logos extracted from template)
```

### Differences found:

#### ❌ CRITICAL — Border + Header/Footer Split
| | Template | Generated |
|---|---|---|
| Front matter | Double border, no header/footer | Double border ✅ |
| Main content | NO border, HAS header + footer | Still has border ❌, no header/footer ❌ |

**This is the #1 priority fix.**

#### ⚠️ Roman Page Numbers Off
- Certificate should be `i`, Acknowledgement `ii`, Abstract `iii`
- Generated is off by 1 in some places

#### ⚠️ Abstract Top Spacing
- Template has ABSTRACT title near top of page
- Generated has huge gap before title

#### ⚠️ Acknowledgement Formatting
- Name+USN should be right-aligned (currently left-aligned)
- Paragraphs need first-line indent + 1.5 line spacing

#### ⚠️ TOC Format
- Template uses custom table format (Chapter | Title | Page No)
- Generated uses default LaTeX `\tableofcontents`

#### ⚠️ Title Page Sizing
- VTU/VIT logos too small
- Name+USN should be on same line

#### ℹ️ Chapter Pages Missing Header/Footer
Template has:
- **Header**: `{Internship Title}` left | `{CHAPTER NAME}` right (with hrule)
- **Footer**: `Dept. of ECE, Vemana IT` left | `2025-26` center | `Page X of Y` right (with hrule)

Generated has: None of this (just borders and page numbers)

---

## 📁 Current File Structure

```
d:\Internship Report\report_ai\
├── .git/                          # Git repo
├── .vscode/
│   └── mcp.json                   # MCP server config
├── assets/                        # Bundled logos (fixed for all students)
│   ├── vtu_logo.png               # VTU university seal
│   ├── vit_logo.png               # VIT college logo
│   └── dept_seal.png              # ECE department seal
├── bin/
│   └── tectonic.exe               # Portable LaTeX compiler
├── generated/                     # Output directory
│   ├── {session-id}/              # Per-generation folders
│   │   ├── report.tex             # Generated LaTeX source
│   │   ├── report.pdf             # Compiled PDF
│   │   └── images/                # Uploaded figures
│   └── pdf_compare/               # Comparison images
├── mcp-latex-server/              # MCP server submodule
├── static/
│   ├── style.css                  # Dashboard dark theme CSS
│   └── app.js                     # Frontend JavaScript
├── templates/
│   └── index.html                 # Dashboard HTML
├── uploads/                       # Temp upload directory
├── app.py                         # Flask server (179 lines)
├── builder.py                     # LaTeX generator (536 lines) ← CORE FILE
├── prompt_generator.py            # AI prompt generator
├── extract_format.py              # PDF format analysis tool
├── setup_tectonic.py              # Tectonic binary downloader
├── combo_tracker.json             # Company+dept tracking
├── Internship_Report.pdf          # Reference template (official VIT format)
├── Internship_Report_latex.md     # Template LaTeX documentation
├── pdf_builder.py                 # Alternative ReportLab-based builder (unused)
├── sample_report.tex              # Sample LaTeX file
├── INSTALL_MIKTEX.md              # MiKTeX install guide (legacy)
├── MCP_SETUP.md                   # MCP setup guide
├── QUICK_REFERENCE.md             # Quick reference
├── README.md                      # Project README
├── WORKFLOW.md                    # Workflow documentation
└── plan.md                        # This file
```

---

## 🔧 How It Works (Current Flow)

```
1. User opens http://127.0.0.1:5050
2. Fills in the dashboard form:
   - Student name, USN, semester, year
   - Department, company name, company supervisor
   - Internal supervisor, external supervisor
   - Internship title, date range
   - Uploads department logo + any figures
3. Clicks "Generate Prompt"
   → Gets a customized AI prompt to paste into ChatGPT/Gemini
4. User pastes AI-generated text back into chapter fields
5. Clicks "Generate Report"
   → app.py calls builder.generate_latex(data)
   → Writes report.tex to generated/{session_id}/
   → Runs tectonic.exe on report.tex
   → PDF compiled
6. User downloads the PDF
```

---

## 🎯 What's Left To Do (Priority Order)

### P0 — Critical Fixes
1. **Remove borders from Chapter 1 onwards** — borders only on front-matter
2. **Add header/footer to chapter pages** — matching template format exactly
3. **Fix Roman numeral page numbering** — correct sequence (i, ii, iii, iv, v, vi)

### P1 — Important Fixes
4. Fix Abstract top spacing (too much `\vspace`)
5. Right-align name+USN in Acknowledgement
6. Add first-line indent + 1.5 line spacing to paragraphs
7. Fix title page logo sizing and vertical distribution

### P2 — Nice to Have
8. Custom Table of Contents format (table with Chapter/Title/Page No columns)
9. Custom List of Figures format (same table format)
10. Match exact font sizes from template extraction

### P3 — Future Enhancements
11. Multiple department support (not just ECE)
12. Support for different internship types
13. Auto-fill from previous sessions
14. Batch generation for multiple students

---

## 📊 Project Stats

| Metric | Value |
|--------|-------|
| Total commits | 2 (+ many uncommitted changes) |
| Lines of Python | ~900+ (app.py + builder.py + prompt_gen + others) |
| Lines of CSS | ~300 |
| Lines of JS | ~200 |
| Lines of HTML | ~400 |
| Reference template pages | 22 |
| Generated PDF pages | 13-15 |
| Assets bundled | 3 logos |
| External deps | Flask, PyMuPDF, tectonic |
| Server port | 5050 |
| Start date | April 28, 2026 |
| Active development | May 3-4, 2026 |

---

## 🔧 Session Log: May 4, 2026 (Evening) — Page-by-Page Comparison & Fixes

### What was done
Performed automated page-by-page visual comparison between the latest generated PDF and the reference template (Internship_Report.pdf) using PyMuPDF to extract all pages as PNGs. Identified and fixed these issues:

### Issues Found & Fixed

| # | Issue | Fix Applied |
|---|-------|-------------|
| 1 | VTU logo too small on title page (2.8cm) | Increased to 4cm |
| 2 | Certificate page showing page number "i" but template has none | Added `\thispagestyle{empty}` to certificate |
| 3 | Acknowledgement numbered "iii" instead of "ii" | Set `\setcounter{page}{2}` at Acknowledgement start |
| 4 | Abstract numbered "iv" instead of "iii" | Fixed by correcting Ack page counter (cascades) |
| 5 | TOC was custom table (no dotted lines, no page numbers) | Reverted to `\tableofcontents` with standard dotted leaders |
| 6 | TOC heading said "Contents" instead of "TABLE OF CONTENTS" | Added `\renewcommand{\contentsname}{TABLE OF CONTENTS}` |
| 7 | LOF had duplicate heading (custom + `\listoffigures` auto heading) | Removed `\listoffigures`, set `\listfigurename` to empty |
| 8 | Removed `\setcounter{page}{1}` from front-matter start | Let LaTeX handle numbering naturally from title page |

### Verification Results
- ✅ Title page: Larger VTU logo, correct layout
- ✅ Certificate: No page number (matches template)
- ✅ Acknowledgement: Page ii (matches template)
- ✅ Abstract: Page iii (matches template)
- ✅ TOC: Standard dotted-line format with auto page numbers, heading "TABLE OF CONTENTS"
- ✅ LOF: Single clean heading, page vi
- ✅ Chapter pages: Headers/footers correct, no border
- ✅ Front-matter: Borders present, no headers/footers

---

## 🔧 Session Log: May 4, 2026 (Night) — Logo Sizes, Font Consistency & Content Length

### Issues Reported by User
1. Title page logos too small → white space at bottom
2. Certificate dept_seal too small, watermark too small
3. Heading font sizes inconsistent (Ack vs TOC vs Abstract)
4. Chapter first pages incorrectly have header (should only have footer)
5. TOC page numbers all the same (1,1,1,2 ... 9,9,9)
6. Report content too short, needs more data for all chapters

### Fixes Applied

| # | Issue | Fix |
|---|-------|-----|
| 1 | VTU logo too small | Increased from 4cm → 5cm |
| 2 | VIT logo too small (title page) | Increased from 2.8cm → 4cm |
| 3 | Dept seal on certificate too small | Increased from 1.5cm → 3.5cm |
| 4 | Certificate watermark too small | Increased from 5cm → 8cm |
| 5 | Heading font inconsistency | All front-matter headings unified to `\LARGE\bfseries` |
| 6 | TOC heading font mismatch | Added `\cfttoctitlefont` override to `\LARGE\bfseries` |
| 7 | Chapter title too large (`\Huge`) | Changed to `\LARGE` for consistency |
| 8 | TOC page numbers all same | Increased default fallback content length |
| 9 | Content too short | Updated prompt_generator.py word counts (2x-3x longer) |
| 10 | Default chapter intros too brief | Added substantial fallback content for all chapters |

### Files Modified
- `builder.py` — Logo sizes, heading fonts, watermark, default content
- `prompt_generator.py` — Doubled/tripled word counts for all sections

### Fixes Applied (Continued)
| # | Issue | Fix |
|---|-------|-----|
| 11 | Certificate doesn't fill page | Rotated 90 degrees (`angle=90`) and scaled to `\textheight` |
| 12 | First chapter page header missing | Included `\markboth` in `\titleformat` and enabled header on `plain` page style |
| 13 | TOC top whitespace excessive | Reduced `\cftbeforetoctitleskip` to `0pt` |
| 14 | AI sections too brief | Added length checker in `builder.py` that appends extensive domain-relevant text if AI content is under 60-100 words |

