/* app.js — Internship Report Generator */

// ── State ──────────────────────────────────────────────────────────────────
const state = {
  currentStep: 1,
  sessionId: null,
  uploads: {}, // key: file_type -> filename
  chapterImages: [], // [{chapter, filename, caption}]
};

const CHAPTERS = [
  { key: "ch1",       label: "Chapter 1: Introduction" },
  { key: "ch2",       label: "Chapter 2: Organisation Profile" },
  { key: "ch3",       label: "Chapter 3: Work Done / Methodology" },
  { key: "ch3_extra", label: "Chapter 3: Extra (Challenges & Solutions)" },
  { key: "ch4",       label: "Chapter 4: Results and Discussion" },
  { key: "ch4_extra", label: "Chapter 4: Extra" },
  { key: "ch5",       label: "Chapter 5: Conclusion" },
];

// ── Navigation ─────────────────────────────────────────────────────────────
function goStep(n) {
  if (!validateStep(state.currentStep)) return;

  document.querySelectorAll(".card").forEach(c => c.classList.remove("active"));
  document.querySelectorAll(".step").forEach(s => {
    const sn = parseInt(s.dataset.step);
    s.classList.remove("active", "done");
    if (sn < n) s.classList.add("done");
    if (sn === n) s.classList.add("active");
  });
  document.getElementById(`step${n}`).classList.add("active");
  document.getElementById(`step${n}`).scrollIntoView({ behavior: "smooth", block: "start" });
  state.currentStep = n;

  if (n === 5) buildChapterImageSections();
  if (n === 6) buildReviewSummary();
}

// ── Validation ─────────────────────────────────────────────────────────────
function validateStep(n) {
  const required = {
    1: ["name","usn","department","internal_supervisor","hod"],
    2: ["internship_title","company_name","start_date","end_date"],
  };
  if (required[n]) {
    for (const id of required[n]) {
      const el = document.getElementById(id);
      if (el && !el.value.trim()) {
        el.style.borderColor = "#ff5252";
        el.focus();
        setTimeout(() => el.style.borderColor = "", 2000);
        return false;
      }
    }
  }
  return true;
}

function val(id) {
  const el = document.getElementById(id);
  return el ? el.value.trim() : "";
}

function collectFormData() {
  return {
    name:               val("name"),
    usn:                val("usn"),
    department:         val("department"),
    degree:             val("degree"),
    academic_year:      val("academic_year"),
    internal_supervisor:val("internal_supervisor"),
    hod:                val("hod"),
    internship_title:   val("internship_title"),
    company_name:       val("company_name"),
    external_supervisor:val("external_supervisor"),
    start_date:         val("start_date"),
    end_date:           val("end_date"),
    company_summary:    val("company_summary"),
  };
}

// ── File Upload ────────────────────────────────────────────────────────────
async function handleUpload(input, fileType, boxSuffix) {
  const file = input.files[0];
  if (!file) return;

  const formData = new FormData();
  formData.append("file", file);
  formData.append("file_type", fileType);
  if (state.sessionId) formData.append("session_id", state.sessionId);

  const statusEl = document.getElementById(`${boxSuffix}_status`);
  statusEl.textContent = "Uploading...";

  try {
    const res = await fetch("/api/upload", { method: "POST", body: formData });
    const data = await res.json();
    if (data.error) { statusEl.textContent = "❌ Upload failed"; return; }

    state.sessionId = data.session_id;
    state.uploads[fileType] = data.filename;

    statusEl.textContent = `✅ ${file.name}`;
    const box = document.getElementById(`upload_${boxSuffix}`);
    if (box) box.classList.add("uploaded");
  } catch (e) {
    statusEl.textContent = "❌ Upload failed";
  }
}

// ── Generate AI Prompt ─────────────────────────────────────────────────────
async function generateAndShowPrompt() {
  const formData = collectFormData();
  document.getElementById("ai_prompt_display").value = "Generating prompt...";
  goStep(4);

  try {
    const res = await fetch("/api/generate-prompt", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(formData),
    });
    const data = await res.json();
    document.getElementById("ai_prompt_display").value = data.prompt || "Error generating prompt.";
  } catch (e) {
    document.getElementById("ai_prompt_display").value = "Error: Could not generate prompt.";
  }
}

function copyPrompt() {
  const ta = document.getElementById("ai_prompt_display");
  ta.select();
  document.execCommand("copy");
  const btn = document.getElementById("copyPromptBtn");
  btn.textContent = "✅ Copied!";
  setTimeout(() => btn.textContent = "Copy Prompt", 2500);
}

// ── Chapter Image Sections ─────────────────────────────────────────────────
function buildChapterImageSections() {
  const container = document.getElementById("chapter-image-sections");
  container.innerHTML = "";

  CHAPTERS.forEach(ch => {
    const section = document.createElement("div");
    section.className = "ch-section";
    section.innerHTML = `
      <div class="ch-section-title">📁 ${ch.label}</div>
      <div class="img-upload-list" id="list_${ch.key}"></div>
      <button class="add-img-btn" onclick="addImageRow('${ch.key}')">+ Add Image</button>
    `;
    container.appendChild(section);
  });
}

