# MCP Setup

## What Is Set Up
- `latex-server` is configured in [`.vscode/mcp.json`](.vscode/mcp.json).
- The server code is cloned in [`mcp-latex-server/`](mcp-latex-server).
- Its dependencies are installed in the current Python environment.
- `markitdown` is already available from the user-level VS Code MCP config.

## Easy Way To Use It
1. Open VS Code in this workspace.
2. Open Copilot Chat or the MCP tools view.
3. Use `markitdown` when you want to convert PDF, DOCX, or other documents into text.
4. Use `latex-server` when you want to create, read, edit, validate, or compile LaTeX files.

## Recommended Workflow For Your Reports
1. Use `markitdown` to extract text from PDFs or documents.
2. Put the extracted content into your report draft.
3. Use `latex-server` to generate or edit `.tex` files.
4. Validate the LaTeX before compiling.
5. Compile only after the structure looks correct.

## Notes
- `latex-server` works inside the workspace base path only.
- If you want PDF compilation, make sure a LaTeX distribution like MiKTeX or TeX Live is installed.
- `uv` is not required here because the server is running through the installed Python environment.
