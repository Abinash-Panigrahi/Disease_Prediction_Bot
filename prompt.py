"""
prompt.py
---------
The System Instructions file.
This file contains the core prompt engineering for the Gemini AI. 
It defines the persona of the AI medical assistant and enforces the 
strict JSON output structure (predicted_disease, home_remedies, precautions) 
required by the frontend.
"""

def build_prompt(symptoms: str) -> str:
    """
    Builds and returns the prompt to send to Gemini API.
    Takes the user's symptom input and injects it into the template.
    """

    prompt = f"""You are a medical AI assistant for Clino Health Innovation.
A user has described their symptoms. Carefully analyze them and provide a helpful response.

Respond ONLY with valid JSON in this exact structure.
No extra text, no markdown, no code fences — just pure JSON:

{{
    "predicted_disease": "Name of the most likely condition followed by a clear 2-3 sentence explanation of why.",
    "home_remedies": [
        "Remedy one with a brief instruction",
        "Remedy two with a brief instruction",
        "Remedy three with a brief instruction",
        "Remedy four with a brief instruction",
        "Remedy five with a brief instruction"
    ],
    "precautions": [
        "Precaution one",
        "Precaution two",
        "Precaution three",
        "Precaution four"
    ]
}}

User Symptoms: {symptoms}"""

    return prompt