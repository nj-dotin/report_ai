"""
builder.py
Generates LaTeX source matching the exact VIT internship report template.
Compiled with tectonic (bin/tectonic.exe) - no MiKTeX needed.

Template spec (extracted from Internship_Report.pdf via PyMuPDF):
  Front-matter (Title → List of Figures):
    - Double border (inner 0.28pt, outer 0.56pt)
    - Roman numeral page numbers at bottom center
    - No headers/footers
  Main content (Chapter 1 → end):
    - NO border
    - Header: {Internship Title} left | {CHAPTER NAME} right, with hrule
    - Footer: Dept. of {dept}, Vemana IT | {year} | Page X of Y, with hrule
    - Arabic page numbers
  Colors: Date range in RED (#ff0000), department name in BLUE (#0000ff)
  Fonts:  Computer Modern (LaTeX default), 12pt base
"""

import re
import os

# --- LaTeX escaping --------------------------------------------------------

def latex_escape(text):
    if not text:
        return ""
    replacements = [
        ("\\", r"\textbackslash{}"),
        ("&",  r"\&"),
        ("%",  r"\%"),
        ("$",  r"\$"),
        ("#",  r"\#"),
        ("_",  r"\_"),
        ("{",  r"\{"),
        ("}",  r"\}"),
        ("~",  r"\textasciitilde{}"),
        ("^",  r"\textasciicircum{}"),
    ]
    for ch, rep in replacements:
        text = text.replace(ch, rep)
    return text

URL_RE = re.compile(r"https?://[^\s,)<>]+")

def protect_urls(text):
    r"""Wrap URLs in \url{} before escaping so they aren't broken."""
    parts = []
    last = 0
    for m in URL_RE.finditer(text):
        parts.append(latex_escape(text[last:m.start()]))
        parts.append(r"\url{" + m.group(0) + "}")
        last = m.end()
    parts.append(latex_escape(text[last:]))
    return "".join(parts)

# --- AI content parser -----------------------------------------------------

def parse_ai_content(ai_text):
    sections = {}
    pat = re.compile(r"===([A-Z0-9_]+)===\s*(.*?)(?====|$)", re.DOTALL)
    for m in pat.finditer(ai_text):
        sections[m.group(1).strip()] = m.group(2).strip()
    return sections

# --- Text to LaTeX conversion ----------------------------------------------

def text_to_latex(raw):
    """Convert plain AI text (with optional bullet points) to LaTeX paragraphs."""
    if not raw:
        return ""
    lines = raw.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    out, buf, in_list = [], [], False

    def flush():
        if buf:
            combined = " ".join(buf).strip()
            if combined:
                out.append("\n" + protect_urls(combined) + "\n")
            buf.clear()

    for line in lines:
        s = line.strip()
        is_bullet = (
            s.startswith(("- ", "* "))
            or (len(s) > 2 and s[0].isdigit() and s[1] in ".):")
        )
        if is_bullet:
            flush()
            if not in_list:
                out.append(r"\begin{itemize}[leftmargin=1.5em]")
                in_list = True
            item = re.sub(r"^[\-\*\d]+[\.\:\)\s]+", "", s).strip()
            out.append(r"    \item " + protect_urls(item))
        elif s == "":
            flush()
            if in_list:
                out.append(r"\end{itemize}")
                in_list = False
        else:
            buf.append(s)

    flush()
    if in_list:
        out.append(r"\end{itemize}")

    return "\n".join(out)

# --- Figure helper ---------------------------------------------------------

def fig(rel_path, caption, width=0.70):
    cap = latex_escape(caption)
    return f"""
\\begin{{figure}}[H]
\\centering
\\includegraphics[width={width}\\textwidth]{{{rel_path}}}
\\caption{{{cap}}}
\\end{{figure}}
"""

def chapter_figures(img_list):
    return "\n".join(
        fig(f"images/{i['filename']}", i.get("caption", "Figure"))
        for i in img_list if i.get("filename")
    )

# --- Variation openers for reframing ---------------------------------------

