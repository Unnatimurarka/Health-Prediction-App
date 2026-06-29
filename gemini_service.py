import os
from dotenv import load_dotenv
from google import genai

# Load environment variables
load_dotenv()

# Create Gemini client
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def generate_health_prediction(glucose, haemoglobin, cholesterol):

    prompt = f"""
You are a healthcare assistant.

Patient Values:
- Glucose: {glucose}
- Haemoglobin: {haemoglobin}
- Cholesterol: {cholesterol}

Give:
1. Short health assessment
2. Possible health risks
3. Lifestyle advice

Keep the response under 60 words.
Do not diagnose diseases.
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )

    return response.text