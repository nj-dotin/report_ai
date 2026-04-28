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
