"""
api.py
------
The Backend logic and API connection file.
This file securely loads the Gemini API key from Streamlit secrets, 
initializes the google-genai client, and handles sending the user's 
symptoms to the AI and returning the parsed JSON response.
"""

import streamlit as st 
import json
import os
from google import genai
from google.genai import types
from prompt import build_prompt

def configure_gemini():
    """
    Reads GEMINI_API_KEY from .streamlit/secrets.toml and configures Gemini.
    """
    # ← 2. Ask Streamlit for the secret instead of using .env
    api_key = st.secrets.get("GEMINI_API_KEY", "") 

    if not api_key:
        raise ValueError("GEMINI_API_KEY not found. Please add it to .streamlit/secrets.toml")
        
    # We set it as an environment variable here so the new GenAI client finds it automatically
    os.environ["GEMINI_API_KEY"] = api_key


def analyze_symptoms(symptoms: str) -> dict:
    """
    Sends symptoms to Gemini API and returns structured result.
    """
    # Step 1 — Build the prompt
    prompt = build_prompt(symptoms)

    # Step 2 — Initialize the new modern client
    client = genai.Client()

    # Step 3 — Call Gemini API using the new syntax
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            temperature=0.2
        )
    )

    # Step 4 — Parse JSON and return
    result = json.loads(response.text)
    return result