import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

# Configure Gemini API with your key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Set the correct model (you can change to flash if you want faster/cheaper inference)
model = genai.GenerativeModel(model_name="models/gemini-1.5-pro-latest")

def summarize_email(content):
    try:
        prompt = f"Summarize the following email in 3-5 bullet points:\n\n{content}"
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error during summarization:\n\n{e}"
