# Report Workflow Guide: Using MarkItDown + LaTeX MCP Server

## Overview
This guide shows how to use the MCP servers to go from a PDF or rough notes to a complete compiled LaTeX report.

## Step 1: Extract Content with MarkItDown
MarkItDown is already available from your user-level MCP config. Use it to convert any document into structured text.

### How to Use MarkItDown in Copilot
1. Open Copilot Chat in VS Code.
2. Mention your PDF, DOCX, or other document.
3. Ask Copilot to use MarkItDown to extract and convert the content.
4. Copy the extracted text.

### Example Prompt
```
Use MarkItDown to convert my Internship_Report.pdf into clean, structured markdown.
I need the chapters, sections, text, figure captions, and any lists preserved.
```

## Step 2: Create or Update a LaTeX File with the LaTeX MCP Server
Use the `latex-server` to generate, edit, or validate `.tex` files from the extracted content.

### Available LaTeX MCP Tools
- **create_latex_file**: Create a new `.tex` file with your content
- **edit_latex_file**: Edit an existing `.tex` file by replacing, inserting, or appending text
- **read_latex_file**: Read a `.tex` file to check its contents
- **validate_latex**: Check for syntax errors (balanced braces, environments, etc.)
- **compile_latex**: Compile `.tex` to PDF (requires pdflatex on PATH)
- **get_latex_structure**: Extract the document structure

### Example Prompt
```
Use the latex-server to create a new file called "report.tex" with document_type="report".
Include the content I just extracted with MarkItDown. Add proper LaTeX formatting.
```

## Step 3: Validate Before Compiling
Always validate the LaTeX before you try to compile it.

### Example Prompt
```
Use latex-server to validate report.tex for syntax errors.
Let me know if there are any issues with braces, environments, or references.
```

## Step 4: Compile to PDF
Once validated, compile the `.tex` file to a PDF.

### Example Prompt
```
Use latex-server to compile report.tex to PDF using pdflatex.
Let me know if there are any compilation errors.
```

## Step 5: Iterate
If there are issues, use the LaTeX MCP server to edit the file and fix them.

---

## Quick Workflow Summary
1. **Extract**: Use MarkItDown to get clean text from your PDF or document.
2. **Create/Edit**: Use LaTeX MCP server to build or update the `.tex` file.
3. **Validate**: Use LaTeX MCP server to check for syntax errors.
4. **Compile**: Use LaTeX MCP server to generate the PDF.
5. **Iterate**: Fix any issues and repeat.

## File Locations
- Workspace root: `F:\report_ai`
- LaTeX files go here: `F:\report_ai\*.tex`
- Your extracted reports: `F:\report_ai\*.md`
- MCP server code: `F:\report_ai\mcp-latex-server`

## Important Notes
- The LaTeX MCP server can only access files in `F:\report_ai` or subdirectories (base path).
- MarkItDown is available from your user VS Code MCP config (no workspace setup needed).
- Both servers are available in Copilot Chat once you mention them by name.
