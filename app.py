import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import joblib
import spacy

# Load data and model
df = pd.read_csv('dataset_cultureMonkey.csv')
import spacy.cli
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    spacy.cli.download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

# Normalize column names
df.columns = df.columns.str.strip().str.lower()
if 'description' in df.columns:
    df.rename(columns={'description': 'job_description'}, inplace=True)

df['job_description'] = df['job_description'].astype(str).str.lower()

# Skill keywords
skill_keywords = [
    'python', 'java', 'sql', 'aws', 'azure', 'gcp', 'docker',
    'kubernetes', 'pytorch', 'tensorflow', 'scikit-learn',
    'spark', 'hadoop', 'nlp', 'machine learning', 'deep learning'
]

def extract_skills(text):
    return [kw for kw in skill_keywords if kw in text]

# Skill trend logic (can replace with real model)
def get_trend_score(skill):
    common_skills = ['python', 'sql', 'aws', 'tensorflow', 'docker']
    if skill in common_skills:
        return 'established', 0.8
    else:
        return 'emerging', 0.5

# Sidebar
st.sidebar.title("Job Market Analysis")
page = st.sidebar.radio("Go to", ["📊 Dashboard", "🧠 Skill Trend Detector", "📄 About"])

# Dashboard Page
if page == "📊 Dashboard":
    st.title("📊 Job Market Skill Dashboard")
    st.markdown("### Skill distribution by seniority")

    entry_roles = df[df['seniority'].str.contains('entry', case=False, na=False)]
    senior_roles = df[df['seniority'].str.contains('senior|lead|manager', case=False, na=False)]

    entry_skills = Counter(entry_roles['job_description'].apply(extract_skills).explode())
    senior_skills = Counter(senior_roles['job_description'].apply(extract_skills).explode())

    common_skills = list(set(entry_skills) | set(senior_skills))

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar([x + ' (Entry)' for x in entry_skills], entry_skills.values(), color='blue', alpha=0.6)
    ax.bar([x + ' (Senior)' for x in senior_skills], senior_skills.values(), color='orange', alpha=0.6)
    st.pyplot(fig)

# Skill Trend Detector Page
elif page == "🧠 Skill Trend Detector":
    st.title("🧠 Skill Trend Detector")

    jd = st.text_area("Paste a job description here:")
    if st.button("Detect Skills"):
        skills = extract_skills(jd.lower())
        results = []
        for skill in skills:
            label, score = get_trend_score(skill)
            results.append({"Skill": skill, "Category": label, "Trend Score": score})
        
        st.table(pd.DataFrame(results))

# About Page
else:
    st.title("About the Project")
    st.markdown("""
    This app was built for the **CultureMonkey AI/ML Junior Developer Assignment**.
    
    Features:
    - Data analysis of job postings
    - Comparison of skill trends by seniority
    - Skill trend detection from job descriptions
    - Interactive visualizations

    Tech Stack:
    - Streamlit
    - Python (Pandas, Seaborn, spaCy)
    - Scikit-learn (optional TF-IDF model)
    """)
