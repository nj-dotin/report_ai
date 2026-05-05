import os
import uuid
import json
import shutil
import subprocess
from flask import Flask, request, render_template, send_file, jsonify
from builder import generate_latex
from prompt_generator import generate_prompt

app = Flask(__name__)
app.secret_key = "report_ai_vit_2025"

BASE_DIR     = os.path.dirname(os.path.abspath(__file__))
UPLOADS_DIR  = os.path.join(BASE_DIR, "uploads")
GEN_DIR      = os.path.join(BASE_DIR, "generated")
TRACKER      = os.path.join(BASE_DIR, "combo_tracker.json")
TECTONIC_EXE = os.path.join(BASE_DIR, "bin", "tectonic.exe")
ASSETS_DIR   = os.path.join(BASE_DIR, "assets")   # Bundled logos (VTU, VIT, dept seal)

os.makedirs(UPLOADS_DIR, exist_ok=True)
os.makedirs(GEN_DIR, exist_ok=True)

# ─── Combo tracker ────────────────────────────────────────────────────────────

def get_combo_count(company, department):
    try:
        with open(TRACKER) as f:
            data = json.load(f)
    except Exception:
        data = {}
    return data.get(f"{company.lower().strip()}|{department.lower().strip()}", 0)

def increment_combo(company, department):
    try:
        with open(TRACKER) as f:
            data = json.load(f)
    except Exception:
        data = {}
    key = f"{company.lower().strip()}|{department.lower().strip()}"
    data[key] = data.get(key, 0) + 1
    with open(TRACKER, "w") as f:
        json.dump(data, f, indent=2)

# ─── PDF compilation via tectonic ────────────────────────────────────────────

def compile_pdf(tex_path, out_dir):
    """
    Compile .tex to PDF using tectonic.
    Returns True if report.pdf is produced.
    """
    exe = TECTONIC_EXE if os.path.exists(TECTONIC_EXE) else "tectonic"
    try:
        cmd = [
            exe,
            "--outdir", out_dir,
            "--keep-logs",           # keep tectonic.log for debugging
            "--print",               # print log to stdout
            tex_path,
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=180,
                                cwd=out_dir)
        print("[tectonic stdout]", result.stdout[-1000:] if result.stdout else "")
        print("[tectonic stderr]", result.stderr[-1000:] if result.stderr else "")
        pdf = os.path.join(out_dir, "report.pdf")
        return os.path.exists(pdf)
    except Exception as e:
        print(f"[compile_pdf error] {e}")
        return False

# ─── Routes ───────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/generate-prompt", methods=["POST"])
def api_generate_prompt():
    data = request.get_json(force=True)
    prompt = generate_prompt(data)
    return jsonify({"prompt": prompt})

from content_engine import generate_academic_content

@app.route("/api/auto-generate", methods=["POST"])
def api_auto_generate():
    data = request.get_json(force=True)
    auto_text = generate_academic_content(data)
    return jsonify({"ai_content": auto_text})

@app.route("/api/upload", methods=["POST"])
def api_upload():
    session_id = request.form.get("session_id") or str(uuid.uuid4())
    file_type  = request.form.get("file_type", "file")
    chapter    = request.form.get("chapter", "")
    caption    = request.form.get("caption", "Image")

    session_dir = os.path.join(UPLOADS_DIR, session_id)
    os.makedirs(session_dir, exist_ok=True)

    file = request.files.get("file")
    if not file or not file.filename:
        return jsonify({"error": "No file"}), 400

    ext     = os.path.splitext(file.filename)[1].lower()
    safe_fn = f"{file_type}_{uuid.uuid4().hex[:8]}{ext}"
    file.save(os.path.join(session_dir, safe_fn))

    return jsonify({
        "session_id": session_id,
        "filename":   safe_fn,
        "file_type":  file_type,
        "chapter":    chapter,
        "caption":    caption,
    })

@app.route("/api/generate-report", methods=["POST"])
def api_generate_report():
    data       = request.get_json(force=True)
    session_id = data.get("session_id") or str(uuid.uuid4())

    src_dir = os.path.join(UPLOADS_DIR, session_id)
    out_dir = os.path.join(GEN_DIR, session_id)
    img_dir = os.path.join(out_dir, "images")
    os.makedirs(img_dir, exist_ok=True)

    # Copy uploaded files → images/
    file_map = {}
    if os.path.exists(src_dir):
        for fn in os.listdir(src_dir):
            shutil.copy2(os.path.join(src_dir, fn), os.path.join(img_dir, fn))
            file_map[fn] = fn

    # Copy bundled assets (VTU logo, VIT logo, dept seal) → images/
    if os.path.exists(ASSETS_DIR):
        for asset_fn in ["vtu_logo.png", "vit_logo.png", "dept_seal.png"]:
            asset_path = os.path.join(ASSETS_DIR, asset_fn)
            if os.path.exists(asset_path):
                shutil.copy2(asset_path, os.path.join(img_dir, asset_fn))

    # Validate chapter images (keep only successfully uploaded ones)
    valid_ch_imgs = []
    for item in data.get("chapter_images", []):
        fn = item.get("filename", "")
        if fn and fn in file_map:
            valid_ch_imgs.append({
                "chapter":  item.get("chapter", "ch1"),
                "filename": fn,
                "caption":  item.get("caption", "Figure"),
            })
    data["chapter_images"] = valid_ch_imgs

    # Combo count for reframing
    combo_count = get_combo_count(
        data.get("company_name", ""),
        data.get("department", "")
    )

    # Generate .tex
    tex = generate_latex(data, combo_count)
    tex_path = os.path.join(out_dir, "report.tex")
    with open(tex_path, "w", encoding="utf-8") as f:
        f.write(tex)

    increment_combo(data.get("company_name", ""), data.get("department", ""))

    # Compile PDF with tectonic
    pdf_ok = compile_pdf(tex_path, out_dir)

    result = {
        "success": True,
        "tex_url": f"/download/{session_id}/report.tex",
    }
    if pdf_ok:
        result["pdf_url"] = f"/download/{session_id}/report.pdf"

    return jsonify(result)

@app.route("/download/<session_id>/<filename>")
def download(session_id, filename):
    path = os.path.join(GEN_DIR, session_id, filename)
    if not os.path.exists(path):
        return "File not found", 404
    return send_file(path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True, port=5050, use_reloader=False)
