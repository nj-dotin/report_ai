# How to Install MiKTeX on Windows

MiKTeX is a free LaTeX distribution for Windows. You need it to compile `.tex` files to PDF using the LaTeX MCP server.

## Steps

1. Go to the official MiKTeX download page:
   - https://miktex.org/download

2. Download the "Net Installer" for Windows (64-bit is recommended).

3. Run the installer and follow the prompts:
   - Choose "Install for anyone who uses this computer" (recommended)
   - Accept the default install location
   - Choose "Preferred paper: A4" (or Letter, as needed)
   - Complete the installation

4. After install, add MiKTeX to your system PATH if the installer does not do it automatically:
   - Open Start Menu, search for "Environment Variables"
   - Edit the `Path` variable in your user or system variables
   - Add the path to the MiKTeX `miktex/bin/x64` folder (e.g., `C:\Program Files\MiKTeX\miktex\bin\x64`)

5. Open a new terminal and run:
   ```
   pdflatex --version
   ```
   If you see version info, it is installed correctly.

6. (Optional) Open MiKTeX Console and update all packages.

---

Once installed, you can use the LaTeX MCP server to compile `.tex` files to PDF from VS Code or any MCP client.
