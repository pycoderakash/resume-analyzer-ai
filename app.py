import streamlit as st
import re
import PyPDF2
import matplotlib.pyplot as plt

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    color: white;
}

h1, h2, h3 {
    color: #00ffd5;
}

.stButton>button {
    background-color: #00ffd5;
    color: black;
    border-radius: 10px;
    padding: 10px;
    font-weight: bold;
}

.stTextArea textarea {
    border-radius: 10px;
}

.card {
    background-color: #1e1e2f;
    padding: 15px;
    border-radius: 12px;
    margin: 10px 0;
}
</style>
""", unsafe_allow_html=True)

st.set_page_config(page_title="AI Resume Analyzer PRO MAX", layout="wide")

# -------------------- SKILL DATABASE --------------------
skill_db = {
"computer_science": {
    "programming": {
        "python": {"weight": 10, "aliases": ["py"]},
        "java": {"weight": 9, "aliases": []},
        "c++": {"weight": 8, "aliases": ["cpp"]},
        "javascript": {"weight": 9, "aliases": ["js"]}
    },
    "web_dev": {
        "html": {"weight": 6, "aliases": []},
        "css": {"weight": 6, "aliases": []},
        "react": {"weight": 8, "aliases": []},
        "node.js": {"weight": 8, "aliases": ["node"]}
    },
    "ai_ml": {
        "machine learning": {"weight": 10, "aliases": ["ml"]},
        "deep learning": {"weight": 10, "aliases": ["dl"]},
        "data science": {"weight": 9, "aliases": []},
        "nlp": {"weight": 9, "aliases": ["natural language processing"]}
    },
    "database": {
        "mysql": {"weight": 7, "aliases": []},
        "mongodb": {"weight": 7, "aliases": []}
    }
},
"electrical": {
    "core": {
        "circuit design": {"weight": 9, "aliases": []},
        "power systems": {"weight": 9, "aliases": []},
        "control systems": {"weight": 8, "aliases": []}
    }
},
"mechanical": {
    "design": {
        "autocad": {"weight": 8, "aliases": []},
        "solidworks": {"weight": 9, "aliases": []},
        "catia": {"weight": 9, "aliases": []}
    },
    "core": {
        "thermodynamics": {"weight": 8, "aliases": []},
        "fluid mechanics": {"weight": 8, "aliases": []}
    }
},
"civil": {
    "design": {
        "etabs": {"weight": 9, "aliases": []},
        "staad": {"weight": 9, "aliases": []}
    },
    "core": {
        "surveying": {"weight": 7, "aliases": []},
        "construction management": {"weight": 8, "aliases": []}
    }
},
"electronics": {
    "core": {
        "vlsi": {"weight": 10, "aliases": []},
        "microcontroller": {"weight": 9, "aliases": []},
        "iot": {"weight": 9, "aliases": ["internet of things"]}
    }
},
"soft_skills": {
    "general": {
        "communication": {"weight": 7, "aliases": []},
        "teamwork": {"weight": 7, "aliases": []},
        "leadership": {"weight": 8, "aliases": []},
        "problem solving": {"weight": 9, "aliases": []}
    }
},
"trending": {
    "future": {
        "artificial intelligence": {"weight": 10, "aliases": ["ai"]},
        "cloud computing": {"weight": 9, "aliases": ["aws", "azure"]},
        "cybersecurity": {"weight": 9, "aliases": []},
        "blockchain": {"weight": 8, "aliases": []}
    }
}
}

# -------------------- JOB ROLES DATABASE --------------------
job_roles_db = {
"computer_science": {
    "Data Scientist": {"python":10,"machine learning":10,"data science":10,"sql":9,"statistics":9,"deep learning":8,"nlp":8},
    "Web Developer": {"html":10,"css":10,"javascript":10,"react":9,"node.js":8,"mongodb":7},
    "Software Engineer": {"java":9,"python":8,"c++":8,"data structures":10,"algorithms":10,"oop":9},
    "AI Engineer": {"python":10,"machine learning":10,"deep learning":10,"tensorflow":9,"pytorch":9,"nlp":8}
},
"electrical": {
    "Electrical Engineer": {"circuit design":10,"power systems":10,"control systems":9,"matlab":8,"simulink":8},
    "Embedded Engineer": {"embedded systems":10,"microcontroller":10,"c programming":9,"arduino":8,"iot":8}
},
"mechanical": {
    "Design Engineer": {"solidworks":10,"catia":10,"autocad":9,"machine design":9},
    "Production Engineer": {"manufacturing":10,"cnc programming":9,"quality control":9}
},
"civil": {
    "Structural Engineer": {"etabs":10,"staad":10,"structural analysis":10,"autocad":8},
    "Site Engineer": {"construction management":10,"surveying":9,"quantity surveying":9}
},
"electronics": {
    "VLSI Engineer": {"vlsi":10,"verilog":10,"digital design":9},
    "IoT Engineer": {"iot":10,"embedded systems":9,"arduino":9,"sensor integration":8}
},
"chemical": {
    "Process Engineer": {"process design":10,"thermodynamics":9,"aspen plus":9}
},
"biotech": {
    "Biotech Engineer": {"bioinformatics":10,"genetic engineering":10,"pcr":9,"cell culture":9}
},
"common_roles": {
    "Data Analyst": {"excel":10,"sql":10,"python":8,"power bi":9,"tableau":9},
    "DevOps Engineer": {"docker":10,"kubernetes":10,"linux":9,"aws":9,"ci/cd":9}
}
}

# -------------------- UI --------------------

# Title
st.markdown(
    "<h1 style='text-align:center;'>🚀 Resume Analyzer AI 🤖</h1>",
    unsafe_allow_html=True
)

st.markdown("### 📄 Upload or Paste Your Resume")

# Input Section
col1, col2 = st.columns(2)

with col1:
    uploaded_file = st.file_uploader("📂 Upload PDF Resume", type=["pdf"])

with col2:
    resume_input = st.text_area("📝 Paste Resume Text")

# Sidebar Settings
st.sidebar.title("⚙️ Settings")

field = st.sidebar.selectbox(
    "Select Field",
    list(job_roles_db.keys())
)

role = st.sidebar.selectbox(
    "Select Role",
    list(job_roles_db[field].keys())
)

# -------------------- RESUME TEXT PROCESSING --------------------

resume_text = ""

# PDF Reading
if uploaded_file is not None:
    try:
        reader = PyPDF2.PdfReader(uploaded_file)
        for page in reader.pages:
            text = page.extract_text()
            if text:
                resume_text += text + " "
    except Exception as e:
        st.warning("⚠️ Error reading PDF")

# Manual Input
if resume_input:
    resume_text += resume_input + " "

# Clean text
resume_text = resume_text.strip()

# -------------------- ANALYSIS --------------------
if st.button("🚀 Analyze Resume"):

    with st.spinner("🤖 AI is analyzing your resume..."):

        if not resume_text.strip():
            st.error("Please provide resume")
            st.stop()

        resume_text = resume_text.lower()
        found = set()

        for category in skill_db.values():
            for subcat in category.values():
                for skill, data in subcat.items():

                    if re.search(r"\b" + re.escape(skill) + r"\b", resume_text):
                        found.add(skill)

                    for alias in data["aliases"]:
                        if re.search(r"\b" + re.escape(alias) + r"\b", resume_text):
                            found.add(skill)

        found = list(found)

        total_score = 0
        max_score = 0

        for category in skill_db.values():
            for subcat in category.values():
                for skill, data in subcat.items():
                    max_score += data["weight"]
                    if skill in found:
                        total_score += data["weight"]

        score = int((total_score / max_score) * 100) if max_score else 0

        # ✅ FIXED ROLE SCORE
        role_data = job_roles_db[field][role]
        total_role_weight = sum(role_data.values())

        if total_role_weight == 0:
            role_score = 0
        else:
            role_score = int(
                (sum(weight for skill, weight in role_data.items() if skill in found) /
                 total_role_weight) * 100
            )

        # -------------------- OUTPUT --------------------
        st.markdown("## 📊 AI Analysis Dashboard")

        col1, col2, col3 = st.columns(3)

        col1.markdown(f"<div class='card'><h3>Overall Score</h3><p>{score}%</p></div>", unsafe_allow_html=True)
        col2.markdown(f"<div class='card'><h3>Role Match</h3><p>{role_score}%</p></div>", unsafe_allow_html=True)
        col3.markdown(f"<div class='card'><h3>Skills Found</h3><p>{len(found)}</p></div>", unsafe_allow_html=True)

        st.progress(score)

        # -------------------- GRAPH --------------------
        labels, values = [], []

        for skill in found:
            for category in skill_db.values():
                for subcat in category.values():
                    if skill in subcat:
                        labels.append(skill)
                        values.append(subcat[skill]["weight"])

        if values:
            st.markdown("### 📈 Skill Strength Graph")

            plt.figure()
            top_skills = sorted(zip(labels, values), key=lambda x: x[1], reverse=True)[:10]

            labels = [i[0] for i in top_skills]
            values = [i[1] for i in top_skills]

            plt.bar(labels, values)
            plt.xticks(rotation=45)
            plt.tight_layout()

            st.pyplot(plt)

        # -------------------- SKILLS OUTPUT --------------------
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("🟢 Found Skills")
            if found:
                for s in found:
                    st.success(s)
            else:
                st.info("No skills detected")

        with col2:
            st.subheader("🔴 Skills to Improve")

            missing = [m for m in role_data if m not in found]

            if missing:
                for m in missing:
                    st.error(m)
            else:
                st.success("All required skills present 🎉")

    

                        
# -------------------- FOOTER --------------------

st.markdown("---")

st.markdown("""
<div style='text-align: center; padding: 10px;'>
    <p style='color: #00ffd5; font-size: 16px;'>
        👨‍💻 Developed by <b>Akash Rai</b>
    </p>
    <p style='color: gray; font-size: 13px;'>
        🚀 AI Resume Analyzer | Built with Python & Streamlit
    </p>
</div>
""", unsafe_allow_html=True)
