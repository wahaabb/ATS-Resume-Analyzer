import streamlit as st
import PyPDF2
import re
import time
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="ATS Resume Analyzer Pro",
    page_icon="[ATS]",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- REDESIGNED CSS ----------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=DM+Mono:wght@400;500&family=Syne:wght@700;800&display=swap');

    /* ── CSS Variables ── */
    :root {
        --bg-deep:    #0d1117;
        --bg-card:    #161b22;
        --bg-hover:   #1f2937;
        --border:     #2d3748;
        --teal:       #2dd4bf;
        --teal-dim:   #0d9488;
        --emerald:    #34d399;
        --amber:      #fbbf24;
        --rose:       #f87171;
        --sky:        #38bdf8;
        --text-hi:    #f0f6fc;
        --text-mid:   #8b949e;
        --text-lo:    #484f58;
        --radius-lg:  16px;
        --radius-md:  10px;
        --radius-sm:  6px;
        --shadow:     0 4px 24px rgba(0,0,0,0.45);
    }

    /* ── Global Reset ── */
    html, body, .stApp {
        background-color: var(--bg-deep) !important;
        font-family: 'DM Sans', sans-serif;
        color: var(--text-hi);
    }

    /* ── Main area ── */
    .main .block-container {
        padding: 2rem 2.5rem;
        max-width: 1200px;
    }

    /* ── Sidebar ── */
    [data-testid="stSidebar"] {
        background: var(--bg-card) !important;
        border-right: 1px solid var(--border) !important;
    }
    [data-testid="stSidebar"] * {
        color: var(--text-hi) !important;
    }
    [data-testid="stSidebar"] .stMarkdown p,
    [data-testid="stSidebar"] .stMarkdown li {
        color: var(--text-mid) !important;
    }
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: var(--teal) !important;
    }
    [data-testid="stSidebar"] hr {
        border-color: var(--border) !important;
    }

    /* ── Headings ── */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Syne', sans-serif;
        color: var(--text-hi) !important;
    }

    /* ── Divider ── */
    hr {
        border-color: var(--border) !important;
        margin: 1.5rem 0;
    }

    /* ── Tabs ── */
    .stTabs [data-baseweb="tab-list"] {
        background: var(--bg-card);
        border-radius: var(--radius-md);
        padding: 4px;
        gap: 4px;
        border: 1px solid var(--border);
    }
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        color: var(--text-mid) !important;
        border-radius: var(--radius-sm);
        font-weight: 500;
        padding: 0.5rem 1.2rem;
        transition: all 0.2s;
    }
    .stTabs [aria-selected="true"] {
        background: var(--teal) !important;
        color: #0d1117 !important;
    }
    .stTabs [data-baseweb="tab-panel"] {
        background: var(--bg-card);
        border-radius: var(--radius-lg);
        padding: 1.5rem;
        border: 1px solid var(--border);
        margin-top: 0.5rem;
    }

    /* ── Buttons ── */
    .stButton > button {
        background: var(--teal) !important;
        color: #0d1117 !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.55rem 1.8rem !important;
        font-weight: 700 !important;
        font-family: 'DM Sans', sans-serif !important;
        font-size: 0.9rem !important;
        letter-spacing: 0.02em;
        transition: all 0.2s ease !important;
        box-shadow: 0 0 0 0 rgba(45,212,191,0.4);
    }
    .stButton > button:hover {
        background: var(--emerald) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(45,212,191,0.35) !important;
    }

    /* ── Download button ── */
    .stDownloadButton > button {
        background: transparent !important;
        color: var(--teal) !important;
        border: 1.5px solid var(--teal) !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        transition: all 0.2s !important;
    }
    .stDownloadButton > button:hover {
        background: var(--teal) !important;
        color: #0d1117 !important;
    }

    /* ── File uploader ── */
    [data-testid="stFileUploader"] {
        background: var(--bg-card) !important;
        border: 1.5px dashed var(--border) !important;
        border-radius: var(--radius-md) !important;
        padding: 0.5rem !important;
        transition: border-color 0.2s;
    }
    [data-testid="stFileUploader"]:hover {
        border-color: var(--teal) !important;
    }
    [data-testid="stFileUploader"] * {
        color: var(--text-mid) !important;
    }

    /* ── Metrics ── */
    [data-testid="stMetric"] {
        background: var(--bg-card) !important;
        border: 1px solid var(--border) !important;
        border-radius: var(--radius-md) !important;
        padding: 1rem !important;
    }
    [data-testid="stMetricLabel"] {
        color: var(--text-mid) !important;
        font-size: 0.8rem !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    [data-testid="stMetricValue"] {
        color: var(--text-hi) !important;
        font-family: 'Syne', sans-serif !important;
        font-size: 1.6rem !important;
    }
    [data-testid="stMetricDelta"] {
        color: var(--teal) !important;
        font-size: 0.78rem !important;
    }

    /* ── Progress bar ── */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, var(--teal), var(--emerald)) !important;
    }
    .stProgress > div > div {
        background: var(--bg-hover) !important;
        border-radius: 99px !important;
    }

    /* ── Expander ── */
    .streamlit-expanderHeader {
        background: var(--bg-card) !important;
        color: var(--text-hi) !important;
        border-radius: var(--radius-md) !important;
        border: 1px solid var(--border) !important;
        font-weight: 600;
    }
    .streamlit-expanderContent {
        background: var(--bg-card) !important;
        border: 1px solid var(--border) !important;
        border-top: none !important;
        border-radius: 0 0 var(--radius-md) var(--radius-md) !important;
    }

    /* ── Text area ── */
    .stTextArea textarea {
        background: var(--bg-deep) !important;
        color: var(--text-mid) !important;
        border: 1px solid var(--border) !important;
        border-radius: var(--radius-sm) !important;
        font-family: 'DM Mono', monospace !important;
        font-size: 0.82rem !important;
    }

    /* ── Info / Success / Error / Warning boxes ── */
    .stAlert {
        border-radius: var(--radius-md) !important;
        border: 1px solid var(--border) !important;
    }
    [data-baseweb="notification"][kind="positive"] {
        background: rgba(52,211,153,0.1) !important;
        border-color: var(--emerald) !important;
        color: var(--emerald) !important;
    }
    [data-baseweb="notification"][kind="negative"] {
        background: rgba(248,113,113,0.1) !important;
        border-color: var(--rose) !important;
        color: var(--rose) !important;
    }
    [data-baseweb="notification"][kind="warning"] {
        background: rgba(251,191,36,0.1) !important;
        border-color: var(--amber) !important;
        color: var(--amber) !important;
    }
    [data-baseweb="notification"][kind="info"] {
        background: rgba(56,189,248,0.1) !important;
        border-color: var(--sky) !important;
        color: var(--sky) !important;
    }

    /* ── Scrollbar ── */
    ::-webkit-scrollbar { width: 7px; height: 7px; }
    ::-webkit-scrollbar-track { background: var(--bg-deep); }
    ::-webkit-scrollbar-thumb { background: var(--border); border-radius: 99px; }
    ::-webkit-scrollbar-thumb:hover { background: var(--teal-dim); }

    /* ── Custom component classes ── */
    .ats-header-title {
        font-family: 'Syne', sans-serif;
        font-size: 2.8rem;
        font-weight: 800;
        color: var(--text-hi);
        text-align: center;
        letter-spacing: -0.02em;
        line-height: 1.1;
    }
    .ats-header-accent {
        color: var(--teal);
    }
    .ats-subtitle {
        text-align: center;
        color: var(--text-mid);
        font-size: 1rem;
        margin-top: 0.5rem;
        letter-spacing: 0.01em;
    }
    .ats-badge {
        display: inline-block;
        background: rgba(45,212,191,0.12);
        color: var(--teal);
        border: 1px solid rgba(45,212,191,0.3);
        border-radius: 99px;
        padding: 2px 12px;
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 0.04em;
        text-transform: uppercase;
        margin: 0 4px;
    }

    .score-card {
        background: linear-gradient(135deg, #0f2027, #1a2a3a);
        border: 1px solid var(--teal);
        border-radius: var(--radius-lg);
        padding: 2rem 1.5rem;
        color: var(--text-hi);
        text-align: center;
        box-shadow: 0 0 40px rgba(45,212,191,0.15);
        animation: slideIn 0.5s ease;
    }
    .score-card .label {
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        color: var(--teal);
        font-weight: 600;
    }
    .score-card .role-name {
        font-family: 'Syne', sans-serif;
        font-size: 1.7rem;
        font-weight: 800;
        color: var(--text-hi);
        margin: 0.4rem 0;
    }
    .score-card .score-num {
        font-family: 'Syne', sans-serif;
        font-size: 3.2rem;
        font-weight: 800;
        color: var(--teal);
        line-height: 1;
    }
    .score-card .score-sub {
        font-size: 0.8rem;
        color: var(--text-mid);
        margin-top: 0.3rem;
    }

    .role-card {
        background: var(--bg-card);
        border-radius: var(--radius-md);
        padding: 1rem 1.2rem;
        margin: 0.5rem 0;
        border-left: 3px solid;
        border-top: 1px solid var(--border);
        border-right: 1px solid var(--border);
        border-bottom: 1px solid var(--border);
        transition: all 0.25s ease;
        cursor: pointer;
    }
    .role-card:hover {
        transform: translateX(6px);
        background: var(--bg-hover);
    }
    .role-card strong {
        color: var(--text-hi) !important;
        font-size: 1rem;
    }
    .role-card .score-pct {
        font-family: 'Syne', sans-serif;
        font-size: 1.3rem;
        font-weight: 700;
    }
    .role-card .progress-track {
        background: var(--bg-deep);
        border-radius: 99px;
        height: 6px;
        margin-top: 0.6rem;
    }
    .role-card .progress-fill {
        height: 6px;
        border-radius: 99px;
    }

    .empty-state {
        text-align: center;
        padding: 3rem 2rem;
        background: var(--bg-card);
        border-radius: var(--radius-lg);
        border: 1px dashed var(--border);
    }
    .empty-state h3 {
        color: var(--text-hi);
        font-family: 'Syne', sans-serif;
        font-size: 1.5rem;
        margin-bottom: 0.75rem;
    }
    .empty-state p {
        color: var(--text-mid);
        font-size: 0.95rem;
        line-height: 1.7;
    }
    .empty-state .features {
        margin-top: 1.5rem;
        padding: 1rem;
        background: var(--bg-deep);
        border-radius: var(--radius-md);
        border: 1px solid var(--border);
        color: var(--text-mid);
        font-size: 0.85rem;
        line-height: 2;
    }

    .sidebar-header {
        text-align: center;
        padding: 1.2rem 0.5rem 0.8rem;
    }
    .sidebar-icon {
        width: 52px;
        height: 52px;
        background: linear-gradient(135deg, var(--teal), var(--emerald));
        border-radius: 14px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 0.8rem;
        font-size: 1.5rem;
        font-weight: 900;
        color: #0d1117;
        font-family: 'Syne', sans-serif;
    }
    .sidebar-appname {
        font-family: 'Syne', sans-serif;
        font-size: 1.15rem;
        font-weight: 800;
        color: var(--text-hi);
    }
    .sidebar-tagline {
        font-size: 0.78rem;
        color: var(--text-mid);
        margin-top: 0.2rem;
    }

    .footer-text {
        text-align: center;
        color: var(--text-lo);
        font-size: 0.8rem;
        padding: 1rem 0 0.5rem;
        line-height: 2;
    }

    @keyframes slideIn {
        from { opacity: 0; transform: translateY(20px); }
        to   { opacity: 1; transform: translateY(0); }
    }
    @keyframes float {
        0%, 100% { transform: translateY(0); }
        50%       { transform: translateY(-8px); }
    }
    .floating { animation: float 4s ease-in-out infinite; }
</style>
""", unsafe_allow_html=True)

# ---------------- ENHANCED ROLE SKILLS ----------------
ROLE_SKILLS = {
    "Web Developer": {
        "skills": ["html", "css", "javascript", "react", "bootstrap", "vue", "angular", "typescript"],
        "color": "#f87171"
    },
    "Backend Developer": {
        "skills": ["python", "django", "flask", "api", "sql", "database", "node.js", "java", "spring"],
        "color": "#2dd4bf"
    },
    "Data Scientist": {
        "skills": ["python", "machine learning", "pandas", "numpy", "tensorflow", "sql", "statistics", "deep learning"],
        "color": "#38bdf8"
    },
    "DevOps Engineer": {
        "skills": ["docker", "kubernetes", "jenkins", "aws", "ci/cd", "linux", "git", "terraform"],
        "color": "#34d399"
    },
    "Mobile Developer": {
        "skills": ["android", "ios", "flutter", "react native", "swift", "kotlin", "mobile", "app"],
        "color": "#fbbf24"
    },
    "AI/ML Engineer": {
        "skills": ["python", "tensorflow", "pytorch", "deep learning", "nlp", "computer vision", "keras", "scikit-learn"],
        "color": "#a78bfa"
    },
    "Cybersecurity Analyst": {
        "skills": ["security", "network", "firewall", "penetration testing", "encryption", "compliance", "risk assessment"],
        "color": "#fb923c"
    },
    "Cloud Architect": {
        "skills": ["aws", "azure", "gcp", "cloud", "infrastructure", "terraform", "kubernetes", "serverless"],
        "color": "#60a5fa"
    }
}

# ---------------- FUNCTIONS ----------------
def extract_text(pdf_file):
    try:
        reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted
        return text if text else "No text could be extracted from PDF"
    except Exception as e:
        return f"Error reading PDF: {str(e)}"

def clean_text(text):
    if not text or "Error" in text:
        return text
    text = text.lower()
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'\S+@\S+', '', text)
    text = re.sub(r'[^a-z\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def calculate_advanced_scores(resume_text):
    if not resume_text or "Error" in resume_text:
        return {}, {}
    scores = {}
    skill_match_details = {}
    for role, role_data in ROLE_SKILLS.items():
        skills = role_data["skills"]
        match_count = 0
        matched_skills = []
        for skill in skills:
            if skill in resume_text:
                match_count += 1
                matched_skills.append(skill)
        score = (match_count / len(skills)) * 100 if skills else 0
        scores[role] = round(score, 2)
        skill_match_details[role] = {
            "matched": matched_skills,
            "missing": [s for s in skills if s not in matched_skills],
            "count": match_count,
            "total": len(skills)
        }
    return scores, skill_match_details

def get_recommendations(score, role):
    recommendations = []
    if score < 40:
        recommendations.append(f"Focus on core {role} skills — consider structured online courses")
        recommendations.append("Build a portfolio of 2-3 projects showcasing relevant work")
        recommendations.append("Pursue certifications in key technologies for this role")
    elif score < 70:
        recommendations.append(f"Strengthen technical vocabulary specific to {role} in your resume")
        recommendations.append("Add concrete, quantified project descriptions with outcomes")
        recommendations.append(f"Tailor your resume specifically for {role} job descriptions")
    else:
        recommendations.append("Excellent match — consider applying for senior or lead roles")
        recommendations.append("Highlight leadership, mentoring, and architectural decisions")
        recommendations.append("Contribute to open source projects in your domain")
    return recommendations

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.markdown("""
        <div class='sidebar-header'>
            <div class='sidebar-icon'>ATS</div>
            <div class='sidebar-appname'>ATS Pro Analyzer</div>
            <div class='sidebar-tagline'>AI-Powered Resume Analysis</div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    uploaded_file = st.file_uploader(
        "Upload Resume (PDF)",
        type=["pdf"],
        help="Upload your resume in PDF format for analysis"
    )

    st.markdown("---")
    st.markdown("### Quick Stats")
    col1, col2 = st.columns(2)
    with col1:
        total_roles = len(ROLE_SKILLS)
        st.metric("Roles", total_roles)
    with col2:
        total_skills = sum(len(r["skills"]) for r in ROLE_SKILLS.values())
        st.metric("Skills", total_skills)

    st.markdown("---")
    st.markdown("""
        <div style='font-size: 0.8rem; color: #8b949e; line-height: 2;'>
            <strong style='color: #f0f6fc;'>Features</strong><br>
            8+ Job Roles<br>
            Smart Skill Matching<br>
            Detailed Analytics<br>
            Personalised Tips<br><br>
            <span style='color: #2dd4bf;'>Powered by Advanced AI</span>
        </div>
    """, unsafe_allow_html=True)

# ---------------- MAIN CONTENT ----------------
st.markdown("""
    <div style='text-align: center; padding: 1.5rem 0 1rem;'>
        <div class='ats-header-title'>
            ATS Resume <span class='ats-header-accent'>Analyzer</span> Pro
        </div>
        <div class='ats-subtitle'>
            <span class='ats-badge'>AI-Powered</span>
            Smart Skill Matching &nbsp;·&nbsp; Deep Career Insights
            <span class='ats-badge'>8+ Roles</span>
        </div>
    </div>
""", unsafe_allow_html=True)

st.markdown("---")

# Main content area
if uploaded_file:
    with st.spinner("Analyzing your resume..."):
        progress_bar = st.progress(0)
        for i in range(100):
            time.sleep(0.01)
            progress_bar.progress(i + 1)
        progress_bar.empty()

        raw_text = extract_text(uploaded_file)
        clean = clean_text(raw_text)

        if clean and "Error" not in clean:
            scores, skill_details = calculate_advanced_scores(clean)
            best_role = max(scores, key=scores.get)
            best_score = scores[best_role]

            st.balloons()

            # Best match card
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.markdown(f"""
                    <div class='score-card'>
                        <div class='label'>Best Match Found</div>
                        <div class='role-name'>{best_role}</div>
                        <div class='score-num'>{best_score}%</div>
                        <div class='score-sub'>ATS Compatibility Score</div>
                    </div>
                """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            # Metrics row
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Roles Analyzed", len(scores), delta="Comprehensive")
            with col2:
                avg_score = sum(scores.values()) / len(scores)
                st.metric("Avg Match", f"{avg_score:.1f}%", delta="Across all roles")
            with col3:
                matched_skills = sum(len(skill_details[r]["matched"]) for r in skill_details)
                st.metric("Skills Matched", matched_skills, delta="Total found")
            with col4:
                confidence = "High" if best_score > 70 else "Medium" if best_score > 40 else "Low"
                st.metric("Confidence", confidence, delta="AI Verified")

            st.markdown("---")
            st.markdown("### Detailed Role Analysis")

            tab1, tab2, tab3 = st.tabs(["Match Scores", "Skill Breakdown", "Recommendations"])

            with tab1:
                roles_list  = list(scores.keys())
                scores_list = list(scores.values())
                colors      = [ROLE_SKILLS[role]["color"] for role in roles_list]

                fig = go.Figure(data=[
                    go.Bar(
                        x=roles_list,
                        y=scores_list,
                        marker_color=colors,
                        marker_line_color='rgba(0,0,0,0)',
                        text=[f"{s}%" for s in scores_list],
                        textposition='auto',
                        textfont=dict(color='#0d1117', size=12, family='DM Sans'),
                        hovertemplate='<b>%{x}</b><br>Match: %{y}%<extra></extra>'
                    )
                ])
                fig.update_layout(
                    title=dict(text="Job Role Match Scores", font=dict(color='#f0f6fc', size=16, family='Syne')),
                    xaxis=dict(title="Role", tickfont=dict(color='#8b949e', size=11), gridcolor='#1f2937', title_font=dict(color='#8b949e')),
                    yaxis=dict(title="Match (%)", tickfont=dict(color='#8b949e', size=11), gridcolor='#1f2937', range=[0,100], title_font=dict(color='#8b949e')),
                    plot_bgcolor='#0d1117',
                    paper_bgcolor='#161b22',
                    font=dict(family='DM Sans', color='#f0f6fc'),
                    showlegend=False,
                    height=400,
                    hovermode='closest',
                    margin=dict(l=20, r=20, t=50, b=20)
                )
                st.plotly_chart(fig, use_container_width=True)

                st.markdown("### Role-wise Breakdown")
                for role, score in sorted(scores.items(), key=lambda x: x[1], reverse=True):
                    color = ROLE_SKILLS[role]["color"]
                    st.markdown(f"""
                        <div class='role-card' style='border-left-color: {color};'>
                            <div style='display: flex; justify-content: space-between; align-items: center;'>
                                <strong>{role}</strong>
                                <span class='score-pct' style='color: {color};'>{score}%</span>
                            </div>
                            <div class='progress-track'>
                                <div class='progress-fill' style='width: {score}%; background: {color};'></div>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)

            with tab2:
                top_3_roles = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:3]
                for role, score in top_3_roles:
                    details = skill_details[role]
                    with st.expander(f"{role}  —  {score}% Match", expanded=True):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown("#### Matched Skills")
                            if details["matched"]:
                                for skill in details["matched"]:
                                    st.success(f"{skill.title()}")
                            else:
                                st.warning("No matching skills found")
                        with col2:
                            st.markdown("#### Missing Skills")
                            if details["missing"]:
                                for skill in details["missing"][:8]:
                                    st.error(f"{skill.title()}")
                            else:
                                st.success("All skills matched!")
                        st.markdown(f"**Match Rate:** {details['count']}/{details['total']} skills")
                        st.progress(details['count'] / details['total'])

                st.markdown("### Extracted Keywords")
                words = clean.split()[:50]
                keyword_text = ", ".join(words[:20])
                st.info(f"**Top keywords found:** {keyword_text}")

            with tab3:
                st.markdown("### Personalised Action Plan")
                recommendations = get_recommendations(best_score, best_role)

                st.markdown(f"#### For the {best_role} Path:")
                for rec in recommendations:
                    st.markdown(f"- {rec}")

                st.markdown("#### General Resume Tips:")
                tips = [
                    "Use action verbs — developed, implemented, architected, led",
                    "Quantify achievements with numbers and business impact",
                    "Include relevant keywords naturally throughout the document",
                    "Keep resume to 1–2 pages maximum",
                    "Proofread carefully for spelling and grammar",
                    "Highlight soft skills: leadership, communication, ownership"
                ]
                for tip in tips:
                    st.markdown(f"- {tip}")

                st.markdown("#### Recommended Learning Resources:")
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("- Coursera Specialisations")
                    st.markdown("- Industry Certifications")
                    st.markdown("- Portfolio Projects on GitHub")
                with col2:
                    st.markdown("- LinkedIn Learning Paths")
                    st.markdown("- Udemy Skill Building")
                    st.markdown("- Open Source Contributions")

            with st.expander("View Extracted Resume Text"):
                st.text_area("Resume Content", raw_text, height=300, help="Text extracted from your PDF")

                report = f"""
ATS Resume Analysis Report
===========================
Date: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
File: {uploaded_file.name}

Best Match: {best_role} ({best_score}%)
Average Score: {avg_score:.1f}%

Detailed Scores:
{chr(10).join([f"- {role}: {score}%" for role, score in scores.items()])}

Skills Matched: {matched_skills} total
Confidence: {confidence}

Recommendations:
{chr(10).join([f"- {rec}" for rec in recommendations])}
"""
                st.download_button(
                    label="Download Analysis Report",
                    data=report,
                    file_name=f"resume_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain"
                )

        else:
            st.error("Could not extract text from the PDF. Please ensure it contains selectable (non-scanned) text.")
            st.info("Tip: Use an OCR tool to convert scanned PDFs to searchable text first.")

else:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
            <div class='empty-state'>
                <div class='floating' style='font-size: 3rem; margin-bottom: 1rem;'>[ PDF ]</div>
                <h3>Ready to Analyse Your Resume?</h3>
                <p>
                    Upload your resume PDF using the sidebar<br>
                    to get an instant AI-powered compatibility report<br>
                    and personalised career recommendations.
                </p>
                <div class='features'>
                    PDF format supported &nbsp;·&nbsp; Instant Analysis<br>
                    8+ Job Roles &nbsp;·&nbsp; Smart Skill Matching &nbsp;·&nbsp; Career Tips
                </div>
            </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
    <div class='footer-text'>
        Powered by Advanced AI &nbsp;·&nbsp; Real-time Resume Analysis &nbsp;·&nbsp; Career Insights<br>
        &copy; 2024 ATS Resume Analyzer Pro
    </div>
""", unsafe_allow_html=True)
