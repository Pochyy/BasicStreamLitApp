import streamlit as st
import pandas as pd
import altair as alt
import os
from datetime import datetime

# ==========================================
# PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="Vinzent Emmanuel M. Lariosa | Portfolio",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# CUSTOM PAPER-INSPIRED CSS SYSTEM
# ==========================================
# Note: Strictly adheres to paper palette, typography, and no-emoji rule.
paper_css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Caveat:wght@500;600;700&family=Inter:wght@300;400;500;600&family=Lora:ital,wght@0,400;0,500;0,600;1,400&display=swap');

:root {
    --bg-canvas: #EAE5DA;
    --paper-main: #F8F6EF;
    --paper-sub: #F0EBDD;
    --text-primary: #292820;
    --text-muted: #777266;
    --accent-brown: #A18B70;
    --sticky-yellow: #F4E7A1;
    --sticky-green: #DCE5D0;
    --sticky-pink: #EBD7D3;
    --border-color: #D8D1C3;
    --font-heading: 'Lora', Georgia, serif;
    --font-body: 'Inter', -apple-system, sans-serif;
    --font-handwritten: 'Caveat', cursive;
}

/* Global Background */
.stApp {
    background-color: var(--bg-canvas);
    color: var(--text-primary);
    font-family: var(--font-body);
}

/* Typography Overrides */
h1, h2, h3, h4 {
    font-family: var(--font-heading) !important;
    color: var(--text-primary) !important;
    font-weight: 500 !important;
    letter-spacing: -0.01em;
}

p, span, label, li {
    color: var(--text-primary);
    font-size: 0.96rem;
    line-height: 1.65;
}

/* Sidebar Customization */
[data-testid="stSidebar"] {
    background-color: var(--paper-sub);
    border-right: 1px solid var(--border-color);
}
[data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
    color: var(--text-primary);
}

/* Paper Sheet Container */
.paper-sheet {
    background-color: var(--paper-main);
    border: 1px solid var(--border-color);
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.04), 0 1px 2px rgba(0, 0, 0, 0.02);
    padding: 28px 32px;
    margin-bottom: 24px;
    border-radius: 2px;
    position: relative;
}

/* Secondary Paper Sheet */
.paper-sheet-subtle {
    background-color: var(--paper-sub);
    border: 1px solid var(--border-color);
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.03);
    padding: 22px 26px;
    margin-bottom: 20px;
    border-radius: 2px;
    position: relative;
}

/* Washi Tape Strip */
.washi-tape {
    width: 110px;
    height: 18px;
    background: rgba(216, 209, 195, 0.75);
    border-left: 2px dashed rgba(161, 139, 112, 0.4);
    border-right: 2px dashed rgba(161, 139, 112, 0.4);
    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
    margin: 0 auto 12px auto;
}

.washi-tape-corner {
    position: absolute;
    top: -10px;
    left: 24px;
    width: 90px;
    height: 20px;
    background: rgba(220, 214, 200, 0.85);
    border-left: 1px dashed rgba(161, 139, 112, 0.5);
    border-right: 1px dashed rgba(161, 139, 112, 0.5);
    transform: rotate(-2deg);
    z-index: 10;
}

/* Handwritten Annotations */
.handwritten {
    font-family: var(--font-handwritten) !important;
    font-size: 1.35rem !important;
    color: var(--accent-brown) !important;
    line-height: 1.2;
}

.handwritten-small {
    font-family: var(--font-handwritten) !important;
    font-size: 1.15rem !important;
    color: var(--text-muted) !important;
}

/* Sticky Notes */
.sticky-note {
    padding: 18px 20px;
    border-radius: 1px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.06), 0 1px 3px rgba(0,0,0,0.04);
    margin-bottom: 18px;
    position: relative;
    border-top: 1px solid rgba(255,255,255,0.4);
}

.sticky-yellow {
    background-color: var(--sticky-yellow);
    transform: rotate(-1deg);
    border-left: 1px solid #ebd982;
}

.sticky-green {
    background-color: var(--sticky-green);
    transform: rotate(1.2deg);
    border-left: 1px solid #c7d5b8;
}

.sticky-pink {
    background-color: var(--sticky-pink);
    transform: rotate(-0.8deg);
    border-left: 1px solid #dfc3bd;
}

/* Photo Matting */
.photo-frame {
    background-color: #FFFFFF;
    padding: 10px 10px 20px 10px;
    border: 1px solid var(--border-color);
    box-shadow: 0 4px 10px rgba(0,0,0,0.08);
    transform: rotate(0.8deg);
    text-align: center;
    max-width: 320px;
    margin: 0 auto;
}

.photo-frame img {
    max-height: 340px !important;
    object-fit: cover !important;
    object-position: center 20% !important;
    width: 100% !important;
}
}

