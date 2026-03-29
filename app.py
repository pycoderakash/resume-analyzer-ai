import streamlit as st
import re
import PyPDF2
import matplotlib.pyplot as plt

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
st.title("🚀 Resume Analyzer AI 🤖")

col1, col2 = st.columns(2)
uploaded_file = col1.file_uploader("📄 Upload Resume (PDF)", type=["pdf"])
resume_input = col2.text_area("Or Paste Resume Text")

field = st.selectbox("Select Field", list(job_roles_db.keys()))
role = st.selectbox("Select Role", list(job_roles_db[field].keys()))

resume_text = ""

if uploaded_file:
    try:
        reader = PyPDF2.PdfReader(uploaded_file)
        for page in reader.pages:
            text = page.extract_text()
            if text:
                resume_text += text
    except:
        st.warning("PDF read issue")

if resume_input:
    resume_text += resume_input

# -------------------- ANALYSIS --------------------
if st.button("Analyze"):

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

    role_data = job_roles_db[field][role]

    role_score = int(
        (sum(weight for skill, weight in role_data.items() if skill in found) /
         sum(role_data.values())) * 100
    ) if role_data else 0

    # -------------------- OUTPUT --------------------
    st.subheader("📊 Scores")

    col1, col2 = st.columns(2)
    col1.metric("Overall Score", f"{score}%")
    col2.metric("Role Match Score", f"{role_score}%")

    st.progress(score)

    # GRAPH
    labels, values = [], []
    for skill in found:
        for category in skill_db.values():
            for subcat in category.values():
                if skill in subcat:
                    labels.append(skill)
                    values.append(subcat[skill]["weight"])

    if values:
        plt.figure()
        plt.bar(labels, values)
        plt.xticks(rotation=45)
        st.pyplot(plt)

    # SKILLS
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🟢 Found Skills")
        for s in found:
            st.success(s)

    with col2:
        st.subheader("🔴 Missing Skills")
        for m in role_data:
            if m not in found:
                st.error(m)
