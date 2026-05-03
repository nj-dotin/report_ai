# MCP Quick Reference: MarkItDown + LaTeX Server

## 🚀 Quick Prompts for Copilot Chat

### Extract a Document (MarkItDown)
```
Use MarkItDown to convert [FILENAME] to clean markdown.
Preserve all structure: chapters, sections, text, lists, captions.
```

### Create a New LaTeX File
```
Use latex-server to create a new file called [FILENAME].tex with:
- document_type: report
- title: [YOUR TITLE]
- author: [YOUR NAME]
- content: [PASTE YOUR TEXT HERE]
- packages: [graphicx, hyperref, booktabs]
```

### Read a LaTeX File
```
Use latex-server to read [FILENAME].tex and show me the current contents.
```

### Edit a LaTeX File (Replace Text)
```
Use latex-server to edit [FILENAME].tex:
- Operation: replace
- Search for: [OLD TEXT]
- Replace with: [NEW TEXT]
```

### Edit a LaTeX File (Insert Before)
```
Use latex-server to edit [FILENAME].tex:
- Operation: insert_before
- Search for: [ANCHOR TEXT]
- New text: [YOUR NEW TEXT]
```

### Edit a LaTeX File (Append)
```
Use latex-server to edit [FILENAME].tex:
- Operation: append
- New text: [YOUR TEXT TO ADD AT END]
```

### Validate LaTeX Syntax
```
Use latex-server to validate [FILENAME].tex for syntax errors.
Check for: balanced braces, matching environments, undefined references.
```

### Get LaTeX Document Structure
```
Use latex-server to get the structure of [FILENAME].tex.
Show me: document class, title, author, packages, section hierarchy.
```

### Compile to PDF
```
Use latex-server to compile [FILENAME].tex to PDF using pdflatex.
Save as: [FILENAME].pdf
```

### List All .tex Files
```
Use latex-server to list all .tex files in the current workspace.
```

---

## 🎯 Common Workflows

### Workflow 1: PDF → LaTeX → PDF
1. Extract PDF with MarkItDown
2. Create `.tex` file with LaTeX server
3. Validate with LaTeX server
4. Compile to PDF with LaTeX server

### Workflow 2: Quick Edit Cycle
1. Read the `.tex` file
2. Edit it with LaTeX server
3. Validate
4. Compile

### Workflow 3: Multi-Chapter Report
1. Create main `.tex` file with `\input{chapter1.tex}` references
2. Create individual chapter files
3. Edit each chapter separately
4. Validate the main file
5. Compile the main file to generate full PDF

---

## 📝 File Operations via Copilot Chat

You can also ask Copilot directly to:
- Read a file: `Read report.tex`
- Show file structure: `Show the structure of report.tex`
- Validate syntax: `Validate report.tex`
- Compile: `Compile report.tex`

All will use the LaTeX MCP server automatically if you mention the filename and the action.

---

## ⚠️ Limits

- LaTeX files must be in `F:\report_ai` or subdirectories
- Compilation requires `pdflatex` on PATH (install MiKTeX if needed)
- MarkItDown works on any document type (PDF, DOCX, etc.)