/* Section Header Bar */
.section-header {
    border-bottom: 1px solid var(--border-color);
    padding-bottom: 8px;
    margin-bottom: 18px;
    display: flex;
    justify-content: space-between;
    align-items: baseline;
}

/* Lined Journal Background for selected readings */
.lined-paper {
    background-color: var(--paper-main);
    background-image: repeating-linear-gradient(
        var(--paper-main) 0px,
        var(--paper-main) 27px,
        #EBE5D8 28px
    );
    border: 1px solid var(--border-color);
    padding: 24px 28px;
    line-height: 28px;
}

/* Tag labels */
.paper-tag {
    display: inline-block;
    background-color: var(--paper-sub);
    border: 1px solid var(--border-color);
    padding: 2px 10px;
    font-size: 0.8rem;
    color: var(--text-muted);
    border-radius: 2px;
    margin-right: 6px;
    margin-bottom: 6px;
}

/* Streamlit Native Widget Resets */
.stButton > button {
    background-color: var(--paper-sub) !important;
    color: var(--text-primary) !important;
    border: 1px solid var(--border-color) !important;
    border-radius: 2px !important;
    font-family: var(--font-body) !important;
    box-shadow: 0 1px 2px rgba(0,0,0,0.04) !important;
    transition: all 0.15s ease-in-out !important;
}
.stButton > button:hover {
    background-color: var(--paper-main) !important;
    border-color: var(--accent-brown) !important;
    color: var(--text-primary) !important;
}

.stDownloadButton > button {
    background-color: var(--paper-main) !important;
    color: var(--text-primary) !important;
    border: 1px solid var(--accent-brown) !important;
    border-radius: 2px !important;
    font-family: var(--font-body) !important;
}

[data-testid="stMetric"] {
    background-color: var(--paper-main);
    border: 1px solid var(--border-color);
    padding: 16px 18px;
    border-radius: 2px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.03);
    min-width: 0;
}

[data-testid="stMetricLabel"] *,
[data-testid="stMetricValue"] *,
[data-testid="stMetricDelta"] * {
    white-space: normal !important;
    overflow: visible !important;
    text-overflow: unset !important;
    word-break: normal !important;
}

[data-testid="stMetricValue"] {
    font-family: var(--font-heading) !important;
    color: var(--text-primary) !important;
    font-size: 1.4rem !important;
}

