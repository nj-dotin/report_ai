import os
import sys
import shutil
import subprocess

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from builder import generate_latex
from content_engine import generate_academic_content

# Sample data based on user's report.tex
data = {
    "name": "Keerthana C",
    "usn": "1VI21EC040",
    "department": "Electronics and Communication Engineering",
    "dept_short": "ECE",
    "degree": "Bachelor of Engineering",
    "academic_year": "2025-2026",
    "company_name": "DLithe",
    "internship_title": "Full Stack Web Development",
    "start_date": "15/01/2026",
    "end_date": "15/02/2026",
    "internal_supervisor": "Mr. Santhosh Kumar S",
    "external_supervisor": "Mr. Girish L",
    "hod": "Dr. Chandrashekar S M",
    "principal": "Dr. Vijayasimha Reddy B G",
    "year_e": "2026",
}

# Generate content using the engine
ai_content = generate_academic_content(data)
data["ai_content"] = ai_content

# Create temporary directory
test_dir = "d:/Internship Report/report_ai/test_blast1"
os.makedirs(test_dir, exist_ok=True)
img_dir = os.path.join(test_dir, "images")
os.makedirs(img_dir, exist_ok=True)

# Copy logos from assets
assets_dir = "d:/Internship Report/report_ai/assets"
for asset_fn in ["vtu_logo.png", "vit_logo.png", "dept_seal.png"]:
    src = os.path.join(assets_dir, asset_fn)
    if os.path.exists(src):
        shutil.copy2(src, os.path.join(img_dir, asset_fn))

# Generate LaTeX
tex_content = generate_latex(data)
tex_path = os.path.join(test_dir, "report.tex")
with open(tex_path, "w", encoding="utf-8") as f:
    f.write(tex_content)

# Run Tectonic
print("Compiling PDF with Tectonic...")
tectonic_exe = "d:/Internship Report/report_ai/bin/tectonic.exe"
try:
    result = subprocess.run(
        [tectonic_exe, "report.tex"],
        cwd=test_dir,
        capture_output=True,
        text=True,
        check=True
    )
    print("PDF generated successfully!")
    # Move to root as test_blast1.pdf
    pdf_src = os.path.join(test_dir, "report.pdf")
    pdf_dst = "d:/Internship Report/report_ai/test_blast1.pdf"
    shutil.copy2(pdf_src, pdf_dst)
    print(f"Copied to {pdf_dst}")
except subprocess.CalledProcessError as e:
    print("Error during compilation:")
    print(e.stderr)
except Exception as e:
    print(f"An error occurred: {e}")
