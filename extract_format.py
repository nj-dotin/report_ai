"""Extract ALL formatting details from both pages of the template PDF."""
import fitz
import json

doc = fitz.open(r'd:\Internship Report\report_ai\Internship_Report.pdf')

for page_num in range(min(2, len(doc))):
    page = doc[page_num]
    print("=" * 80)
    print(f"PAGE {page_num + 1}")
    print(f"Page size: {page.rect.width:.1f} x {page.rect.height:.1f} pts")
    print("=" * 80)

    blocks = page.get_text("dict")["blocks"]
    for b in blocks:
        if "lines" in b:
            for line in b["lines"]:
                # Combine spans in same line
                texts = []
                for span in line["spans"]:
                    text = span["text"].strip()
                    if text:
                        font = span["font"]
                        size = span["size"]
                        color = span["color"]
                        flags = span["flags"]
                        bold = "B" if flags & 16 else " "
                        italic = "I" if flags & 2 else " "
                        texts.append(f"{text}")
                combined = " ".join(texts)
                if combined.strip():
                    # Use first span's properties as representative
                    first_span = line["spans"][0]
                    font = first_span["font"]
                    size = first_span["size"]
                    color = first_span["color"]
                    flags = first_span["flags"]
                    bold = "BOLD" if flags & 16 else "    "
                    ox, oy = first_span["origin"]
                    bbox = line["bbox"]
                    line_w = bbox[2] - bbox[0]
                    page_w = page.rect.width
                    center_x = (bbox[0] + bbox[2]) / 2
                    # Determine alignment
                    if abs(center_x - page_w/2) < 20:
                        align = "CENTER"
                    elif bbox[0] < 100:
                        align = "LEFT  "
                    else:
                        align = "RIGHT "
                    print(f"  {size:5.1f}pt {bold} {align} #{color:06x} [{font:20s}] | {combined[:80]}")
        elif "image" in b:
            x0, y0, x1, y1 = b["bbox"]
            w = x1 - x0
            h = y1 - y0
            cx = (x0 + x1) / 2
            print(f"  [IMAGE] pos=({x0:.0f},{y0:.0f}) size={w:.0f}x{h:.0f}pt center_x={cx:.0f}")

    # Border details
    drawings = page.get_drawings()
    border_lines = [d for d in drawings if len(d.get("items",[])) == 1 and d["items"][0][0] == "l"]
    if border_lines:
        print(f"\n  BORDERS/LINES ({len(border_lines)} total):")
        for d in border_lines:
            r = d["rect"]
            w = d.get("width", 0)
            is_horiz = abs(r.y0 - r.y1) < 1
            is_vert = abs(r.x0 - r.x1) < 1
            kind = "H-LINE" if is_horiz else ("V-LINE" if is_vert else "OTHER")
            print(f"    {kind} from ({r.x0:.1f},{r.y0:.1f}) to ({r.x1:.1f},{r.y1:.1f}) width={w:.2f}pt")
    print()

# Extract and save images
print("=" * 80)
print("EXTRACTING IMAGES FROM PDF")
print("=" * 80)
import os
img_dir = r'd:\Internship Report\report_ai\generated\pdf_compare\extracted_images'
os.makedirs(img_dir, exist_ok=True)

for page_num in range(min(2, len(doc))):
    page = doc[page_num]
    imgs = page.get_images(full=True)
    for idx, img in enumerate(imgs):
        xref = img[0]
        w = img[2]
        h = img[3]
        pix = fitz.Pixmap(doc, xref)
        if pix.n > 4:
            pix = fitz.Pixmap(fitz.csRGB, pix)
        fn = f"page{page_num+1}_img{idx+1}_{w}x{h}.png"
        pix.save(os.path.join(img_dir, fn))
        print(f"  Page {page_num+1} Image {idx+1}: {w}x{h}px -> {fn}")

doc.close()
print("\nDone!")