[data-testid="stMetricLabel"] {
    color: var(--text-muted) !important;
    font-size: 0.78rem !important;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

[data-testid="stMetricDelta"] {
    font-size: 0.82rem !important;
    color: var(--text-muted) !important;
}

/* Table styling */
[data-testid="stTable"], [data-testid="stDataFrame"] {
    border: 1px solid var(--border-color);
    background-color: var(--paper-main);
}
</style>
"""
st.markdown(paper_css, unsafe_allow_html=True)

# ==========================================
# SESSION STATE INITIALIZATION
# ==========================================
if "feedback_entries" not in st.session_state:
    st.session_state["feedback_entries"] = []

if "view_mode" not in st.session_state:
    st.session_state["view_mode"] = "Tabbed Journal View"

# ==========================================
# DATA DEFINITIONS
# ==========================================
SKILLS_DATA = [
    {"Skill": "Java Programming", "Category": "Backend & Core", "Rating": 3, "Proficiency": "Intermediate"},
    {"Skill": "Python Programming", "Category": "Backend & Core", "Rating": 2, "Proficiency": "Basic"},
    {"Skill": "JavaScript", "Category": "Web Development", "Rating": 3, "Proficiency": "Intermediate"},
    {"Skill": "React.js", "Category": "Web Development", "Rating": 3, "Proficiency": "Intermediate"},
    {"Skill": "Spring Boot", "Category": "Backend & Core", "Rating": 3, "Proficiency": "Intermediate"},
    {"Skill": "Kotlin / Android Development", "Category": "Mobile Development", "Rating": 3, "Proficiency": "Intermediate"},
    {"Skill": "HTML and CSS", "Category": "Web Development", "Rating": 3, "Proficiency": "Intermediate"},
    {"Skill": "SQL / Database Management", "Category": "Data & Storage", "Rating": 3, "Proficiency": "Intermediate"},
    {"Skill": "Git and GitHub", "Category": "Tools & Workflow", "Rating": 3, "Proficiency": "Intermediate"},
    {"Skill": "Computer Networking Fundamentals", "Category": "Networking & Infrastructure", "Rating": 2, "Proficiency": "Basic"},
    {"Skill": "Network Troubleshooting", "Category": "Networking & Infrastructure", "Rating": 2, "Proficiency": "Basic"},
    {"Skill": "IP Addressing and Subnetting", "Category": "Networking & Infrastructure", "Rating": 2, "Proficiency": "Basic"},
    {"Skill": "Cloud Computing Fundamentals", "Category": "Networking & Infrastructure", "Rating": 2, "Proficiency": "Basic"},
    {"Skill": "Debugging and Troubleshooting", "Category": "Methodologies & Soft Skills", "Rating": 3, "Proficiency": "Intermediate"},
    {"Skill": "Teamwork and Collaboration", "Category": "Methodologies & Soft Skills", "Rating": 3, "Proficiency": "Intermediate"},
    {"Skill": "Problem-Solving", "Category": "Methodologies & Soft Skills", "Rating": 3, "Proficiency": "Intermediate"},
]

df_skills = pd.DataFrame(SKILLS_DATA)

PROJECTS_DATA = [
    {
        "id": "cit-u-ojt",
        "title": "CIT-U OJT Internship Management System",
        "role": "Student Developer (Team Project)",
        "tech_stack": ["React.js", "JavaScript", "Java", "Spring Boot", "MySQL", "Git", "GitHub"],
        "category": "Web Application",
        "description": "A web-based system designed to support the management of student internship applications and related On-the-Job Training (OJT) processes.",
        "contributions": "Worked on frontend development, application navigation, login and registration screens, role-based access control, and integration with backend API functionality.",
        "outcome": "Developed key functional parts of an internship management platform aimed at making OJT-related tracking and administrative processes more organized.",
        "github_url": "https://github.com/Pochyy/citumanagementsystem"
    },
    {
        "id": "modular-monolith",
        "title": "Modular Monolith Integration: Tiangge & LegacySupply",
        "role": "Student Developer",
        "tech_stack": ["Java 17", "Spring Boot", "Maven", "PostgreSQL", "Supabase", "Git"],
        "category": "Enterprise Backend",
        "description": "An academic software engineering project focused on integrating different modules and external systems using a structured modular monolith architecture.",
        "contributions": "Worked on supplier integration services, scheduled order polling routines, access control, stock level synchronization, and resilient integration error handling.",
        "outcome": "Engineered a functional prototype demonstrating robust communication between the core application and external supplier systems, including order and inventory workflows.",
        "github_url": "https://github.com/Pochyy/modular-monolith-integration"
    },
    {
        "id": "simplenotes",
        "title": "SimpleNotes: Android Note-Taking Application",
        "role": "Android Developer",
        "tech_stack": ["Kotlin", "XML", "Android Studio", "SharedPreferences", "GitHub"],
        "category": "Mobile Application",
        "description": "A clean Android application that enables users to create, manage, search, and systematically organize personal notes on mobile devices.",
        "contributions": "Implemented the Model-View-Presenter (MVP) architecture, authentication/profile flows, note searching, pinned note priority, and user-specific persistent storage.",
        "outcome": "Delivered an MVP-style note-taking application featuring intuitive user account handling and structured mobile note organization.",
        "github_url": "https://github.com/Pochyy/SimpleNotes"
    }
]

# ==========================================
# SIDEBAR: JOURNAL INDEX & CONTROLS
# ==========================================
with st.sidebar:
    st.markdown('<div class="washi-tape"></div>', unsafe_allow_html=True)
    st.markdown("### Portfolio Desk Index")
    st.caption("CSIT349 Applied AI | Academic Submission")
    
    st.markdown("""
    <div class="sticky-note sticky-yellow">
        <strong>Student Information</strong><br>
        <strong>Name:</strong> Vinzent Emmanuel M. Lariosa<br>
        <strong>Program:</strong> BSIT - 4th Year<br>
        <strong>Section:</strong> CSIT349 - G01<br>
        <strong>Campus:</strong> CIT - University
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("#### Page Navigation")
    nav_selection = st.selectbox(
        "Jump to Notebook Section",
        [
            "Cover & Profile",
            "Autobiography Pages",
            "Technical Skills Matrix",
            "Project Portfolio Sheets",
            "Visitor Feedback Card",
            "Dossier Summary"
        ],
        index=0
    )
    
    st.markdown("#### Reading Mode")
    autobio_view = st.radio(
        "Autobiography Layout",
        ["Tabbed Journal View", "Complete Narrative View"],
        index=0,
        help="Select between tabbed reading cards or an open chronological reading view."
    )
    st.session_state["view_mode"] = autobio_view

    st.markdown("---")
    st.markdown("#### Interactive Filters")
    
    # Slider for skill rating
    min_rating_filter = st.slider(
        "Filter Skills by Minimum Rating",
        min_value=1,
        max_value=5,
        value=1,
        step=1,
        help="Adjust to filter skills shown in the primary chart view."
    )
    
    # Checkbox to maintain full table accessibility
    always_show_full_table = st.checkbox(
        "Always display full 16-skill table",
        value=True,
        help="Preserves the complete unabridged skills matrix regardless of rating filters."
    )
    
    # Multiselect for project technologies
    all_tech_tags = sorted(list({tech for p in PROJECTS_DATA for tech in p["tech_stack"]}))
    selected_tech = st.multiselect(
        "Filter Projects by Technology",
        options=all_tech_tags,
        default=[],
        help="Leave empty to display all projects, or select technologies to filter."
    )
    
    if st.button("Reset All Filters", width="stretch"):
        st.rerun()

    st.markdown("---")
    st.markdown("""
    <div class="sticky-note sticky-green">
        <span class="handwritten-small">Career Direction</span><br>
        <strong>Aspiring Networking Engineer</strong><br>
        Committed to disciplined continuous growth, network infrastructure, and system reliability.
    </div>
    """, unsafe_allow_html=True)


# ==========================================
# MAIN CONTENT: EDITORIAL SCRAPBOOK
# ==========================================

# 1. HEADER / INTRODUCTION
st.markdown('<div id="cover-profile"></div>', unsafe_allow_html=True)
st.markdown('<div class="washi-tape"></div>', unsafe_allow_html=True)

header_col1, header_col2 = st.columns([1.65, 1.0], gap="large")

with header_col1:
    st.markdown('<span class="handwritten">A little about me — personal academic journal</span>', unsafe_allow_html=True)
    st.markdown("# Vinzent Emmanuel M. Lariosa")
    st.markdown("#### Bachelor of Science in Information Technology — 4th Year")
    st.markdown("**Course and Section:** CSIT349 – G01 &nbsp;|&nbsp; **Origin:** Talisay City, Cebu")
    
    st.markdown("""
    <div class="paper-sheet" style="margin-top: 18px;">
        <div class="washi-tape-corner"></div>
        <p style="font-size: 1.05rem; font-style: italic; color: #3A3830; margin-bottom: 14px;">
            "An aspiring Networking Engineer, disciplined and determined to continuously improve, 
            challenge my capabilities, and achieve more than I once thought possible. I believe in consistent 
            growth, hard work, and making the most of every opportunity to develop both personally and professionally."
        </p>
        <p style="font-size: 0.92rem; color: #777266; margin-bottom: 0;">
            Currently compiling academic milestones, practical engineering projects, and technical self-evaluations 
            for the CSIT349 Applied AI portfolio submission at Cebu Institute of Technology – University.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Balanced 2x2 Metrics Grid directly inside left column
    st.markdown("<div style='margin-top: 14px;'></div>", unsafe_allow_html=True)
    m_row1_col1, m_row1_col2 = st.columns(2)
    with m_row1_col1:
        st.metric(label="Academic Standing", value="BSIT - 4", delta="Final Year", delta_color="off")
    with m_row1_col2:
        st.metric(label="Career Aim", value="Networking", delta="Infrastructure Focus", delta_color="off")

    st.markdown("<div style='margin-top: 8px;'></div>", unsafe_allow_html=True)
    m_row2_col1, m_row2_col2 = st.columns(2)
    with m_row2_col1:
        st.metric(label="Featured Works", value="3 Projects", delta="Documented on GitHub", delta_color="off")
    with m_row2_col2:
        st.metric(label="Skills Assessed", value="16 Items", delta="Scale of 1 to 5", delta_color="off")

with header_col2:
    st.markdown('<div class="washi-tape"></div>', unsafe_allow_html=True)
    photo_path = "assets/profile.png"
    if os.path.exists(photo_path):
        st.markdown('<div class="photo-frame">', unsafe_allow_html=True)
        st.image(photo_path, caption="Vinzent Emmanuel M. Lariosa", width="stretch")
        st.markdown('<span class="handwritten-small">Vinzent — BSIT 4, CSIT349</span>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.warning("Profile photo not found in assets. Please ensure assets/profile.png exists.")
        
    st.markdown("""
    <div class="sticky-note sticky-pink" style="margin-top: 16px;">
        <span class="handwritten-small">Core Creed</span><br>
        Consistent growth and practical problem-solving over short-term shortcuts. Exploring technology from physical networking to software systems.
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# 2. AUTOBIOGRAPHY SECTION
st.markdown('<div id="autobiography-pages"></div>', unsafe_allow_html=True)
st.markdown("""
<div class="section-header">
    <h2>Autobiography</h2>
    <span class="handwritten">Reflections from academic & personal journeys</span>
</div>
""", unsafe_allow_html=True)

if st.session_state["view_mode"] == "Tabbed Journal View":
    tab_bg, tab_edu, tab_int, tab_mil = st.tabs([
        "Background",
        "Education",
        "Interests",
        "Milestones and Achievements"
    ])
    
    with tab_bg:
        st.markdown("""
        <div class="paper-sheet">
            <span class="handwritten-small">Chapter I: Roots and Everyday Pursuits</span>
            <h3 style="margin-top: 6px;">Background</h3>
            <p>
                I am an Information Technology student from <strong>Talisay City, Cebu</strong>. I am someone who genuinely 
                enjoys learning new things, exploring technology, and developing practical skills that I can apply directly 
                in real-world situations.
            </p>
            <p>
                Outside of academics, I maintain a diverse range of offline interests including 
                <strong>baking, cooking, reading, physical fitness, and woodworking</strong>. These pursuits allow me 
                to explore both creative and tactile problem-solving, teaching me patience, attention to detail, 
                and the value of disciplined craftsmanship.
            </p>
            <div class="sticky-note sticky-green" style="max-width: 480px; margin-top: 16px;">
                <span class="handwritten-small">Journal Note</span><br>
                Woodworking and culinary preparation mirror software and networking: careful planning, proper measurement, and respecting the structure.
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    with tab_edu:
        st.markdown("""
        <div class="paper-sheet">
            <span class="handwritten-small">Chapter II: Academic Foundation</span>
            <h3 style="margin-top: 6px;">Education</h3>
            <p>
                I am currently in my fourth year of pursuing the <strong>Bachelor of Science in Information Technology</strong> 
                degree at <strong>Cebu Institute of Technology – University</strong>.
            </p>
            <p>
                Throughout my academic career, I have cultivated hands-on experience in computer programming, database management, 
                software development methodologies, and system design.
            </p>
            <p>
                I have had the opportunity to work with multiple programming languages, modern frameworks, and industry-standard 
                development tools through rigorous individual lab assignments as well as collaborative team projects.
            </p>
            <div class="sticky-note sticky-yellow" style="max-width: 440px; margin-top: 16px;">
                <span class="handwritten-small">Current Academic Status</span><br>
                Fourth-Year Senior Standing &bull; CSIT349 Applied AI &bull; CIT-U College of Computer Studies
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    with tab_int:
        st.markdown("""
        <div class="paper-sheet">
            <span class="handwritten-small">Chapter III: Passions and Focus Areas</span>
            <h3 style="margin-top: 6px;">Interests</h3>
            <p>
                My professional curiosity is anchored in understanding how complex computing systems communicate and operate reliably:
            </p>
            <ul>
                <li><strong>Computer Networking:</strong> Network infrastructure, topology planning, and systematic network troubleshooting.</li>
                <li><strong>Cloud Computing:</strong> Understanding distributed communication, virtualization, and resilient cloud architectures.</li>
                <li><strong>Software & Application Design:</strong> Backend development, clean service integration, and modular architectures.</li>
                <li><strong>Practical Problem Solving:</strong> Building dependable tools that solve tangible day-to-day problems.</li>
                <li><strong>Personal Pursuits:</strong> Baking, culinary experimentation, reading, physical conditioning, and woodworking.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
    with tab_mil:
        st.markdown("""
        <div class="paper-sheet">
            <span class="handwritten-small">Chapter IV: Progress and Turning Points</span>
            <h3 style="margin-top: 6px;">Milestones and Achievements</h3>
            <ul style="line-height: 1.8;">
                <li><strong>Senior Year Progression:</strong> Successfully advanced to the final fourth year of the Bachelor of Science in Information Technology program.</li>
                <li><strong>Full-Stack & Mobile Development:</strong> Gained extensive practical experience designing and shipping web and mobile applications across academic initiatives.</li>
                <li><strong>Multi-Language Competence:</strong> Worked with Java, Python, JavaScript, React, Spring Boot, Kotlin, and relational SQL databases.</li>
                <li><strong>Collaborative Leadership:</strong> Undertook key responsibilities in team software development projects, coordinating planning, code implementation, and troubleshooting.</li>
                <li><strong>Mobile Architecture Implementation:</strong> Architected and developed a functional Android note-taking application using the Model-View-Presenter (MVP) architecture.</li>
                <li><strong>Systems & Backend Integration:</strong> Deepened practical proficiency through complex projects involving scheduled order polling, external supplier synchronization, and database design.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

else:
    # Complete Narrative View
    st.markdown("""
    <div class="lined-paper">
        <h3 style="font-family: 'Lora', Georgia, serif; margin-bottom: 4px;">Autobiographical Narrative</h3>
        <p class="handwritten-small" style="margin-bottom: 20px;">Continuous journal entry &bull; Vinzent Emmanuel M. Lariosa</p>
        
        <p><strong>Background:</strong> I am an Information Technology student hailing from Talisay City, Cebu. I am someone driven by curiosity, who takes satisfaction in learning new concepts, exploring technology, and developing hands-on, practical capabilities that hold direct relevance to real-world environments. Outside academia, I channel focus and creativity into baking, cooking, reading, physical fitness, and woodworking—activities that demand both patience and structured execution.</p>
        
        <p><strong>Education:</strong> I am enrolled as a fourth-year student in the Bachelor of Science in Information Technology program at Cebu Institute of Technology – University. My time at CIT-U has provided a grounded foundation in programming, database design, software architecture, and system engineering. I have applied these principles across varied programming languages, backend frameworks, and collaborative tools.</p>
        
        <p><strong>Interests:</strong> My primary career ambition is to excel as a Networking Engineer. I am deeply interested in computer networking fundamentals, network infrastructure, IP addressing, subnetting, and network troubleshooting. In parallel, I explore cloud computing, backend development, system integration, and software design aimed at solving everyday operational hurdles.</p>
        
        <p><strong>Milestones & Achievements:</strong> My progression into the fourth year marks steady dedication. Along the way, I have delivered comprehensive web and mobile applications, worked extensively with Java, Python, JavaScript, React, Spring Boot, Kotlin, and SQL databases, and successfully engineered an MVP-architected Android note-taking system. These experiences have instilled in me strong collaborative habits and a persistent problem-solving mindset.</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# 3. SKILLS SECTION
st.markdown('<div id="skills-matrix"></div>', unsafe_allow_html=True)
st.markdown("""
<div class="section-header">
    <h2>Skills and Self-Assessment</h2>
    <span class="handwritten">1 to 5 proficiency scale evaluation</span>
</div>
""", unsafe_allow_html=True)

skills_intro_col1, skills_intro_col2 = st.columns([2.2, 1.0])
with skills_intro_col1:
    st.markdown("""
    <p>
        I have developing skills in both frontend and backend development. My academic experience has allowed me 
        to work with different programming languages, frameworks, databases, and development tools. I am also familiar 
        with debugging, troubleshooting, teamwork, and learning new technologies.
    </p>
    <p>
        As someone aspiring to become a <strong>Networking Engineer</strong>, I am actively expanding my knowledge 
        of computer networking, network infrastructure, IP subnetting, and cloud systems.
    </p>
    """, unsafe_allow_html=True)
with skills_intro_col2:
    st.markdown("""
    <div class="sticky-note sticky-yellow" style="padding: 12px 16px;">
        <span class="handwritten-small">Rating Scale</span><br>
        <strong>1:</strong> Beginner &nbsp;|&nbsp; <strong>2:</strong> Basic<br>
        <strong>3:</strong> Intermediate &nbsp;|&nbsp; <strong>4:</strong> Advanced<br>
        <strong>5:</strong> Highly Proficient
    </div>
    """, unsafe_allow_html=True)

# Filter skills for chart
filtered_df = df_skills[df_skills["Rating"] >= min_rating_filter]

# Altair Chart using the paper palette
st.markdown("#### Technical Proficiency Chart")
if min_rating_filter > 1:
    st.caption(f"Displaying skills with self-rating of {min_rating_filter}/5 and above (Adjust slider in the sidebar to change).")

chart = (
    alt.Chart(filtered_df)
    .mark_bar(cornerRadiusEnd=2, color="#A18B70", height=18)
    .encode(
        y=alt.Y("Skill:N", sort="-x", title="", axis=alt.Axis(labelFont="Inter", labelFontSize=12, labelColor="#292820")),
        x=alt.X("Rating:Q", title="Self-Rating (Scale 1 to 5)", scale=alt.Scale(domain=[0, 5]), axis=alt.Axis(tickCount=6, labelFont="Inter", titleColor="#777266")),
        tooltip=["Skill", "Category", "Rating", "Proficiency"]
    )
    .properties(
        height=max(220, len(filtered_df) * 26),
        background="#F8F6EF"
    )
    .configure_view(strokeWidth=1, stroke="#D8D1C3")
)
st.altair_chart(chart, width="stretch")

# Skills Table Display (Guaranteed accessibility)
st.markdown("#### Full Skills Self-Assessment Matrix")
if always_show_full_table:
    display_table_df = df_skills.copy()
    st.caption("Displaying all 16 self-assessed skills across backend, web, mobile, networking, and soft skills.")
else:
    display_table_df = filtered_df.copy()
    st.caption(f"Filtered view active (showing {len(display_table_df)} of 16 skills). Check 'Always display full 16-skill table' in the sidebar to view all.")

display_table_df["Rating Formatted"] = display_table_df["Rating"].apply(lambda r: f"{r} / 5")
st.dataframe(
    display_table_df[["Skill", "Category", "Rating Formatted", "Proficiency"]].rename(
        columns={"Rating Formatted": "Self-Rating", "Proficiency": "Assessed Level"}
    ),
    width="stretch",
    hide_index=True
)

st.markdown("<br>", unsafe_allow_html=True)

# 4. PROJECTS SECTION
st.markdown('<div id="project-sheets"></div>', unsafe_allow_html=True)
st.markdown("""
<div class="section-header">
    <h2>Project Portfolio Sheets</h2>
    <span class="handwritten">Documented works and GitHub source references</span>
</div>
""", unsafe_allow_html=True)

# Filter projects if technology tags are selected
if selected_tech:
    active_projects = [
        p for p in PROJECTS_DATA 
        if any(t in p["tech_stack"] for t in selected_tech)
    ]
    st.caption(f"Showing projects utilizing: {', '.join(selected_tech)} ({len(active_projects)} matching of {len(PROJECTS_DATA)} total).")
else:
    active_projects = PROJECTS_DATA
    st.caption("Displaying all documented software projects. Use the sidebar technology filter to narrow by stack.")

if not active_projects:
    st.info("No projects match the selected technology filters. Reset the filters from the sidebar to view all projects.")

for idx, project in enumerate(active_projects):
    sheet_bg = "paper-sheet" if idx % 2 == 0 else "paper-sheet-subtle"
    tech_badge_html = "".join([f'<span class="paper-tag">{tech}</span>' for tech in project["tech_stack"]])
    
    st.markdown(f"""
    <div class="{sheet_bg}">
        <div class="washi-tape-corner"></div>
        <div style="display: flex; justify-content: space-between; align-items: baseline; flex-wrap: wrap;">
            <h3 style="margin-bottom: 4px;">{idx + 1}. {project["title"]}</h3>
            <span class="handwritten-small" style="font-weight: 600;">{project["category"]}</span>
        </div>
        <p style="margin-bottom: 10px; color: #777266;">
            <strong>Role:</strong> {project["role"]}
        </p>
        <div style="margin-bottom: 14px;">
            {tech_badge_html}
        </div>
        <div style="margin-bottom: 12px;">
            <strong>Description:</strong><br>
            <p style="margin-top: 4px; margin-bottom: 10px;">{project["description"]}</p>
        </div>
        <div style="margin-bottom: 12px;">
            <strong>Key Contributions:</strong><br>
            <p style="margin-top: 4px; margin-bottom: 10px;">{project["contributions"]}</p>
        </div>
        <div style="margin-bottom: 16px;">
            <strong>Project Outcome:</strong><br>
            <p style="margin-top: 4px; margin-bottom: 10px;">{project["outcome"]}</p>
        </div>
        <p style="margin-bottom: 0;">
            <strong>Source Repository:</strong> 
            <a href="{project['github_url']}" target="_blank" style="color: #A18B70; text-decoration: underline; font-weight: 500;">
                {project['github_url']}
            </a>
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# 5. CONTACT / FEEDBACK CARD (FORM COMPONENT)
st.markdown('<div id="feedback-card"></div>', unsafe_allow_html=True)
st.markdown("""
<div class="section-header">
    <h2>Visitor Feedback & Correspondence</h2>
    <span class="handwritten">Leave a note or contact message</span>
</div>
""", unsafe_allow_html=True)

feedback_col1, feedback_col2 = st.columns([1.7, 1.0], gap="large")

with feedback_col1:
    st.markdown("""
    <div class="paper-sheet">
        <p style="color: #777266; margin-bottom: 16px;">
            Please fill out the form below to leave constructive feedback, comments, or inquiries regarding 
            this portfolio. Submitted notes are recorded directly into the application's active session state.
        </p>
    """, unsafe_allow_html=True)
    
    with st.form("visitor_feedback_form", clear_on_submit=True):
        f_name = st.text_input("Your Name *", placeholder="e.g., Professor / Peer Reviewer")
        f_email = st.text_input("Your Contact Email (Optional)", placeholder="e.g., reviewer@cit.edu")
        f_subject = st.selectbox(
            "Topic / Subject",
            [
                "Academic Review & Feedback",
                "Technical Project Inquiry",
                "Networking / Cloud Discussion",
                "General Message"
            ]
        )
        f_message = st.text_area("Your Note or Assessment *", placeholder="Enter your observations, feedback, or comments here...", height=120)
        
        submitted = st.form_submit_button("Record Note in Portfolio")
        
        if submitted:
            if not f_name.strip():
                st.error("Please provide your name before submitting.")
            elif not f_message.strip():
                st.error("Please include a message or note before submitting.")
            else:
                new_entry = {
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "name": f_name.strip(),
                    "email": f_email.strip() if f_email.strip() else "Not provided",
                    "subject": f_subject,
                    "message": f_message.strip()
                }
                st.session_state["feedback_entries"].append(new_entry)
                st.success(f"Thank you, {f_name.strip()}! Your note has been recorded in this active session's log.")
    
    st.markdown("</div>", unsafe_allow_html=True)

with feedback_col2:
    st.markdown("""
    <div class="sticky-note sticky-yellow">
        <span class="handwritten-small">Desk Note</span><br>
        <strong>Feedback Policy:</strong><br>
        Submissions are stored directly inside Streamlit's <code>session_state</code> for instant review during this browsing session. No external email service is fabricated.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("#### Session Feedback Log")
    if st.session_state["feedback_entries"]:
        for entry in reversed(st.session_state["feedback_entries"]):
            st.markdown(f"""
            <div class="paper-sheet-subtle" style="padding: 14px 18px; margin-bottom: 12px;">
                <div style="display: flex; justify-content: space-between;">
                    <strong>{entry['name']}</strong>
                    <span style="font-size: 0.8rem; color: #777266;">{entry['timestamp']}</span>
                </div>
                <div style="font-size: 0.85rem; color: #A18B70; margin-bottom: 6px;">{entry['subject']}</div>
                <p style="font-size: 0.9rem; margin-bottom: 0;">{entry['message']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        if st.button("Clear Session Feedback Log"):
            st.session_state["feedback_entries"] = []
            st.rerun()
    else:
        st.caption("No notes recorded yet in this session. Feel free to submit the first entry using the form.")

st.markdown("<br>", unsafe_allow_html=True)

# 6. DOSSIER SUMMARY & DOWNLOAD
st.markdown('<div id="dossier-summary"></div>', unsafe_allow_html=True)
st.markdown("""
<div class="section-header">
    <h2>Portfolio Dossier Summary</h2>
    <span class="handwritten">Exportable record for offline evaluation</span>
</div>
""", unsafe_allow_html=True)

summary_col1, summary_col2 = st.columns([2.0, 1.0])
with summary_col1:
    st.markdown("""
    <div class="paper-sheet">
        <p>
            You can download a clean, structured Markdown copy of this entire academic portfolio—including 
            the autobiography, assessed skill scores, and project documentation—for offline review or record-keeping.
        </p>
    """, unsafe_allow_html=True)
    
    skills_md_table = "| Skill / Technology | Category | Rating | Assessed Level |\n|---|---|:---:|---|\n" + "\n".join([
        f"| {row['Skill']} | {row['Category']} | {row['Rating']}/5 | {row['Proficiency']} |"
        for _, row in df_skills.iterrows()
    ])

    portfolio_md_content = f"""# PERSONAL INFORMATION & PORTFOLIO DOSSIER

**Name:** Vinzent Emmanuel M. Lariosa
**Program and Year:** Bachelor of Science in Information Technology – 4th Year (BSIT – 4)
**Subject and Section:** CSIT349 – G01
**Institution:** Cebu Institute of Technology – University
**Career Focus:** Aspiring Networking Engineer

---

## SHORT BIOGRAPHY
An aspiring Networking Engineer, disciplined and determined to continuously improve, challenge my capabilities, and achieve more than I once thought possible. I believe in consistent growth, hard work, and making the most of every opportunity to develop both personally and professionally.

---

## AUTOBIOGRAPHY
- **Background:** IT student from Talisay City, Cebu. Dedicated to practical technology and real-world skills. Offline interests include baking, cooking, reading, physical fitness, and woodworking.
- **Education:** Fourth-year BSIT at Cebu Institute of Technology – University. Experienced in programming, databases, software development, and system design.
- **Interests:** Computer networking, network infrastructure, troubleshooting, cloud computing, backend development, and building practical applications.
- **Milestones:** Senior year progression, multi-language mastery (Java, Python, JS, React, Spring Boot, Kotlin, SQL), collaborative project leadership, and MVP Android app development.

---

## SKILLS SELF-ASSESSMENT (SCALE 1 TO 5)
{skills_md_table}

---

## FEATURED PROJECTS
1. **CIT-U OJT Internship Management System**
   - Role: Student Developer (Team Project)
   - Tech: React.js, JavaScript, Java, Spring Boot, MySQL, Git, GitHub
   - Link: https://github.com/Pochyy/citumanagementsystem

2. **Modular Monolith Integration – Tiangge and LegacySupply**
   - Role: Student Developer
   - Tech: Java 17, Spring Boot, Maven, PostgreSQL, Supabase, Git
   - Link: https://github.com/Pochyy/modular-monolith-integration

3. **SimpleNotes – Android Note-Taking Application**
   - Role: Android Developer
   - Tech: Kotlin, XML, Android Studio, SharedPreferences, GitHub
   - Link: https://github.com/Pochyy/SimpleNotes
"""
    st.download_button(
        label="Download Full Portfolio Dossier (.md)",
        data=portfolio_md_content,
        file_name="Vinzent_Lariosa_Portfolio_Dossier.md",
        mime="text/markdown"
    )
    st.markdown("</div>", unsafe_allow_html=True)

with summary_col2:
    st.markdown("""
    <div class="sticky-note sticky-pink">
        <span class="handwritten-small">Verification & Integrity</span><br>
        All projects, repositories, and self-assessment scores reflect authentic student work completed for the BSIT program at CIT-U.
    </div>
    """, unsafe_allow_html=True)

# 7. FOOTER
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #777266; font-size: 0.88rem; padding: 18px 0 36px 0;">
    <strong>Vinzent Emmanuel M. Lariosa</strong> &bull; BSIT – 4 &bull; CSIT349 – G01<br>
    Cebu Institute of Technology – University &bull; Applied AI Laboratory Activity
</div>
""", unsafe_allow_html=True)
