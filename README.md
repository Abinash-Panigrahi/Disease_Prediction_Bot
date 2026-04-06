# Clino Health — AI Disease Prediction System

**Clino Health Innovation** | Internal Repository | Confidential

---

## Overview

Clino Health is an AI-powered healthcare assistant designed to analyze patient-described symptoms and return a structured medical report in real time. The system leverages Google Gemini AI to deliver condition predictions, severity grading, home remedies, and precautionary guidance — all through a clean, accessible web interface.

---

## Live Application

| | |
|---|---|
| **Production URL** | `https://company-domain.com` *(update after deployment)* |
| **Event QR Code** | Located in `assets/clino_qr.png` *(regenerate after deployment)* |

---

## Key Features

- **AI-Powered Diagnosis** — Gemini AI analyzes symptoms with clinical accuracy
- **Natural Language Input** — Accepts both medical terminology and everyday language
- **Emergency Detection** — Instantly flags life-threatening symptoms with a high-priority alert
- **Severity Grading** — Classifies conditions as Mild / Moderate / Severe with visual indicators
- **Home Remedies** — Five safe, condition-specific remedies per diagnosis
- **Smart Precautions** — Clear DO's and DON'Ts tailored to the predicted condition
- **Doctor Referral Guidance** — Specific warning signs that indicate when to seek professional care
- **Secure API Management** — API key handled via environment secrets, never hardcoded

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend & Server | Streamlit |
| AI Model | gemini-2.5-flash |
| AI SDK | `google-genai` |
| Language | Python 3.10+ |
| Styling | Custom CSS |
| Secret Management | Environment-based secrets |
| Deployment | Company Production Server |

---

## Project Structure

```
Disease_Prediction_Bot/
│
├── app.py                        # Streamlit UI — input, HTML rendering, error handling
├── api.py                        # Gemini API — client configuration, model call, response parsing
├── prompt.py                     # Prompt engine — XML-structured, dual-format medical responses
├── style.css                     # All custom CSS — separated from application logic
│
├── requirements.txt              # Project dependencies
├── .gitignore                    # Excludes .venv, secrets.toml, __pycache__
│
└── .streamlit/
    ├── config.toml               # Streamlit theme configuration
    ├── secrets.toml              # ⚠️ Real API key — never commit this file
    └── secrets.toml.example      # ✅ Safe placeholder — committed to repository
│
└── assets/
    └── clino_qr.png              # QR code for event-based app access
```

---

## Architecture

Each module follows a single-responsibility principle:

```
app.py  ──imports──▶  api.py  ──imports──▶  prompt.py
   │                     │                      │
   │                     │                      │
UI & error display    Gemini API call       XML prompt engine
st.error()            raise ValueError()    build_prompt()
st.spinner()          json.loads()          layman + medical format
HTML card injection   os.environ bridge
```

---

## Local Development Setup

### 1. Clone the Repository

```bash
git clone https://gitlab.com/your-company/healthcare-bot.git
cd healthcare-bot
```

### 2. Create & Activate Virtual Environment

```bash
python -m venv .venv
```

```bash
# Mac / Linux
source .venv/bin/activate

# Windows (Command Prompt)
.venv\Scripts\activate

# Windows (PowerShell)
.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure API Key

```bash
# Mac / Linux
cp .streamlit/secrets.toml.example .streamlit/secrets.toml

# Windows
copy .streamlit\secrets.toml.example .streamlit\secrets.toml
```

Open `.streamlit/secrets.toml` then add your key:

```toml
GEMINI_API_KEY = "your_gemini_api_key_here"
```

> Obtain a Gemini API key from [aistudio.google.com](https://aistudio.google.com)

### 5. Run Locally

```bash
streamlit run app.py
```

Application will be available at `http://localhost:8501`

---

## Security

| Concern | Approach |
|---|---|
| API key — local | Stored in `.streamlit/secrets.toml` (git-ignored) |
| Code access | `st.secrets` → mapped to `os.environ` |
| Safe to commit | `secrets.toml.example` (no real values) |
| Never commit | `secrets.toml`, `.venv/`, `__pycache__/` |

---

## Dependencies

```
streamlit
google-genai
```

```bash
pip install -r requirements.txt
```

---

*© 2026 Clino Health Innovation.*