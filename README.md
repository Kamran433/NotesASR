# Gemini PDF Assistant - Streamlit App

This is a Streamlit-based intelligent assistant that allows you to upload PDF documents and interact with them using **Google Gemini 1.5 Flash**. It provides a conversational interface to ask questions about the content, get references, generate detailed notes, take tests, and jot down personal ideas in a notepad. Built with a future scope for deployment as a web and mobile application.

---

## Features

### 1. **PDF Upload & Parsing**

- Upload one or more PDFs (max size based on Streamlit limit)
- Extracts text page-wise using **PyMuPDF** (fast, accurate)

### 2. **Gemini 1.5 Flash Integration**

- Uses Google’s `generative-ai-python` SDK
- You can ask contextual questions based on the uploaded PDFs
- Gemini replies with smart answers and inline references like `[Ref: docname page 3]`

### 3. **Two-Pane Interface**

- **Left Pane**: Chatbox for natural language Q&A
- **Right Pane**: Tabs for References, Notes, Tests, and Freeform Notes

### 4. **Tabs Overview**

- **References Tab**: View cited passages from the PDFs
- **Detailed Notes Tab**: Gemini generates comprehensive notes from selected content
- **Test Tab**:
  - Choose difficulty (Easy / Medium / Hard)
  - Auto-generates questions from PDFs
  - Hard mode includes a timer and webcam-based proctoring via `streamlit-webrtc`
- **Freeform Notepad**: Type and save anything (works offline too)

### 5. **"Did You Know?" Tips**

- After every answer, get a bonus tip or interesting fact from the material

---

## Screenshots

(You can insert screenshots here after running locally)

---

## How It Works

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
