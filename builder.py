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

def fig(rel_path, caption, width=0.45):
    cap = latex_escape(caption)
    return f"""
\\begin{{figure}}[H]
\\centering
\\includegraphics[width={width}\\textwidth,height=5cm,keepaspectratio]{{{rel_path}}}
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
        "CH1_EVOLUTION": 250, "CH1_TRENDS": 250,
        "CH2_VISION": 250, "CH2_PROGRAMS": 250, "CH2_IMPACT": 250, "CH2_VALUES": 250,
        "CH3_TOOLS": 250, "CH3_PROCESS": 250, "CH3_CASESTUDY": 250,
        "CH3_CHALLENGES": 250, "CH3_SOLUTIONS": 250,
        "CH4_OUTCOMES": 250, "CH4_LEARNING": 250, "CH4_ANALYSIS": 250,
        "CH5_SUMMARY": 250, "CH5_GROWTH": 250, "CH5_FUTURE": 250,
    }

    EXPANSIONS = {
        "CH1_EVOLUTION": f"\n\nThe evolution of practices in the field of {title} has been marked by significant advancements in technology and methodology. Early approaches relied heavily on manual processes and standalone systems. With the advent of the internet and cloud computing, the field shifted towards distributed systems and web-based solutions. Modern practices now emphasize automation, continuous integration, and agile development methodologies. The integration of artificial intelligence and machine learning has further transformed the landscape, enabling predictive analytics, intelligent automation, and data-driven decision making. These advancements have made it essential for professionals to continuously update their skills and adapt to emerging technologies. \n\nFurthermore, the transition from monolithic architectures to microservices has radically changed how software and hardware systems are designed and maintained. This architectural shift allows teams to work independently, accelerating the delivery of complex features. It also requires a robust understanding of containerization, orchestration tools, and distributed system debugging. In the current industry scenario, keeping abreast with these evolutionary steps is crucial for delivering high-performance, resilient, and scalable solutions that meet modern business demands.",
        "CH1_TRENDS": f"\n\nSeveral key trends are shaping the current landscape of {title}. Cloud-native development and microservices architecture have become standard practices for building scalable applications. DevOps practices and CI/CD pipelines have streamlined the software development lifecycle. The adoption of containerization technologies such as Docker and Kubernetes has revolutionized deployment strategies. Edge computing is gaining traction for applications requiring low-latency processing. \n\nFurthermore, the increasing emphasis on cybersecurity has led to the adoption of security-first development practices across organizations of all sizes. The rise of generative AI and automated coding assistants is another massive trend, significantly reducing the boilerplate code developers write and shifting the focus to high-level architecture and problem-solving. Teams are also exploring sustainable and green computing, optimizing algorithms to reduce energy consumption, which is becoming a priority for global enterprises.",
        "CH2_VISION": f"\n\nThe organization's vision extends to becoming a leading provider of technology solutions that drive innovation and create lasting value for clients and stakeholders. Their mission emphasizes the importance of continuous learning, practical skill development, and maintaining the highest standards of quality in all deliverables. This alignment between vision and daily practice creates a productive and growth-oriented work environment. \n\nLooking forward, the organization aims to expand its technological footprint by embracing open-source initiatives and community-driven projects. They emphasize fostering a workplace culture where ethical engineering and societal impact are at the forefront of every business decision. This forward-thinking vision ensures they remain competitive while contributing positively to the broader technology ecosystem.",
        "CH2_PROGRAMS": f"\n\nThe organization offers a diverse range of programs and services that cater to various aspects of technology and engineering. These include structured internship programs for engineering students, professional training workshops, consulting services for technology implementation, and research and development initiatives. The programs are designed to bridge the gap between academic knowledge and industry requirements, ensuring that participants gain practical, applicable skills. \n\nIn addition to technical skill development, the organization conducts seminars on leadership, project management, and agile methodologies. This holistic approach ensures that individuals are well-equipped to handle the multifaceted challenges of the modern corporate world. Their services are continually updated to reflect the latest technological advancements, ensuring clients and students receive the most current and relevant guidance.",
        "CH2_IMPACT": f"\n\nThe organization has made a significant impact in the technology sector through its commitment to quality, innovation, and skill development. Key impact areas include training and mentoring hundreds of engineering students, developing solutions that improve operational efficiency for client organizations, contributing to open-source projects and knowledge sharing, and establishing partnerships with academic institutions. These efforts have positioned the organization as a trusted partner in the technology ecosystem. \n\nTheir commitment to excellence has resulted in several industry accolades and a high retention rate among their client base. By continuously delivering scalable and reliable technological solutions, they have empowered businesses to achieve their digital transformation goals faster and more efficiently. Furthermore, their internship programs have successfully transitioned many students into highly skilled professionals, significantly reducing the industry's skill gap.",
        "CH2_VALUES": f"\n\nThese core values are not merely stated principles but are actively embedded in the organization's daily operations, decision-making processes, and employee interactions. The commitment to these values creates a work culture that fosters creativity, encourages continuous improvement, and supports both individual and collective growth. \n\nTransparency, integrity, and collaboration form the foundation of their corporate philosophy. Employees are encouraged to take ownership of their work and are provided with the autonomy to experiment with novel solutions. This environment not only accelerates innovation but also ensures that ethical considerations and high quality standards are maintained across all projects and deliverables.",
        "CH3_TOOLS": f"\n\nEach tool was selected based on its suitability for the specific requirements of the project, its industry adoption, and its ability to integrate with other components in the technology stack. Understanding the strengths and limitations of each tool was an important part of the learning experience during the internship. \n\nFurthermore, setting up the development environment required configuring these tools to work harmoniously together. This involved dealing with version compatibility, environment variables, and establishing automated build scripts. The process of troubleshooting integration issues provided deep insights into the underlying architecture of these technologies, transforming theoretical knowledge into practical, hands-on expertise that is invaluable in a professional setting.",
        "CH3_PROCESS": f"\n\nThe methodology followed during the internship emphasized iterative development, regular code reviews, and continuous feedback. Each task began with a thorough understanding of requirements, followed by research and planning. Implementation was done in incremental steps, with testing at each stage to ensure quality. Documentation was maintained throughout the process to facilitate knowledge transfer and future reference. This structured approach helped in managing complexity and delivering reliable solutions. \n\nDaily stand-up meetings were held to discuss progress, outline the day's objectives, and identify any potential roadblocks. This agile approach ensured that any issues were addressed promptly, preventing them from escalating into major delays. Version control was rigorously maintained, with meaningful commit messages and proper branching strategies, ensuring that the codebase remained clean, stable, and easily understandable for all team members.",
        "CH3_CASESTUDY": f"\n\nThe project provided valuable insights into the complete software development lifecycle, from requirements gathering and design to implementation, testing, and deployment. It demonstrated the importance of proper architecture planning, code organization, and testing strategies in building maintainable and scalable applications. The experience gained from this project has been instrumental in developing a comprehensive understanding of professional software development practices. \n\nA significant portion of the work involved refactoring existing modules to improve performance and readability. By analyzing the time complexity of critical algorithms and optimizing database queries, the overall system responsiveness was markedly improved. This hands-on optimization process highlighted the critical difference between writing functional code and writing efficient, production-ready code that can scale with increasing user demand.",
        "CH3_CHALLENGES": f"\n\nAdditionally, managing time effectively across multiple concurrent tasks required developing strong organizational skills. Understanding and adapting to the company's coding standards and development workflow also presented an initial learning curve that required patience and systematic effort to overcome. \n\nOne of the major technical hurdles encountered was dealing with inconsistent data formats when integrating third-party APIs. This required developing robust parsing mechanisms and extensive error-handling logic to prevent system crashes. Debugging these integration issues often involved meticulously analyzing network logs and understanding the nuances of asynchronous data flow, which was both challenging and highly educational.",
        "CH3_SOLUTIONS": f"\n\nMoreover, establishing a habit of documenting learnings and maintaining detailed notes helped in retaining and applying knowledge across different tasks. Seeking regular feedback from supervisors and peers also proved invaluable in identifying areas for improvement and refining approaches. \n\nTo address the technical challenges, comprehensive unit tests were written to cover edge cases, ensuring that the application behaved predictably under various scenarios. We also implemented fallback mechanisms so that the system could gracefully degrade rather than fail completely when external services were unresponsive. By systematically breaking down complex problems into smaller, manageable sub-tasks, the overall troubleshooting process became much more efficient and less overwhelming.",
        "CH4_OUTCOMES": f"\n\nThese outcomes demonstrate the practical value of the internship in building real-world engineering competencies. The deliverables produced during the internship met professional quality standards and contributed meaningfully to the organization's objectives. The experience has established a strong foundation for future professional endeavors in the field. \n\nThe solutions developed have been successfully integrated into the organization's workflow, leading to measurable improvements in efficiency and reduced processing times. The positive feedback received from the project stakeholders validates the quality of the work and underscores the importance of adhering to industry best practices. This tangible contribution to the organization's goals has been highly rewarding and motivating.",
        "CH4_LEARNING": f"\n\nBeyond technical competencies, the internship fostered important professional skills such as effective communication, teamwork, time management, and adaptability. These soft skills are equally valuable in a professional engineering career and complement the technical knowledge gained during the internship period. \n\nPresenting technical concepts to non-technical stakeholders was a particularly valuable learning experience. It required distilling complex algorithms and architectures into clear, understandable business benefits. Additionally, participating in code review sessions improved my ability to give and receive constructive criticism, fostering a collaborative mindset that is essential for working effectively within a professional engineering team.",
        "CH4_ANALYSIS": f"\n\nOverall, the internship experience exceeded initial expectations in terms of the depth and breadth of learning opportunities provided. While certain areas could have benefited from more structured guidance, the hands-on approach proved highly effective in developing practical engineering skills. The experience has highlighted the importance of continuous learning and adaptability in the rapidly evolving technology landscape. \n\nAn analysis of the tasks completed shows a clear progression from basic implementation assignments to handling complex, architectural challenges. This progressive increase in responsibility allowed for a gradual build-up of confidence and competence. The practical exposure to real-world constraints, such as tight deadlines and legacy codebases, provided a realistic preview of the challenges commonly faced in the professional software engineering industry.",
        "CH5_SUMMARY": f"\n\nThe internship experience at {company} has been a transformative journey that has significantly enhanced both technical capabilities and professional outlook. The exposure to real-world engineering practices, combined with mentorship from experienced professionals, has provided a solid foundation for a career in technology and engineering. \n\nThe opportunity to work on live projects and contribute to meaningful solutions has bridged the gap between academic theory and industry practice. The insights gained regarding system architecture, agile methodologies, and collaborative development are invaluable. This comprehensive learning experience has not only improved my technical proficiency but has also shaped my approach to problem-solving and professional conduct.",
        "CH5_GROWTH": f"\n\nThe internship has instilled a growth mindset and a commitment to continuous learning. The experience of working in a professional environment has improved my ability to collaborate effectively, communicate technical concepts clearly, and approach complex problems with a structured methodology. These personal and professional developments will serve as valuable assets throughout my career. \n\nThe challenges faced during the internship have cultivated resilience and a proactive approach to overcoming obstacles. Learning to independently research and implement new technologies has boosted my self-reliance and confidence. The constructive feedback received throughout the program has been instrumental in identifying my strengths and areas for further improvement, guiding my ongoing professional development journey.",
        "CH5_FUTURE": f"\n\nThe field continues to evolve rapidly, with emerging technologies creating new opportunities for innovation and specialization. The skills and knowledge gained during this internship provide a strong foundation for pursuing advanced studies, industry certifications, or specialized roles in technology companies. The internship has opened up multiple career pathways and has reinforced the commitment to lifelong learning in this dynamic field. \n\nMoving forward, I plan to further explore the areas of distributed systems and cloud architecture, which I found particularly fascinating during my internship. The practical foundation established here will be crucial as I undertake more complex academic projects and prepare for my future career. The professional network built during this period will also be a valuable resource for future collaborations and career guidance.",
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

I express my sincere gratitude to \textbf{{{prin_e}}}, Principal, Vemana Institute of Technology, Bengaluru, for providing the necessary infrastructure, encouragement, and support to successfully carry out the internship work.

I extend my heartfelt thanks to \textbf{{{hod_e}}}, Head of the Department, {dept_e}, Vemana Institute of Technology, for their constant guidance, motivation, and encouragement throughout the internship duration.

I would also like to thank Internal Supervisor \textbf{{{intsup_e}}}, External Supervisor \textbf{{{extsup_e}}}, and all Internship Coordinators for their cooperation, coordination, and support during the internship period.

I am thankful to all the teaching and non-teaching staff members of the Department of {dept_e} for their support and encouragement throughout the internship.

I also acknowledge the support of \textbf{{{comp_e}}} for providing structured learning resources and an environment that encouraged systematic understanding, practical application, and continuous improvement."""

    # -- Build custom TOC entries for the table format -----------------------
    # We'll build a manual TOC in a tabular environment matching the template
    # The template uses: Chapter | Title | Page No columns

    # Count total main-body pages (approximate for TOC page refs)
    # We'll use \label/\pageref for accurate numbering

    # =======================================================================
    # FULL LATEX DOCUMENT
    # =======================================================================
    tex = rf"""\documentclass[12pt,a4paper]{{report}}
\usepackage{{indentfirst}}

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
\setstretch{{1.15}}
%\setlength{{\parindent}}{{1.5em}}
\setlength{{\parskip}}{{0.4em}}

% -- Chapter heading format -------------------------------------------------
\titleformat{{\chapter}}[display]
  {{\filcenter\bfseries\Large}}
  {{\chaptername~\thechapter}}{{10pt}}{{\LARGE}}

\titlespacing*{{\chapter}}
{{0pt}}
{{-10pt}}
{{35pt}}

% Ensure chapter marks are set for headers
\renewcommand{{\chaptermark}}[1]{{\markboth{{#1}}{{#1}}}}

% -- Rename TOC / LOF headings to match template ----------------------------
\renewcommand{{\contentsname}}{{TABLE OF CONTENTS}}
\renewcommand{{\listfigurename}}{{LIST OF FIGURES}}

% -- TOC heading format (consistent with other front-matter headings) -------
\renewcommand{{\cfttoctitlefont}}{{\hfill\LARGE\bfseries}}
\renewcommand{{\cftaftertoctitle}}{{\hfill}}
\renewcommand{{\cftloftitlefont}}{{\hfill\LARGE\bfseries}}
\renewcommand{{\cftafterloftitle}}{{\hfill}}
\setlength{{\cftbeforetoctitleskip}}{{-1.5em}}
\setlength{{\cftaftertoctitleskip}}{{1.5em}}
\setlength{{\cftbeforeloftitleskip}}{{-1.5em}}
\setlength{{\cftafterloftitleskip}}{{1.5em}}
\renewcommand{{\cftsecleader}}{{\cftdotfill{{\cftdotsep}}}}
\renewcommand{{\cftchapleader}}{{\cftdotfill{{\cftdotsep}}}}

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
  \renewcommand{{\chaptermark}}[1]{{\markboth{{##1}}{{}}}}
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
\setlength{{\parindent}}{{0pt}}
% ==========================================================================
% TITLE PAGE  (single-spaced, zero parskip so it fits on one page)
% ==========================================================================
\begin{{titlepage}}
\thispagestyle{{empty}}
\begin{{singlespacing}}
\setlength{{\parskip}}{{0pt}}
%\setlength{{\parindent}}{{0pt}}
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
{{\large \textbf{{\textcolor{{black}}{{{dept_e}}}}}\par}}
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

% Watermark
\AddToShipoutPictureFG*{{%
\begin{{tikzpicture}}[remember picture,overlay]
\node[opacity=0.05] at ([yshift=-4.8cm]current page.center)
{{
\includegraphics[height=7cm]{{images/vit_logo.png}}
}};
\end{{tikzpicture}}
}}

\begin{{center}}

\vspace*{{-1.4cm}}

{{\large \textbf{{Karnataka ReddyJana Sangha}}}}

{{\Large \textbf{{VEMANA INSTITUTE OF TECHNOLOGY}}}}\\[2pt]

{{\small (Affiliated to Visvesvaraya Technological University, Belagavi)}}\\[-1pt]

{{\small Koramangala, Bengaluru--560034}}\\[10pt]

\includegraphics[height=2.8cm]{{images/dept_seal.png}}\\[8pt]

{{\large \textbf{{DEPARTMENT OF}}}}\\[2pt]

{{\large \textbf{{{dept_e.upper()}}}}}\\[10pt]

{{\LARGE \textbf{{CERTIFICATE}}}}

\end{{center}}

\vspace{{0.2cm}}

\noindent
This is to certify that the internship entitled \textbf{{“{title_e}”}} is a bonafide work carried out by \textbf{{{name_upper} ({usn})}} in partial fulfillment of the requirements for the award of Bachelor of Engineering degree in \textbf{{{dept_e}}}, Visvesvaraya Technological University, Belagavi, during the academic year {year_e}.

\vspace{{0.25cm}}

\noindent
It is certified that all corrections and suggestions indicated for internal assessment have been duly incorporated in the report. The internship report has been approved as it satisfies the academic requirements prescribed for the said degree.

\vspace{{1.2cm}}

\begin{{center}}

\renewcommand{{\arraystretch}}{{1.15}}

\begin{{tabular}}{{c c c c}}

\textbf{{Internal Supervisor}} &
\textbf{{External Supervisor}} &
\textbf{{HOD}} &
\textbf{{Principal}}
\\[4pt]

({intsup_e}) &
({extsup_e}) &
({hod_e}) &
({prin_e})

\end{{tabular}}

\end{{center}}

\vspace{{1cm}}

\noindent
\textbf{{Name of the Examiners}}
\hfill
\textbf{{Signature with Date}}

\vspace{{0.4cm}}

\noindent
1.\hspace{{0.2cm}}\rule{{5cm}}{{0.4pt}}
\hfill
\rule{{4cm}}{{0.4pt}}

\vspace{{0.4cm}}

\noindent
2.\hspace{{0.2cm}}\rule{{5cm}}{{0.4pt}}
\hfill
\rule{{4cm}}{{0.4pt}}


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
\setlength{{\parskip}}{{1em}}
\begin{{onehalfspacing}}
{ack_body}
\end{{onehalfspacing}}
\setlength{{\parskip}}{{0.4em}}

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
%\setlength{{\parindent}}{{1.5em}}
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
% We need the custom header for LOF
\addtocontents{{lof}}{{\textbf{{Figure No}} \hfill \textbf{{Title}} \hfill \textbf{{Page No}}\par\smallskip\hrule\par\bigskip}}
\listoffigures

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
  \renewcommand{{\chaptermark}}[1]{{\markboth{{##1}}{{}}}}
}}
\pagestyle{{mainchapter}}

% ==========================================================================
% CHAPTER 1: INTRODUCTION
% ==========================================================================
\chapter{{INTRODUCTION}}
\label{{ch:intro}}

{S("CH1_INTRO")}

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

{S("CH2_INTRO")}

\section{{Introduction}}
{S("CH2_ORG_INTRO")}

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

{S("CH3_OVERVIEW")}

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

{S("CH4_INTRO")}

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
