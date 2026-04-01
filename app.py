"""
app.py
------
The main Frontend application file for Clino Health Innovation.
This file handles the Streamlit user interface, injects custom CSS 
for styling, captures user symptom input, and displays the final 
AI-generated medical report.
"""

import streamlit as st
import json
from api import configure_gemini, analyze_symptoms

# ─── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Clino Health Innovation",
    page_icon="🏥",
    layout="centered"
)

# ─── Configure Gemini ──────────────────────────────────────────────────────────
try:
    configure_gemini()
except ValueError as e:
    st.error(f"❌ {str(e)}")
    st.stop()

# ─── Custom CSS ────────────────────────────────────────────────────────────────
with open("style.css", "r") as css_file:
    st.markdown(f"<style>{css_file.read()}</style>", unsafe_allow_html=True)

# ─── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="main-header">
    <h1>🏥 Clino Health Innovation</h1>
    <p>AI-Powered Symptom Checker &amp; Disease Predictor</p>
</div>
""", unsafe_allow_html=True)

# ─── Input Section ─────────────────────────────────────────────────────────────
st.markdown('<p class="section-label">📝 Describe Your Symptoms</p>', unsafe_allow_html=True)
st.markdown('<p class="section-sub">Be as detailed as possible — duration, severity, and any other details help improve accuracy.</p>', unsafe_allow_html=True)

symptoms = st.text_area(
    label="Describe your symptoms",
    label_visibility="collapsed",
    placeholder="e.g. I have had a high fever, sore throat, body aches, and fatigue for the past 2 days...",
    height=170,
    key="symptom_input"
)

# ─── Predict Button ─────────────────────────────────────────────────────────────
col1, col2, col3 = st.columns([0.8, 2.4, 0.8])
with col2:
    predict_btn = st.button("🔍  Predict My Condition", use_container_width=True)

# ─── On Button Click ────────────────────────────────────────────────────────────
if predict_btn:
    if not symptoms.strip():
        st.warning("⚠️ Please describe your symptoms before clicking Predict.")
    else:
        with st.spinner("🤖 Analyzing your symptoms with Gemini AI..."):
            try:
                result = analyze_symptoms(symptoms)

                # 🛑 THE NEW GUARDRAIL: Intercept Invalid Input
                if "Invalid Input" in result.get('predicted_disease', ''):
                    st.warning(f"⚠️ {result.get('predicted_disease', '')}")
                
                # ✅ If the input IS valid, draw the full health report
                else:
                    st.markdown("<hr>", unsafe_allow_html=True)
                    st.markdown('<p class="report-title">🩺 Your Health Report</p>', unsafe_allow_html=True)

                    # 🚨 1. EMERGENCY OVERRIDE
                    if result.get('emergency_flag', False):
                        st.error(f"**🚨 {result.get('emergency_note', 'Please seek immediate medical attention.')}**")

                    # 🦠 2. Predicted Disease & Severity
                    severity = result.get('severity_level', 'Unknown')
                    sev_color = "#1e8449" if "Mild" in severity else "#d35400" if "Moderate" in severity else "#c0392b"
                    
                    st.markdown(f"""
                    <div class="result-card disease-card">
                        <p class="card-heading">🦠 &nbsp;Predicted Condition</p>
                        <p style="font-weight: 700; color: {sev_color}; font-size: 0.9rem; margin-top: -8px; margin-bottom: 10px;">
                            Severity Level: {severity}
                        </p>
                        <div class="card-body">{result.get('predicted_disease', '')}</div>
                    </div>
                    """, unsafe_allow_html=True)

                    # 🌿 3. Home Remedies
                    if len(result.get('home_remedies', [])) == 0:
                        remedies_li = "<li><em>No home remedies recommended for this condition. Please seek medical help.</em></li>"
                    else:
                        remedies_li = "".join([f"<li>{r}</li>" for r in result.get('home_remedies', [])])
                        st.markdown(f"""
                        <div class="result-card remedies-card">
                            <p class="card-heading">🌿 &nbsp;Home Remedies</p>
                            <div class="card-body"><ul>{remedies_li}</ul></div>
                        </div>
                        """, unsafe_allow_html=True)

                    # ⚠️ 4. Precautions
                    precautions_li = "".join([f"<li>{p}</li>" for p in result.get('precautions', [])])
                    st.markdown(f"""
                    <div class="result-card precautions-card">
                        <p class="card-heading">⚠️ &nbsp;Precautions</p>
                        <div class="card-body"><ul>{precautions_li}</ul></div>
                    </div>
                    """, unsafe_allow_html=True)

                    # 🏥 5. When to See a Doctor
                    st.markdown(f"""
                    <div class="result-card" style="border-left-color: #e67e22;">
                        <p class="card-heading" style="color: #e67e22;">🏥 &nbsp;When to see a Doctor</p>
                        <div class="card-body">{result.get('when_to_see_doctor', '')}</div>
                    </div>
                    """, unsafe_allow_html=True)

                    # 💡 6. Fun Health Fact
                    st.info(f"**💡 Fun Fact:** {result.get('fun_health_fact', '')}")

                    # ⚕️ 7. Dynamic AI Disclaimer
                    st.markdown(f"""
                    <div class="disclaimer">
                        {result.get('disclaimer', '')}
                    </div>
                    """, unsafe_allow_html=True)

            except json.JSONDecodeError:
                st.error("⚠️ Could not read the AI response. Please try again.")
            except Exception as e:
                st.error(f"❌ Something went wrong: {str(e)}")

# ─── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    © 2026 Clino Health Innovation &nbsp;|&nbsp; Powered by Gemini AI &nbsp;|&nbsp; For demonstration purposes only
</div>
""", unsafe_allow_html=True)