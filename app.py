import streamlit as st
import requests

# Title
st.set_page_config(page_title="Skill Trend Detector", layout="centered")
st.title("🧠 Skill Trend Detector")

# Text area for job description
description = st.text_area("📄 Paste a Job Description Below")

# Set the URL of your FastAPI backend deployed on Render
API_URL = "https://skill-trend-api.onrender.com/skill-trend"  # ← ✅ Replace with your actual FastAPI URL if different

# Button action
if st.button("🔍 Analyze Skills"):
    if description.strip():
        try:
            with st.spinner("Analyzing..."):
                response = requests.post(API_URL, json={"job_description": description})
                if response.status_code == 200:
                    result = response.json()
                    st.success("✅ Skills extracted successfully!")
                    st.subheader("📋 Detected Skills:")
                    for item in result.get("detected_skills", []):
                        st.write(f"🔹 `{item['skill']}` → *{item['category']}* (score: {item['trend_score']})")
                else:
                    st.error(f"API Error: {response.status_code} - {response.text}")
        except requests.exceptions.RequestException as e:
            st.error(f"Connection failed: {e}")
    else:
        st.warning("⚠️ Please enter a job description.")
