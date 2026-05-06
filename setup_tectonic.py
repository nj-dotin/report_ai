"""
setup_tectonic.py
Downloads tectonic.exe for Windows (self-contained LaTeX engine).
Run once: python setup_tectonic.py
"""
import os
import sys
import zipfile
import urllib.request

BIN_DIR     = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bin")
TECTONIC    = os.path.join(BIN_DIR, "tectonic.exe")
# Latest stable release
RELEASE_URL = "https://github.com/tectonic-typesetting/tectonic/releases/download/tectonic%400.15.0/tectonic-0.15.0-x86_64-pc-windows-msvc.zip"
ZIP_PATH    = os.path.join(BIN_DIR, "tectonic.zip")

def download_tectonic():
    if os.path.exists(TECTONIC):
        print(f"[OK] tectonic.exe already exists: {TECTONIC}")
        return True

    os.makedirs(BIN_DIR, exist_ok=True)
    print("[DL] Downloading tectonic (~10 MB)...")

    def progress(block, block_size, total):
        done = block * block_size
        pct  = min(100, done * 100 // total) if total > 0 else 0
        bar  = "#" * (pct // 5) + "." * (20 - pct // 5)
        print(f"\r  [{bar}] {pct}%  ({done//1024} KB / {total//1024} KB)", end="", flush=True)

    try:
        urllib.request.urlretrieve(RELEASE_URL, ZIP_PATH, reporthook=progress)
        print()
    except Exception as e:
        print(f"\n[ERR] Download failed: {e}")
        print("\nFallback: Install MiKTeX from: https://miktex.org/download")
        return False

    print("[EX] Extracting...")
    with zipfile.ZipFile(ZIP_PATH, "r") as z:
        z.extractall(BIN_DIR)
    os.remove(ZIP_PATH)

    if os.path.exists(TECTONIC):
        print(f"[OK] Tectonic ready: {TECTONIC}")
        return True
    else:
        # Maybe extracted with different name
        for f in os.listdir(BIN_DIR):
            if f.lower().endswith(".exe"):
                os.rename(os.path.join(BIN_DIR, f), TECTONIC)
                print(f"[OK] Tectonic ready: {TECTONIC}")
                return True
        print("[ERR] Could not find tectonic.exe after extraction.")
        return False

if __name__ == "__main__":
    ok = download_tectonic()
    if ok:
        import subprocess
        result = subprocess.run([TECTONIC, "--version"], capture_output=True, text=True)
        print(f"Version: {result.stdout.strip()}")
    sys.exit(0 if ok else 1)