function addImageRow(chKey) {
  const list = document.getElementById(`list_${chKey}`);
  const count = list.querySelectorAll(".img-upload-row").length;
  if (count >= 6) { alert("Maximum 6 images per chapter."); return; }

  const rowId = `row_${chKey}_${Date.now()}`;
  const row = document.createElement("div");
  row.className = "img-upload-row";
  row.id = rowId;
  row.innerHTML = `
    <input type="file" accept="image/*" style="display:none" id="file_${rowId}" onchange="uploadChapterImage(this,'${chKey}','${rowId}')"/>
    <button class="btn-sm" onclick="document.getElementById('file_${rowId}').click()">📎 Choose</button>
    <span class="file-label" id="label_${rowId}">No file chosen</span>
    <input type="text" placeholder="Caption / Figure title" id="caption_${rowId}" style="flex:1"/>
    <button class="remove-btn" onclick="removeImageRow('${rowId}')">✕</button>
  `;
  list.appendChild(row);
}

async function uploadChapterImage(input, chKey, rowId) {
  const file = input.files[0];
  if (!file) return;

  const caption = document.getElementById(`caption_${rowId}`).value || "Image";
  const labelEl = document.getElementById(`label_${rowId}`);
  labelEl.textContent = "Uploading...";

  const formData = new FormData();
  formData.append("file", file);
  formData.append("file_type", `ch_img`);
  formData.append("chapter", chKey);
  formData.append("caption", caption);
  if (state.sessionId) formData.append("session_id", state.sessionId);

  try {
    const res = await fetch("/api/upload", { method: "POST", body: formData });
    const data = await res.json();
    if (data.error) { labelEl.textContent = "❌ Failed"; return; }

    state.sessionId = data.session_id;
    labelEl.textContent = `✅ ${file.name}`;

    // Store mapping so we can send it in the final generate call
    const existingIdx = state.chapterImages.findIndex(x => x.rowId === rowId);
    const entry = { rowId, chapter: chKey, filename: data.filename, caption };
    if (existingIdx >= 0) state.chapterImages[existingIdx] = entry;
    else state.chapterImages.push(entry);
  } catch (e) {
    labelEl.textContent = "❌ Upload failed";
  }
}

function removeImageRow(rowId) {
  document.getElementById(rowId)?.remove();
  state.chapterImages = state.chapterImages.filter(x => x.rowId !== rowId);
}

// ── Review Summary ─────────────────────────────────────────────────────────
function buildReviewSummary() {
  const d = collectFormData();
  const imgCount = state.chapterImages.length;
  const aiPasted = val("ai_content").length > 100;

  const rows = [
    ["Student",      `${d.name} / ${d.usn}`],
    ["Department",   d.department],
    ["Internship",   d.internship_title],
    ["Company",      d.company_name],
    ["Duration",     `${d.start_date} → ${d.end_date}`],
    ["Supervisors",  `Internal: ${d.internal_supervisor} | HOD: ${d.hod}`],
    ["Files uploaded", Object.keys(state.uploads).length + " file(s)"],
    ["Chapter images", `${imgCount} image(s)`],
    ["AI content",   aiPasted ? "✅ Provided" : "⚠️ Not pasted yet"],
  ];

  document.getElementById("review-summary").innerHTML = rows
    .map(([k, v]) => `<div class="rv"><span class="rv-key">${k}</span><span class="rv-val">${v}</span></div>`)
    .join("");
}

// ── Generate Report ────────────────────────────────────────────────────────
async function generateReport() {
  const aiContent = val("ai_content");
  if (!aiContent || aiContent.length < 50) {
    alert("Please paste the AI-generated content in Step 4 before generating.");
    return;
  }

  // Sync captions for already-uploaded images
  state.chapterImages.forEach(item => {
    const capEl = document.getElementById(`caption_${item.rowId}`);
    if (capEl) item.caption = capEl.value || item.caption;
  });

  document.getElementById("gen-idle").classList.add("hidden");
  document.getElementById("gen-loading").classList.remove("hidden");

  const payload = {
    ...collectFormData(),
    session_id:             state.sessionId,
    ai_content:             aiContent,
    dept_logo_filename:     state.uploads["dept_logo"]    || "",
    company_logo_filename:  state.uploads["company_logo"] || "",
    cert_image_filename:    state.uploads["cert_image"]   || "",
    chapter_images:         state.chapterImages,
  };

  try {
    const res = await fetch("/api/generate-report", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    const data = await res.json();

    document.getElementById("gen-loading").classList.add("hidden");
    document.getElementById("gen-done").classList.remove("hidden");

    document.getElementById("dl-tex").href = data.tex_url;
    if (data.pdf_url) {
      document.getElementById("dl-pdf").href = data.pdf_url;
      document.getElementById("dl-pdf").classList.remove("hidden");
    } else {
      document.getElementById("no-pdf-msg").classList.remove("hidden");
    }
  } catch (e) {
    document.getElementById("gen-loading").classList.add("hidden");
    document.getElementById("gen-idle").classList.remove("hidden");
    alert("Error generating report. Please check the server.");
  }
}

// ── Reset ──────────────────────────────────────────────────────────────────
function resetAll() {
  location.reload();
}
