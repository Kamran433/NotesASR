import google.generativeai as genai
from google.generativeai import GenerativeModel
import re

genai.configure(api_key="AIzaSyD2q1ALHLR8BE4tx513Hwu-MHDO-BG7faw")
model = GenerativeModel("models/gemini-2.5-flash-preview-04-17")

def generate_test_questions(pdf_chunks, difficulty, q_type):
    prompt_intro = f"Generate 25 {q_type} questions of {difficulty} difficulty strictly from the following neccesary parts of the content."

    if q_type == "MCQ":
        format_hint = """
Return the questions in the following JSON list format:

[
  {
    "question": "What is the capital of France?",
    "options": ["Berlin", "Madrid", "Paris", "Rome"],
    "answer": "C",
    "hint": "It's known as the city of love."
  },
  ...
]

Only return the JSON list without any extra explanation or formatting.
"""
    elif q_type == "Short Answer":
        format_hint = """
Return the questions in the following JSON list format:

[
  {
    "question": "Explain the concept of polymorphism in OOP.",
    "answer": "Polymorphism is the ability..."
    "hint": "It's known as the city of love."
  },
  ...
]

Only return the JSON list without any extra explanation or formatting.
"""
    else:
        format_hint = """
Return the questions in the following JSON list format:

[
  {
    "question": "Describe how a blockchain ensures data integrity.",
    "answer": "A blockchain ensures integrity by..."
    "hint": "It's known as the city of love."
  },
  ...
]

Only return the JSON list without any extra explanation or formatting.
"""

    content = "\n\n".join(pdf_chunks[:5])  # Limit for brevity
    full_prompt = f"{prompt_intro}\n{format_hint}\nContent:\n{content}"

    try:
        response = model.generate_content(full_prompt)
        if not hasattr(response, "text") or not response.text.strip():
            raise ValueError("Empty response from Gemini.")
        return response.text.strip()
    except Exception as e:
        print(f"Error generating questions: {e}")
        return """
[
  {
    "question": "What is the capital of France?",
    "options": ["Berlin", "Madrid", "Paris", "Rome"],
    "answer": "C",
    "hint": "It's known as the city of love."
  }
]
"""




import json

import json
import re

def parse_mcqs(raw_output):
    try:
        # Remove Markdown code block markers if present
        cleaned = re.sub(r"^```json|```$", "", raw_output.strip(), flags=re.MULTILINE).strip()

        # Try parsing the cleaned JSON string
        questions = json.loads(cleaned)

        parsed_questions = []
        for q in questions:
            parsed_questions.append({
                "question": q.get("question"),
                "options": q.get("options"),
                "answer": q.get("answer"),
                "hint": q.get("hint", None)
            })
        return parsed_questions
    except json.JSONDecodeError as e:
        print("JSON parsing error:", e)
        return []





def parse_qa(raw_output):
    cleaned = re.sub(r"^```json|```$", "", raw_output.strip(), flags=re.MULTILINE).strip()
    questions = json.loads(cleaned)
    parsed_questions = []
    for q in questions:
        parsed_questions.append({
            "question": q.get("question"),
            "answer": q.get("answer"),
            "hint": q.get("hint", None)
        })
    return parsed_questions



def validate_answer(correct, user_input, diff):
    full_prompt = f'you are an experienced examiner, check the students answer {[user_input]} with the correct answer {[correct]}, please check the answers with lineancy based on the difficulty level {diff}.     Only return True or False without any extra explanation or formatting.'
    answer = model.generate_content(full_prompt)
    print(type(answer.text.strip()))
    return answer.text.strip() == 'True'


# Streamlit section