ACK_OPENERS = [
    "I sincerely thank Visvesvaraya Technological University (VTU) for providing me with the opportunity to undertake this internship as a part of the academic curriculum, which has contributed significantly to my learning and overall development.",
    "I extend my heartfelt gratitude to Visvesvaraya Technological University (VTU) for including this internship as part of the curriculum, giving me a valuable opportunity to apply my academic knowledge in a professional environment.",
    "I am immensely grateful to Visvesvaraya Technological University (VTU) for facilitating this internship program, which has been instrumental in bridging the gap between classroom learning and real-world application.",
    "I would like to begin by expressing my sincere thanks to Visvesvaraya Technological University (VTU) for this invaluable internship opportunity, which has greatly enriched my academic and professional journey.",
]

CONCLUSION_OPENERS = [
    "This chapter summarizes the overall internship experience, highlighting key outcomes, personal growth, and future directions.",
    "In this concluding chapter, the key takeaways, achievements, and future opportunities stemming from the internship are discussed.",
    "This chapter presents a comprehensive summary of the internship, the skills developed, and the path forward in the chosen domain.",
    "The following sections capture the essence of the internship journey, from its outcomes to the personal milestones achieved.",
]

# --- Chapter name mapping for headers --------------------------------------

CHAPTER_NAMES = {
    1: "INTRODUCTION",
    2: "ORGANISATION PROFILE",
    3: "WORK DONE / METHODOLOGY",
    4: "RESULTS AND DISCUSSION",
    5: "CONCLUSION",
}

# --- Main LaTeX generator ---------------------------------------------------

