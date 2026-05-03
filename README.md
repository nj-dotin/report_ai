# Report AI: Your MCP Setup for Overleaf + LaTeX Reports

Welcome! This workspace is set up to help you build college project and internship reports using LaTeX, with MCP servers for automation.

## 📋 Documentation Index

- [**WORKFLOW.md**](WORKFLOW.md) — Step-by-step guide for using MarkItDown + LaTeX MCP server
- [**QUICK_REFERENCE.md**](QUICK_REFERENCE.md) — Copy-paste prompts for Copilot Chat
- [**MCP_SETUP.md**](MCP_SETUP.md) — What is installed and how the MCP servers work
- [**INSTALL_MIKTEX.md**](INSTALL_MIKTEX.md) — How to install MiKTeX for PDF compilation
- [**plan.md**](plan.md) — Original project planning document

## 🎯 What You Have

1. **LaTeX MCP Server** (`mcp-latex-server/`)
   - Create, edit, read, validate, and compile `.tex` files
   - Configured in `.vscode/mcp.json`
   - Available in Copilot Chat

2. **MarkItDown** (from your user VS Code MCP config)
   - Extract text from PDFs, DOCX, and other documents
   - Convert to clean markdown
   - Available in Copilot Chat

3. **Sample Report Template** (`sample_report.tex`)
   - A minimal working LaTeX report structure
   - Use as a starting point for your actual report

4. **Extracted Internship Report** (`Internship_Report_latex.md`)
   - Full LaTeX source for the PDF you uploaded
   - Ready to use as reference or starting point

## 🚀 Quick Start

1. **Install MiKTeX** (optional but recommended for PDF compilation)
   - Follow [INSTALL_MIKTEX.md](INSTALL_MIKTEX.md)

2. **Open Copilot Chat in VS Code**
   - Mention your document or ask for help

3. **Use the prompts from [QUICK_REFERENCE.md](QUICK_REFERENCE.md)**
   - Copy-paste a prompt that matches your task
   - The MCP servers will handle the rest

4. **Follow the [WORKFLOW.md](WORKFLOW.md) guide**
   - Extract → Create → Validate → Compile

## 📁 File Structure

```
f:\report_ai/
├── .vscode/
│   └── mcp.json                      # Workspace MCP config (latex-server)
├── mcp-latex-server/                 # LaTeX MCP server code
├── Internship_Report.pdf             # Your original PDF
├── Internship_Report_latex.md         # Extracted LaTeX source
├── sample_report.tex                 # Sample LaTeX template
├── plan.md                           # Original project plan
├── WORKFLOW.md                       # Step-by-step workflow guide
├── QUICK_REFERENCE.md                # Copy-paste prompts
├── MCP_SETUP.md                      # MCP setup details
├── INSTALL_MIKTEX.md                 # MiKTeX installation guide
└── README.md                         # This file
```

## ❓ Common Questions

**Q: Do I need to manually run the MCP server?**  
A: No. Copilot Chat in VS Code handles starting and stopping it automatically.

**Q: Can I edit LaTeX files locally?**  
A: Yes! Edit locally in VS Code, or use the LaTeX MCP server tools for automated edits. Both work.

**Q: What if compilation fails?**  
A: Make sure MiKTeX is installed and `pdflatex` is on your PATH. Then try validating the `.tex` file first to catch syntax errors.

**Q: Can I use this with Overleaf?**  
A: Yes! Generate `.tex` files here, then upload to Overleaf. Or download from Overleaf, edit here, and upload again.

**Q: Do I need to know LaTeX?**  
A: Not really. The MCP server and templates handle most of the structure. Just focus on your content.

## 🎓 Next Steps

1. Check out [WORKFLOW.md](WORKFLOW.md) for the full walkthrough
2. Copy a prompt from [QUICK_REFERENCE.md](QUICK_REFERENCE.md) and paste it into Copilot Chat
3. Start with the `sample_report.tex` template or the extracted `Internship_Report_latex.md`
4. Build your report incrementally: create, validate, compile, iterate

---

Happy reporting! 🎉
