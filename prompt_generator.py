def generate_prompt(data):
    name                = data.get("name", "")
    usn                 = data.get("usn", "")
    department          = data.get("department", "")
    degree              = data.get("degree", "Bachelor of Engineering")
    internal_supervisor = data.get("internal_supervisor", "")
    hod                 = data.get("hod", "")
    company_name        = data.get("company_name", "")
    internship_title    = data.get("internship_title", "")
    external_supervisor = data.get("external_supervisor", "")
    start_date          = data.get("start_date", "")
    end_date            = data.get("end_date", "")
    academic_year       = data.get("academic_year", "2025-2026")
    company_summary     = data.get("company_summary", "")

    prompt = f"""You are writing a professional internship report for an engineering student at Vemana Institute of Technology (VIT), Bengaluru, affiliated to Visvesvaraya Technological University (VTU).

STUDENT INFORMATION:
- Student Name: {name}
- USN: {usn}
- Department: {department}
- Degree: {degree}
- Academic Year: {academic_year}
- Internal Supervisor: {internal_supervisor}
- HOD: {hod}

INTERNSHIP INFORMATION:
- Company: {company_name}
- Role/Title: {internship_title}
- External Supervisor (from company): {external_supervisor}
- Duration: {start_date} to {end_date}

ABOUT THE COMPANY (use this to write accurate, specific content):
{company_summary}

---

CRITICAL REQUIREMENTS:
- Write in FIRST PERSON (I, my, me)
- Be professional and academic in tone
- Be SPECIFIC to {company_name} and the role "{internship_title}"
- NEVER use placeholder text like "[Company Name]" — always use the real names
- Use varied sentence structure throughout
- Each section must start immediately after its marker
- IMPORTANT: Write SUBSTANTIAL content for each section. The report must be at least 15-18 pages long. Each section MUST meet its MINIMUM word count. Short sections will cause incorrect page numbering in the Table of Contents.

Generate ALL sections using EXACTLY these markers (do not skip any):

===ABSTRACT===
(250-350 words. Summarize the entire internship at {company_name}: what was learned, what was done, key outcomes, technologies used, and how the experience contributed to professional development. First person. Include specific project names and technologies.)

===ACKNOWLEDGEMENT===
(250-300 words. Thank VTU, Principal Dr. Vijayasimha Reddy B G, HOD {hod}, Internal Supervisor {internal_supervisor}, External Supervisor {external_supervisor}, {company_name}, and all staff members. Professional academic tone. First person.)

===CH1_INTRO===
(200-250 words. Opening paragraph for Chapter 1. Introduce the internship at {company_name} in the role of {internship_title}. Explain the industry context, why internships are important in engineering education, what the chapter covers, and the overall structure of the report.)

===CH1_SCOPE===
(300-400 words. Section: Internship Scope and Objectives. Detail the goals and scope of this internship comprehensively. Use bullet points for at least 6-8 specific objectives. Explain each objective in 1-2 sentences. Cover technical skills, professional development, and domain knowledge goals.)

===CH1_RELEVANCE===
(300-400 words. Section: Relevance of {internship_title} to {department}. Explain in depth why this internship matters for this engineering domain. Include specific connections between coursework and internship tasks. Discuss at least 4-5 specific areas where the internship connects to the curriculum.)

===CH1_EVOLUTION===
(250-300 words. Section: Evolution of Practices in the Field. How this technology/field has evolved over time — from early stages to current state. Include specific milestones, key developments, and paradigm shifts. Discuss at least 3-4 distinct evolutionary phases.)

===CH1_TRENDS===
(250-300 words. Section: Current Trends and Technologies. Latest tools and trends relevant to this internship domain. Include specific technologies, frameworks, industry standards. Discuss at least 5-6 current trends with brief explanations.)

===CH2_INTRO===
(150-200 words. Chapter 2 opening paragraph. State what this chapter covers about {company_name} and why understanding the organization is important for the internship context.)

===CH2_ORG_INTRO===
(300-400 words. Section 2.1 Introduction of {company_name}. History, founding year, purpose, what they do, who they serve, geographic reach, key achievements. Be very specific from company info provided. Include details about company size, clientele, and market position.)

===CH2_VISION===
(200-250 words. Section: Vision and Mission of {company_name}. Separate vision and mission clearly. Include company's long-term goals, strategic direction, and how they align with industry needs. Discuss how these influence the work culture and internship experience.)

===CH2_PROGRAMS===
(250-300 words. Section: Programs and Services Offered by {company_name}. List and describe key services, programs, domains in detail. Use bullet points for at least 5-6 programs/services with explanations.)

===CH2_IMPACT===
(200-250 words. Section: Organizational Impact and Reach. Include stats or numbers if available. Use bullet points for impact metrics. Discuss contributions to industry, community, and education. Include at least 5-6 impact points.)

===CH2_VALUES===
(200-250 words. Section: Core Values. Use bullet points for 6-8 values with 2-3 sentence explanation of each. Discuss how these values are reflected in the daily work culture.)

===CH3_OVERVIEW===
(200-250 words. Chapter 3 opening paragraph describing what the chapter covers about the work done. Provide an overview of the entire work timeline and major phases of the internship.)

===CH3_WORK_OVERVIEW===
(350-450 words. Section 3.1 Overview of Internship Work. What tasks were performed day-to-day. Be very specific to the role. Break down into phases or sprints. Include at least 4-5 major work areas with detailed descriptions of responsibilities in each.)

===CH3_TOOLS===
(300-400 words. Section: Tools and Technologies Used. List and explain each tool used. Use bullet points for at least 8-10 tools/technologies. For each tool, explain what it is, why it was chosen, and how it was used in the project.)

===CH3_PROCESS===
(300-400 words. Section: Work Process and Methodology. Detailed step-by-step description of how work was approached — research, planning, execution, testing, review, documentation. Include specific methodologies like Agile, Scrum, etc. with concrete examples.)

===CH3_CASESTUDY===
(400-500 words. Section: Key Project and Case Study. A specific project or major task in full detail. Include: project background, requirements, architecture, implementation steps, and results. Use bullet points for key features/characteristics. This should be the most detailed section of the chapter.)

===CH3_CHALLENGES===
(250-300 words. Section: Challenges Faced. What was difficult. Describe 5-6 specific technical and non-technical challenges in detail. For each challenge, explain the context and impact.)

===CH3_SOLUTIONS===
(250-300 words. Section: Solutions Implemented. How each challenge was overcome. Match each solution to its corresponding challenge. Include specific technical approaches used.)

===CH4_INTRO===
(150-200 words. Chapter 4 opening paragraph. What this chapter presents — comprehensive evaluation and analysis of work done during the internship, including measurable outcomes.)

===CH4_OUTCOMES===
(300-400 words. Section: Outcomes of the Work. What was delivered and achieved at {company_name}. Use bullet points for at least 6-8 specific deliverables and outcomes. Include measurable results where possible.)

===CH4_LEARNING===
(300-400 words. Section: Learning Outcomes. Technical and soft skills gained. Be specific to {internship_title}. Use bullet points for at least 8-10 specific learning outcomes across technical skills, domain knowledge, and professional competencies.)

===CH4_ANALYSIS===
(250-300 words. Section: Analysis. Critical evaluation — what worked well, areas of improvement, limitations, comparison with initial expectations, and recommendations for future interns.)

===CH5_INTRO===
(150-200 words. Chapter 5 opening paragraph. Summarize the significance of the internship and what this concluding chapter will discuss.)

===CH5_SUMMARY===
(300-400 words. Section: Summary. Comprehensive recap of the full internship experience at {company_name}. Cover all chapters briefly — introduction, organization, work done, results. Include key highlights and achievements.)

===CH5_GROWTH===
(250-300 words. Section: Personal Growth. Professional and personal development in detail. How perspective changed. Include specific before/after comparisons of skills and knowledge. Discuss at least 5-6 areas of growth.)

===CH5_FUTURE===
(250-300 words. Section: Future Scope. How this field/domain will evolve and what opportunities it opens. Discuss emerging technologies, career paths, and further learning opportunities. Include at least 4-5 future directions.)
"""
    return prompt
