from google.generativeai import GenerativeModel
import google.generativeai as genai

# Paste your Gemini API key here
genai.configure(api_key="AIzaSyD2q1ALHLR8BE4tx513Hwu-MHDO-BG7faw")
model = GenerativeModel("models/gemini-2.5-flash-preview-04-17")

def query_gemini(prompt):
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {e}"