def generate_latex(data, combo_count=0):
    """
    Generate complete LaTeX source matching the VIT internship report template exactly.
    Includes: conditional borders (front-matter only), headers/footers (chapters only),
    correct logos, colors, examiner lines, watermark.
    """
    # Student
    name       = data.get("name", "Student Name")
    name_upper = name.upper()
    usn        = data.get("usn", "")
    department = data.get("department", "")
    degree     = data.get("degree", "Bachelor of Engineering")
    year       = data.get("academic_year", "2025-2026")

    # Internship
    company    = data.get("company_name", "Company")
    title      = data.get("internship_title", "Internship")
    start      = data.get("start_date", "")
    end        = data.get("end_date", "")
    duration   = f"{start} to {end}" if start and end else ""
    ext_sup    = data.get("external_supervisor", "")
    int_sup    = data.get("internal_supervisor", "")
    hod        = data.get("hod", "")
    principal  = "Dr. Vijayasimha Reddy B G"

    # Short department name for footer (e.g., "Electronics and Communication Engineering" -> "ECE")
    dept_short = data.get("dept_short", "ECE")

    # Files
    dept_logo_fn    = data.get("dept_logo_filename", "")
    company_logo_fn = data.get("company_logo_filename", "")
    cert_fn         = data.get("cert_image_filename", "")

    # Chapter images: list of {chapter, filename, caption}
    ch_raw = data.get("chapter_images", [])
    ch_map = {}
    for item in ch_raw:
        ch_map.setdefault(item.get("chapter", "ch1"), []).append(item)

    def ci(key):
        return chapter_figures(ch_map.get(key, []))

    # AI sections
    ai_raw = data.get("ai_content", "")
    sec    = parse_ai_content(ai_raw)

    # --- Content expansion: enhance short sections -------------------------
    # If a section is under the minimum word count, append expansion content.
    MIN_WORDS = {
        "CH1_EVOLUTION": 80, "CH1_TRENDS": 80,
        "CH2_VISION": 60, "CH2_PROGRAMS": 60, "CH2_IMPACT": 60, "CH2_VALUES": 60,
        "CH3_TOOLS": 80, "CH3_PROCESS": 80, "CH3_CASESTUDY": 100,
        "CH3_CHALLENGES": 60, "CH3_SOLUTIONS": 60,
        "CH4_OUTCOMES": 80, "CH4_LEARNING": 80, "CH4_ANALYSIS": 60,
        "CH5_SUMMARY": 80, "CH5_GROWTH": 60, "CH5_FUTURE": 60,
    }

    EXPANSIONS = {
        "CH1_EVOLUTION": f"\n\nThe evolution of practices in the field of {title} has been marked by significant advancements in technology and methodology. Early approaches relied heavily on manual processes and standalone systems. With the advent of the internet and cloud computing, the field shifted towards distributed systems and web-based solutions. Modern practices now emphasize automation, continuous integration, and agile development methodologies. The integration of artificial intelligence and machine learning has further transformed the landscape, enabling predictive analytics, intelligent automation, and data-driven decision making. These advancements have made it essential for professionals to continuously update their skills and adapt to emerging technologies.",
        "CH1_TRENDS": f"\n\nSeveral key trends are shaping the current landscape of {title}. Cloud-native development and microservices architecture have become standard practices for building scalable applications. DevOps practices and CI/CD pipelines have streamlined the software development lifecycle. The adoption of containerization technologies such as Docker and Kubernetes has revolutionized deployment strategies. Edge computing is gaining traction for applications requiring low-latency processing. Furthermore, the increasing emphasis on cybersecurity has led to the adoption of security-first development practices across organizations of all sizes.",
        "CH2_VISION": f"\n\nThe organization's vision extends to becoming a leading provider of technology solutions that drive innovation and create lasting value for clients and stakeholders. Their mission emphasizes the importance of continuous learning, practical skill development, and maintaining the highest standards of quality in all deliverables. This alignment between vision and daily practice creates a productive and growth-oriented work environment.",
        "CH2_PROGRAMS": f"\n\nThe organization offers a diverse range of programs and services that cater to various aspects of technology and engineering. These include structured internship programs for engineering students, professional training workshops, consulting services for technology implementation, and research and development initiatives. The programs are designed to bridge the gap between academic knowledge and industry requirements, ensuring that participants gain practical, applicable skills.",
        "CH2_IMPACT": f"\n\nThe organization has made a significant impact in the technology sector through its commitment to quality, innovation, and skill development. Key impact areas include training and mentoring hundreds of engineering students, developing solutions that improve operational efficiency for client organizations, contributing to open-source projects and knowledge sharing, and establishing partnerships with academic institutions. These efforts have positioned the organization as a trusted partner in the technology ecosystem.",
        "CH2_VALUES": f"\n\nThese core values are not merely stated principles but are actively embedded in the organization's daily operations, decision-making processes, and employee interactions. The commitment to these values creates a work culture that fosters creativity, encourages continuous improvement, and supports both individual and collective growth.",
        "CH3_TOOLS": f"\n\nEach tool was selected based on its suitability for the specific requirements of the project, its industry adoption, and its ability to integrate with other components in the technology stack. Understanding the strengths and limitations of each tool was an important part of the learning experience during the internship.",
        "CH3_PROCESS": f"\n\nThe methodology followed during the internship emphasized iterative development, regular code reviews, and continuous feedback. Each task began with a thorough understanding of requirements, followed by research and planning. Implementation was done in incremental steps, with testing at each stage to ensure quality. Documentation was maintained throughout the process to facilitate knowledge transfer and future reference. This structured approach helped in managing complexity and delivering reliable solutions.",
        "CH3_CASESTUDY": f"\n\nThe project provided valuable insights into the complete software development lifecycle, from requirements gathering and design to implementation, testing, and deployment. It demonstrated the importance of proper architecture planning, code organization, and testing strategies in building maintainable and scalable applications. The experience gained from this project has been instrumental in developing a comprehensive understanding of professional software development practices.",
        "CH3_CHALLENGES": f"\n\nAdditionally, managing time effectively across multiple concurrent tasks required developing strong organizational skills. Understanding and adapting to the company's coding standards and development workflow also presented an initial learning curve that required patience and systematic effort to overcome.",
        "CH3_SOLUTIONS": f"\n\nMoreover, establishing a habit of documenting learnings and maintaining detailed notes helped in retaining and applying knowledge across different tasks. Seeking regular feedback from supervisors and peers also proved invaluable in identifying areas for improvement and refining approaches.",
        "CH4_OUTCOMES": f"\n\nThese outcomes demonstrate the practical value of the internship in building real-world engineering competencies. The deliverables produced during the internship met professional quality standards and contributed meaningfully to the organization's objectives. The experience has established a strong foundation for future professional endeavors in the field.",
        "CH4_LEARNING": f"\n\nBeyond technical competencies, the internship fostered important professional skills such as effective communication, teamwork, time management, and adaptability. These soft skills are equally valuable in a professional engineering career and complement the technical knowledge gained during the internship period.",
        "CH4_ANALYSIS": f"\n\nOverall, the internship experience exceeded initial expectations in terms of the depth and breadth of learning opportunities provided. While certain areas could have benefited from more structured guidance, the hands-on approach proved highly effective in developing practical engineering skills. The experience has highlighted the importance of continuous learning and adaptability in the rapidly evolving technology landscape.",
        "CH5_SUMMARY": f"\n\nThe internship experience at {company} has been a transformative journey that has significantly enhanced both technical capabilities and professional outlook. The exposure to real-world engineering practices, combined with mentorship from experienced professionals, has provided a solid foundation for a career in technology and engineering.",
        "CH5_GROWTH": f"\n\nThe internship has instilled a growth mindset and a commitment to continuous learning. The experience of working in a professional environment has improved my ability to collaborate effectively, communicate technical concepts clearly, and approach complex problems with a structured methodology. These personal and professional developments will serve as valuable assets throughout my career.",
        "CH5_FUTURE": f"\n\nThe field continues to evolve rapidly, with emerging technologies creating new opportunities for innovation and specialization. The skills and knowledge gained during this internship provide a strong foundation for pursuing advanced studies, industry certifications, or specialized roles in technology companies. The internship has opened up multiple career pathways and has reinforced the commitment to lifelong learning in this dynamic field.",
    }

    for key, min_wc in MIN_WORDS.items():
        content = sec.get(key, "")
        if content and len(content.split()) < min_wc and key in EXPANSIONS:
            sec[key] = content + EXPANSIONS[key]

    def S(key, fallback=""):
        return text_to_latex(sec.get(key, fallback))

    vi = combo_count % len(ACK_OPENERS)

    # Escaped values
    E = latex_escape
    dept_e   = E(department)
    comp_e   = E(company)
    title_e  = E(title)
    dur_e    = E(duration)
    deg_e    = E(degree)
    year_e   = E(year)
    extsup_e = E(ext_sup)
    intsup_e = E(int_sup)
    hod_e    = E(hod)
    prin_e   = E(principal)
    name_e   = E(name)
    dept_short_e = E(dept_short)

    # Company logo figure block
    comp_logo_block = ""
    if company_logo_fn:
        comp_logo_block = fig(f"images/{company_logo_fn}", f"Internship Provider - {company} Logo", width=0.55)

    # Company certificate block — rotate image to landscape so it fills the page
    cert_block = ""
    if cert_fn:
        cert_block = f"""
\\newpage
\\begin{{center}}
\\vspace*{{\\fill}}
\\includegraphics[angle=90,origin=c,width=0.92\\textheight,height=0.92\\textwidth,keepaspectratio]{{images/{cert_fn}}}
\\vspace*{{\\fill}}
\\end{{center}}
"""

    # -- Acknowledgement text ------------------------------------------------
    ack_provided = sec.get("ACKNOWLEDGEMENT", "").strip()
    if ack_provided:
        ack_body = text_to_latex(ack_provided)
    else:
        ack_body = f"""{ACK_OPENERS[vi]}

I express my sincere gratitude to {prin_e}, Principal, Vemana Institute of Technology, Bengaluru, for providing the necessary infrastructure, encouragement, and support to successfully carry out the internship work.

I extend my heartfelt thanks to {hod_e}, Head of the Department, {dept_e}, Vemana Institute of Technology, for their constant guidance, motivation, and encouragement throughout the internship duration.

I would also like to thank Internal Supervisor {intsup_e}, External Supervisor {extsup_e}, and all Internship Coordinators for their cooperation, coordination, and support during the internship period.

I am thankful to all the teaching and non-teaching staff members of the Department of {dept_e} for their support and encouragement throughout the internship.

I also acknowledge the support of {comp_e} for providing structured learning resources and an environment that encouraged systematic understanding, practical application, and continuous improvement."""

    # -- Build custom TOC entries for the table format -----------------------
    # We'll build a manual TOC in a tabular environment matching the template
    # The template uses: Chapter | Title | Page No columns

    # Count total main-body pages (approximate for TOC page refs)
    # We'll use \label/\pageref for accurate numbering

    # =======================================================================
    # FULL LATEX DOCUMENT
    # =======================================================================
    tex = rf"""\documentclass[12pt,a4paper]{{report}}

\usepackage[margin=1in]{{geometry}}
\usepackage{{graphicx}}
\usepackage{{array}}
\usepackage{{booktabs}}
\usepackage{{float}}
\usepackage{{setspace}}
\usepackage{{titlesec}}
\usepackage{{tocloft}}
\usepackage{{enumitem}}
\usepackage{{hyperref}}
\usepackage{{xcolor}}
\usepackage{{url}}
\usepackage{{eso-pic}}
\usepackage{{tikz}}
\usepackage{{fancyhdr}}
\usepackage{{lastpage}}
\usepackage{{etoolbox}}

\hypersetup{{
    colorlinks=true,
    linkcolor=black,
    urlcolor=blue,
    pdftitle={{Internship Report}},
    pdfauthor={{{name_e}}}
}}

% -- Spacing ----------------------------------------------------------------
\setstretch{{1.5}}
\setlength{{\parindent}}{{1.5em}}
\setlength{{\parskip}}{{0.4em}}

% -- Chapter heading format -------------------------------------------------
\titleformat{{\chapter}}[display]
  {{\bfseries\Large}}
  {{\chaptername~\thechapter}}{{10pt}}{{\LARGE\markboth{{\MakeUppercase{{##1}}}}{{\MakeUppercase{{##1}}}}}}

% Ensure chapter marks are set for headers
\renewcommand{{\chaptermark}}[1]{{\markboth{{##1}}{{##1}}}}

% -- Rename TOC / LOF headings to match template ----------------------------
\renewcommand{{\contentsname}}{{TABLE OF CONTENTS}}
\renewcommand{{\listfigurename}}{{}}

% -- TOC heading format (consistent with other front-matter headings) -------
\renewcommand{{\cfttoctitlefont}}{{\hfill\LARGE\bfseries}}
\renewcommand{{\cftaftertoctitle}}{{\hfill}}
\renewcommand{{\cftloftitlefont}}{{\hfill\LARGE\bfseries}}
\renewcommand{{\cftafterloftitle}}{{\hfill}}
\setlength{{\cftbeforetoctitleskip}}{{0pt}}
\setlength{{\cftaftertoctitleskip}}{{1.5em}}

% -- Toggle: border ON/OFF --------------------------------------------------
% We define a boolean that controls whether borders are drawn.
% Front-matter pages: border ON.  Chapter pages: border OFF.
\newif\ifshowborder
\showbordertrue  % start with borders ON

\AddToShipoutPictureBG{{%
  \ifshowborder
  \begin{{tikzpicture}}[remember picture, overlay]
    \draw[line width=0.56pt]
      ([xshift=18pt, yshift=-18pt]current page.north west)
      rectangle
      ([xshift=-18pt, yshift=18pt]current page.south east);
    \draw[line width=0.28pt]
      ([xshift=20pt, yshift=-20pt]current page.north west)
      rectangle
      ([xshift=-20pt, yshift=20pt]current page.south east);
  \end{{tikzpicture}}%
  \fi
}}

% -- Page styles ------------------------------------------------------------

% Style for front-matter: no header/footer, just centered page number
\fancypagestyle{{frontmatter}}{{
  \fancyhf{{}}
  \renewcommand{{\headrulewidth}}{{0pt}}
  \renewcommand{{\footrulewidth}}{{0pt}}
  \fancyfoot[C]{{\thepage}}
}}

% Style for main content: header + footer, no border
\fancypagestyle{{mainchapter}}{{
  \fancyhf{{}}
  \renewcommand{{\headrulewidth}}{{0.4pt}}
  \renewcommand{{\footrulewidth}}{{0.4pt}}
  \fancyhead[L]{{\small {title_e}}}
  \fancyhead[R]{{\small\nouppercase{{\leftmark}}}}
  \fancyfoot[L]{{\small Dept. of {dept_short_e}, Vemana IT}}
  \fancyfoot[C]{{\small {year_e}}}
  \fancyfoot[R]{{\small Page \thepage\ of \pageref{{LastPage}}}}
}}

% Plain style for front-matter (used by \chapter*, \listoffigures, etc.)
% Initially just centered page number. Redefined before main content.
\fancypagestyle{{plain}}{{
  \fancyhf{{}}
  \renewcommand{{\headrulewidth}}{{0pt}}
  \renewcommand{{\footrulewidth}}{{0pt}}
  \fancyfoot[C]{{\thepage}}
}}

\begin{{document}}

% ==========================================================================
% TITLE PAGE  (single-spaced, zero parskip so it fits on one page)
% ==========================================================================
\begin{{titlepage}}
\thispagestyle{{empty}}
\begin{{singlespacing}}
\setlength{{\parskip}}{{0pt}}
\setlength{{\parindent}}{{0pt}}
\centering
\vspace*{{-0.5cm}}

{{\Large \textbf{{VISVESVARAYA TECHNOLOGICAL UNIVERSITY}}\par}}
\vspace{{2pt}}
{{\large \textbf{{Jnana Sangama, Belagavi -- 590018}}\par}}
\vspace{{8pt}}
\includegraphics[height=5cm]{{images/vtu_logo.png}}\par
\vspace{{8pt}}
{{\itshape An Internship Report\par}}
\vspace{{2pt}}
{{\itshape On\par}}
\vspace{{4pt}}
{{\LARGE \textbf{{\textquotedblleft {title_e}\textquotedblright}}\par}}
\vspace{{4pt}}
{{\textcolor{{red}}{{{dur_e}}}\par}}
\vspace{{8pt}}
{{\itshape Submitted in partial fulfillment of the requirements for the award of the degree of\par}}
\vspace{{4pt}}
{{\large \textbf{{{deg_e}}}\par}}
\vspace{{2pt}}
{{\large \textbf{{in}}\par}}
\vspace{{2pt}}
{{\large \textbf{{\textcolor{{blue}}{{{dept_e}}}}}\par}}
\vspace{{8pt}}
Submitted by\par
\vspace{{4pt}}
{{\large \textbf{{{name_upper} \hspace{{2cm}} {usn}}}\par}}
\vspace{{10pt}}
\includegraphics[height=4cm]{{images/vit_logo.png}}\par
\vspace{{10pt}}
{{\large \textbf{{DEPARTMENT OF {dept_e.upper()}}}\par}}
{{\Large \textbf{{VEMANA INSTITUTE OF TECHNOLOGY}}\par}}
{{\large BENGALURU -- 560034\par}}
\vspace{{6pt}}
{{\Large \textbf{{{year_e}}}\par}}

\end{{singlespacing}}
\end{{titlepage}}

% ==========================================================================
% FRONT MATTER — borders ON, roman numbering, no headers/footers
% ==========================================================================
\pagenumbering{{roman}}
\pagestyle{{frontmatter}}

% ==========================================================================
% CERTIFICATE PAGE
% ==========================================================================
\thispagestyle{{empty}}
\begin{{singlespacing}}
\setlength{{\parskip}}{{0pt}}
\setlength{{\parindent}}{{0pt}}
\begin{{center}}
{{\large \textbf{{Karnataka ReddyJana Sangha}}\par}}
\vspace{{2pt}}
{{\Large \textbf{{VEMANA INSTITUTE OF TECHNOLOGY}}\par}}
\vspace{{2pt}}
(Affiliated to Visvesvaraya Technological University, Belagavi)\par
Koramangala, Bengaluru--560034\par
\vspace{{8pt}}
\includegraphics[height=3.5cm]{{images/dept_seal.png}}\par
\vspace{{10pt}}
{{\large \textbf{{DEPARTMENT OF}}\par}}
{{\large \textbf{{{dept_e.upper()}}}\par}}
\vspace{{10pt}}
{{\LARGE \textbf{{CERTIFICATE}}\par}}
\end{{center}}
\end{{singlespacing}}

\vspace{{6pt}}
\setlength{{\parindent}}{{1.5em}}
This is to certify that the internship entitled \textbf{{\textquotedblleft {title_e}\textquotedblright}} is a bonafide work carried out by \textbf{{{name_upper} ({usn})}} in partial fulfilment of the requirements for the award of {deg_e} degree in \textbf{{{dept_e}}}, Visvesvaraya Technological University, Belagavi, during the academic year {year_e}.

It is certified that all corrections and suggestions indicated for internal assessment have been duly incorporated in the report. The internship report has been approved as it satisfies the academic requirements prescribed for the said degree.

% -- Watermark: VIT logo behind signatures ---------------------------------
\AddToShipoutPictureFG*{{%
  \begin{{tikzpicture}}[remember picture, overlay]
    \node[opacity=0.10] at ([yshift=-4cm]current page.center) {{%
      \includegraphics[height=8cm]{{images/vit_logo.png}}%
    }};
  \end{{tikzpicture}}%
}}

\vspace{{0.6cm}}
\begin{{center}}
\begin{{tabular}}{{p{{0.22\textwidth}} p{{0.22\textwidth}} p{{0.22\textwidth}} p{{0.22\textwidth}}}}
\textbf{{Internal Supervisor}} & \textbf{{External Supervisor}} & \textbf{{HOD}} & \textbf{{Principal}} \\
({intsup_e}) & ({extsup_e}) & ({hod_e}) & ({prin_e}) \\
\end{{tabular}}
\end{{center}}

\vspace{{0.5cm}}
\textbf{{Name of the Examiners}} \hfill \textbf{{Signature with Date}}\par
\vspace{{0.2cm}}
1.\enspace\rule{{5cm}}{{0.4pt}} \hfill \rule{{3.5cm}}{{0.4pt}}\par
\vspace{{0.4cm}}
2.\enspace\rule{{5cm}}{{0.4pt}} \hfill \rule{{3.5cm}}{{0.4pt}}\par

{cert_block}

% ==========================================================================
% ACKNOWLEDGEMENT
% ==========================================================================
\newpage
\setcounter{{page}}{{2}}  % Ack = page ii (certificate was empty)
\begin{{center}}
{{\LARGE \textbf{{ACKNOWLEDGEMENT}}\par}}
\end{{center}}
\addcontentsline{{toc}}{{chapter}}{{Acknowledgement}}

\vspace{{0.5cm}}
\setlength{{\parindent}}{{1.5em}}
\begin{{onehalfspacing}}
{ack_body}
\end{{onehalfspacing}}

\vspace{{1cm}}
\begin{{flushright}}
\textbf{{{name_e}}}\par
{usn}\par
\end{{flushright}}

% ==========================================================================
% ABSTRACT
% ==========================================================================
\newpage
\begin{{center}}
{{\LARGE \textbf{{ABSTRACT}}\par}}
\end{{center}}
\addcontentsline{{toc}}{{chapter}}{{Abstract}}

\vspace{{0.5cm}}
\setlength{{\parindent}}{{1.5em}}
{S("ABSTRACT", "Abstract not provided.")}

% ==========================================================================
% TABLE OF CONTENTS — Standard LaTeX TOC with dotted leaders
% ==========================================================================
\newpage
\tableofcontents

% ==========================================================================
% LIST OF FIGURES — Custom table format matching template
% ==========================================================================
\newpage
\begin{{center}}
{{\LARGE \textbf{{LIST OF FIGURES}}\par}}
\end{{center}}
\addcontentsline{{toc}}{{chapter}}{{List of Figures}}

\vspace{{0.3cm}}
\begin{{tabular}}{{@{{}} p{{2cm}} p{{10cm}} r @{{}}}}
\textbf{{Figure No}} & \textbf{{Title}} & \textbf{{Page No}} \\
\midrule
\end{{tabular}}

% ==========================================================================
% MAIN CONTENT — borders OFF, headers/footers ON, arabic numbering
% ==========================================================================
\newpage
\showborderfalse       % TURN OFF borders for all remaining pages
\pagenumbering{{arabic}}

% Redefine plain style for chapter first pages — SAME as mainchapter
% Template shows header + footer on ALL chapter pages including the first page
\fancypagestyle{{plain}}{{
  \fancyhf{{}}
  \renewcommand{{\headrulewidth}}{{0.4pt}}
  \renewcommand{{\footrulewidth}}{{0.4pt}}
  \fancyhead[L]{{\small {title_e}}}
  \fancyhead[R]{{\small\nouppercase{{\leftmark}}}}
  \fancyfoot[L]{{\small Dept. of {dept_short_e}, Vemana IT}}
  \fancyfoot[C]{{\small {year_e}}}
  \fancyfoot[R]{{\small Page \thepage\ of \pageref{{LastPage}}}}
}}
\pagestyle{{mainchapter}}

% ==========================================================================
% CHAPTER 1: INTRODUCTION
% ==========================================================================
\chapter{{INTRODUCTION}}
\label{{ch:intro}}

{S("CH1_INTRO", f"This chapter provides an introduction to my internship experience at {comp_e} in the role of {title_e}. It outlines the objectives, scope, and relevance of the internship in relation to my academic background in {dept_e}. The chapter also discusses the evolution of technologies and current trends related to the work carried out during the internship period. Internships play a crucial role in bridging the gap between theoretical knowledge gained in the classroom and practical skills required in the industry. This internship provided me with a unique opportunity to apply my engineering knowledge in a real-world professional environment, working alongside experienced professionals and contributing to meaningful projects.")}

\section{{Internship Scope and Objectives}}
{S("CH1_SCOPE")}

\section{{Relevance of {title_e} to {dept_e}}}
{S("CH1_RELEVANCE")}

\section{{Evolution of Practices in the Field}}
{S("CH1_EVOLUTION")}

\section{{Current Trends and Technologies}}
{S("CH1_TRENDS")}

{ci("ch1")}

% ==========================================================================
% CHAPTER 2: ORGANISATION PROFILE
% ==========================================================================
\chapter{{ORGANISATION PROFILE}}
\label{{ch:org}}

{S("CH2_INTRO", f"In addition to answering questions like when and where the internship was completed, this chapter gives a comprehensive overview of {comp_e} and concentrates on its history, founding vision, organizational structure, services offered, and overall impact in the industry. Understanding the organization where the internship was carried out is essential as it provides context for the work done and helps in appreciating the learning environment that contributed to the overall internship experience.")}

\section{{Introduction}}
{S("CH2_ORG_INTRO", f"{comp_e} is a leading organization that provides structured learning, training, and internship programs to engineering students and professionals across multiple domains. The organization has established itself as a reputable entity in the technology sector, known for fostering innovation, supporting skill development, and contributing to the growth of the engineering workforce. With a commitment to practical education and industry-aligned training, the organization has been instrumental in shaping the careers of numerous students and professionals.")}

{comp_logo_block}

\section{{Vision and Mission of the Organization}}
{S("CH2_VISION")}

\section{{Programs and Services Offered}}
{S("CH2_PROGRAMS")}

\section{{Organizational Impact and Reach}}
{S("CH2_IMPACT")}

\section{{Core Values}}
{S("CH2_VALUES")}

{ci("ch2")}

% ==========================================================================
% CHAPTER 3: WORK DONE / METHODOLOGY
% ==========================================================================
\chapter{{WORK DONE / METHODOLOGY}}
\label{{ch:work}}

{S("CH3_OVERVIEW", "The work completed during the internship and the methodology used are presented in this chapter. This chapter provides a detailed account of the day-to-day activities, the tools and technologies employed, the work process followed, and the key projects undertaken. It also discusses the challenges encountered during the internship and the solutions implemented to overcome them. The chapter aims to give a comprehensive understanding of the practical work experience gained during the internship period.")}

\section{{Overview of Internship Work}}
{S("CH3_WORK_OVERVIEW")}

\section{{Tools and Technologies Used}}
{S("CH3_TOOLS")}

{ci("ch3")}

\section{{Work Process and Methodology}}
{S("CH3_PROCESS")}

\section{{Key Project and Case Study}}
{S("CH3_CASESTUDY")}

{ci("ch3_extra")}

\section{{Challenges Faced}}
{S("CH3_CHALLENGES")}

\section{{Solutions Implemented}}
{S("CH3_SOLUTIONS")}

% ==========================================================================
% CHAPTER 4: RESULTS AND DISCUSSION
% ==========================================================================
\chapter{{RESULTS AND DISCUSSION}}
\label{{ch:results}}

{S("CH4_INTRO", "The work that was evaluated and examined during the internship is included in this chapter. This chapter presents a thorough analysis of the outcomes achieved, the learning acquired, and the overall effectiveness of the internship experience. It evaluates the deliverables produced, the skills developed, and provides a critical analysis of the entire internship journey, highlighting both the successes and areas for improvement.")}

{ci("ch4")}

\section{{Outcomes of the Work}}
{S("CH4_OUTCOMES")}

\section{{Learning Outcomes}}
{S("CH4_LEARNING")}

\section{{Analysis}}
{S("CH4_ANALYSIS")}

{ci("ch4_extra")}

% ==========================================================================
% CHAPTER 5: CONCLUSION
% ==========================================================================
\chapter{{CONCLUSION}}
\label{{ch:conclusion}}

{S("CH5_INTRO", CONCLUSION_OPENERS[vi])}

{ci("ch5")}

\section{{Summary}}
{S("CH5_SUMMARY")}

\section{{Personal Growth}}
{S("CH5_GROWTH")}

\section{{Future Scope}}
{S("CH5_FUTURE")}

\end{{document}}
"""
    return tex
