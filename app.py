import streamlit as st
from chat_utils import chat_with_pdf
from pdf_utils import parse_pdf
from note_utils import generate_enhanced_notes, generate_enhanced_formulas, generate_enhanced_pyqs, generate_enhanced_vids, generate_enhanced_lnks
from test_utils import generate_test_questions, validate_answer, parse_mcqs, parse_qa
from proctor_utils import start_proctoring
import weasyprint
import markdown as md
import streamlit.components.v1 as components
import time
from googleapiclient.errors import HttpError
import speech_recognition as sr
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
import tempfile
from streamlit_webrtc import webrtc_streamer, AudioProcessorBase
from googleapiclient.discovery import build
import speech_recognition as sr
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
import tempfile
import os
import base64
from memory_map import render_memory_map_tab

# streamlit run /Users/xyz/Downloads/notes-gpt/app.py



# Replace with your actual API key
YOUTUBE_API_KEY = st.secrets['youtube_key']

def recognize_speech_from_mic():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    
    with mic as source:
        recognizer.adjust_for_ambient_noise(source)  # Optional: handles background noise
        audio = recognizer.listen(source, phrase_time_limit=60)
        
    try:
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        st.error("Sorry, I couldn't understand what you said.")
    except sr.RequestError:
        st.error("Could not request results from Google Speech Recognition.")
    return ""

def speak_text(text):
    tts = gTTS(text)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
        tts.save(fp.name)
        audio_path = fp.name

    # Embed the audio using base64
    with open(audio_path, "rb") as f:
        audio_data = f.read()
        b64 = base64.b64encode(audio_data).decode()
        audio_html = f"""
        <audio autoplay controls>
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
        </audio>
        """
        st.markdown(audio_html, unsafe_allow_html=True)
    os.remove(audio_path)


def extract_topics_from_notes(notes_text):
    topics_raw = generate_enhanced_vids(notes_text)
    topics = [topic.strip() for topic in topics_raw[0].split(',')]
    return list(set(topics))[:5]

def search_youtube_for_topic(topic, api_key):
    try:
        youtube = build('youtube', 'v3', developerKey=api_key)
        request = youtube.search().list(
            q=topic,
            part='snippet',
            type='video',
            maxResults=1,
            safeSearch='strict',
        )
        response = request.execute()
        videos = []
        for item in response.get('items', []):
            video_url = f"https://www.youtube.com/watch?v={item['id']['videoId']}"
            videos.append(video_url)
        return videos
    except HttpError as e:
        error_reason = e.error_details[0]['reason'] if e.error_details else "unknown"
        if error_reason == 'quotaExceeded':
            st.info("YouTube API quota exceeded. Please wait or use another key.")
        else:
            st.info(f"An HTTP error occurred: {e}")

    

def get_valid_youtube_urls(notes_text):
    topics = extract_topics_from_notes(notes_text)
    all_video_urls = []
    for topic in topics:
        # print(topic)
        urls = search_youtube_for_topic(topic, YOUTUBE_API_KEY)
        all_video_urls.append([urls, topic])
    return all_video_urls

# Example usage:



def html_to_pdf(html_content):
    pdf = weasyprint.HTML(string=html_content).write_pdf()
    return pdf

import markdown as md

def generate_html_from_markdown(notes):
    mathjax_script = """
    <script type="text/javascript"
      id="MathJax-script"
      async
      src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js">
    </script>
    """

    styles = """
    <style>
        body {
            font-family: 'Georgia', serif;
            padding: 2em;
            color: #000000;
            line-height: 1.6;
        }
        h1, h2, h3 {
            color: #2c3e50;
        }
        img {
            max-width: 100%;
            margin: 1em 0;
            border-radius: 8px;
        }
        code {
            background-color: #f4f4f4;
            padding: 0.2em 0.4em;
            border-radius: 4px;
            font-family: monospace;
        }
        pre {
            background-color: #f4f4f4;
            padding: 1em;
            border-radius: 6px;
            overflow-x: auto;
        }
        ul, ol {
            padding-left: 2em;
        }
        hr {
            margin: 2em 0;
        }
    </style>
    """

    markdown_converter = md.Markdown(extensions=["fenced_code", "tables"])
    
    body_html = "<body>"
    for i, note_md in enumerate(notes):
        body_html += f"<h2>Note {i+1}</h2>"
        body_html += markdown_converter.convert(note_md)
        body_html += "<hr>"
    body_html += "</body>"

    full_html = f"""
    <html>
    <head>
        {styles}
        {mathjax_script}
    </head>
    {body_html}
    </html>
    """

    return full_html

# List of YouTube video embed URLs

# Setting the page configuration
st.set_page_config(
    page_title="Notes ASR", 
    page_icon='🌀', 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# Custom CSS for a professional and futuristic look
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700&family=Open+Sans:wght@300;600&display=swap" rel="stylesheet">

<style>
    html, body, [class*="css"] {
        font-family: 'Open Sans', sans-serif;
        background: radial-gradient(ellipse at top, #0a0a0a 0%, #141414 100%);
        color: #EDEDED;
        overflow-x: hidden;
    }
    .subheader {
        font-size: 22px;
        text-align: center;
        color: #bbbbbb;
        margin-top: -10px;
        font-weight: 300;
    }
    .title {
        font-family: 'Orbitron', sans-serif;
        font-size: 48px;
        text-align: center;
        color: #00f9ff;
        text-shadow: 0 0 20px #00f9ff;
        margin-top: 30px;
        letter-spacing: 3px;
        animation: fadeIn 2s ease-in-out;
    }

    .glass-panel {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(12px);
        border-radius: 16px;
        padding: 30px;
        margin: 30px auto;
        width: 90%;
        max-width: 800px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        animation: slideUp 0.6s ease forwards;
    }

    .glass-panel:hover {
        box-shadow: 0 0 25px rgba(0,249,255,0.1);
        transform: scale(1.01);
    }

    .upload-animation {
        text-align: center;
        font-size: 24px;
        color: #00f9ff;
        margin-top: 20px;
        animation: pulse 1.5s infinite;
    }

    @keyframes fadeIn {
        0% { opacity: 0; transform: scale(0.95); }
        100% { opacity: 1; transform: scale(1); }
    }

    @keyframes slideUp {
        0% { opacity: 0; transform: translateY(20px); }
        100% { opacity: 1; transform: translateY(0); }
    }

    @keyframes pulse {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.7; transform: scale(1.05); }
    }
</style>
""", unsafe_allow_html=True)

# --- Start Animation ---
def load():
    placeholder = st.empty()
    with placeholder.container():
        st.markdown('<div class="title">Notes ASR Loading...</div>'
        '<p class="title subheader">Study the advanced way</p>', unsafe_allow_html=True)
        time.sleep(3.5)


    placeholder.empty()
load()

# Title and Subtitle with futuristic fonts and color scheme
st.markdown('<div class="title">Notes ASR</div>', unsafe_allow_html=True)
st.markdown('''
<div class="glass-panel subheader">
    With Love from Kamran 
</div>
''', unsafe_allow_html=True)

# Stylish Divider
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)



# Sidebar: Upload and Settings
st.sidebar.header("Settings")
theme = st.sidebar.radio("Select Theme", ("Light", "Dark"))
st.sidebar.header("Upload PDFs")
uploaded_files = st.sidebar.file_uploader("Choose PDF files", type=["pdf"], accept_multiple_files=True,)
st.sidebar.markdown("---")
st.sidebar.subheader("Personal Notes")
personal_notes = st.sidebar.text_area("Jot something down:", height=1500)

# Apply theme styles
if theme == "Dark":
    st.markdown(
        """<style>
        [data-testid="stAppViewContainer"] {
            background-color: #18191A;
            color: #EEE;
        }
        [data-testid="stSidebar"] {
            background-color: #111;
            color: #DDD;
        }
        .css-15zrgzn {color: #EEE;}  /* headings */
        .input-container {
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        .text-input {
            flex: 1;
        }
        .mic-button {
            padding-top: 8px;
        }
        </style>""",
        unsafe_allow_html=True
    )


# Session state setup
if "pdf_chunks" not in st.session_state:
    st.session_state.pdf_chunks = []
if "history" not in st.session_state:
    st.session_state.history = []
if "last_refs" not in st.session_state:
    st.session_state.last_refs = []

# Parse PDFs when uploaded
if uploaded_files:
    st.session_state.pdf_chunks = parse_pdf(uploaded_files)

# Main layout: chat on left, tools on right
if st.session_state.pdf_chunks:
        tabs = st.tabs(["Chat", "References", "Notes", "Tests", "Important Formulas", "PYQ's", "Video Reference's"])
        chat_tab, ref_tab, notes_tab, tests_tab, formula_tab, exam_tab, video_tab = tabs
        with chat_tab:
                # --- Button to capture speech ---\
                    if "question_input" not in st.session_state:
                        st.session_state.question_input = ""
                        spoken_text = ""
                    st.markdown('<div class="input-container">', unsafe_allow_html=True)
                    col1, col2 = st.columns([10, 1])
                    # Voice input button
                    with col2:
                        st.markdown('<div style="padding-top: 27px">', unsafe_allow_html=True)
                        mic_clicked = st.button("Speak", key="micbutton")
                        st.markdown('</div>', unsafe_allow_html=True)
                    if mic_clicked:
                        with col1:
                            with st.spinner("Listening..."):
                                spoken_text = recognize_speech_from_mic()
                        if spoken_text:
                            st.session_state.question_input = spoken_text
                        question = st.session_state.question_input
                    # Text input field shows either typed or spoken input
                    with col1:
                        question = st.text_input("Ask a question:", key="question_input")
                    
                    # if st.button("Speak"):
                    #     question = recognize_speech_from_mic()
                    # else:
                    #     question = st.text_input("Or type your question:")

                    # --- If we have a question, get the answer ---
                        if question:
                            with st.spinner("Thinking..."):
                                answer, refs, tip = chat_with_pdf(question, st.session_state.pdf_chunks)
                            st.session_state.history.append({"role": "user", "content": question})
                            st.session_state.history.append({"role": "assistant", "content": answer})
                            st.info(answer)
                            if tip:
                                st.info(f"💡 Tip: {tip}")
                            if refs:
                                st.success("🔗 References added to the References tab.")
                                st.session_state.last_refs = refs
                            # if st.button('Audio-Book'):
                            #     speak_text(answer)
                    st.markdown('</div>', unsafe_allow_html=True)
                        
                
        with ref_tab:
            st.subheader("References")
            if st.session_state.last_refs:
                for i, ref in enumerate(st.session_state.last_refs):
                    with st.expander(f"📖 Reference {i+1}"):
                        st.markdown(f"> {ref}")
            else:
                st.info("No references to display. Ask a question in the Chat panel.")
        with notes_tab:
            st.markdown("""
                <style>
                    .pdf-viewer {
                        background-color: #ffffff;
                        padding: 2rem;
                        border-radius: 12px;
                        max-height: 80vh;
                        overflow-y: scroll;
                        box-shadow: 0 0 20px rgba(0, 0, 0, 0.2);
                        font-family: 'Georgia', serif;
                        color: #000000;
                        line-height: 1.7;
                    }
                    .note-page {
                        margin-bottom: 3rem;
                        border-bottom: 1px solid #ccc;
                        padding-bottom: 2rem;
                    }
                    .note-page h1, .note-page h2, .note-page h3 {
                        color: #004d99;
                    }
                    .note-page img {
                        max-width: 100%;
                        border-radius: 8px;
                        margin-top: 1rem;
                        margin-bottom: 1rem;
                    }
                    ::-webkit-scrollbar {
                        width: 8px;
                    }
                    ::-webkit-scrollbar-thumb {
                        background-color: #888;
                        border-radius: 8px;
                    }
                    ::-webkit-scrollbar-track {
                        background: #f1f1f1;
                    }
                </style>
            """, unsafe_allow_html=True)

            st.subheader("📘 Smart Notes Viewer")
            def gen_not():
                notes = generate_enhanced_notes(st.session_state.pdf_chunks)

                html_content = '<div class="pdf-viewer">\n'
                for i, note in enumerate(notes):
                    html_content += f"<div>{note}</div>\n"
                html_content += '</div>'

                # Display the notes in a "book-like" viewer
                with st.container():
                    st.markdown('<div class="pdf-viewer">', unsafe_allow_html=True)
                    for i, note in enumerate(notes):
                        st.markdown(note, unsafe_allow_html=False)  # Render Markdown properly
                        st.markdown('</div>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                html_content = generate_html_from_markdown(notes)
                # Convert the HTML content to PDF
                pdf = html_to_pdf(html_content)

                # Provide the download button
                st.download_button(
                    label="Download Notes as PDF",
                    data=pdf,
                    file_name="smart_notes.pdf",
                    mime="application/pdf"
                )
            if st.button("Generate Smart-Notes"):
                TIME = True
                gen_not()
                TIME = False
        # tests_tab = st.container()
        with formula_tab:
            st.subheader("Formula Section")
            def gen_form():
                notes = generate_enhanced_formulas(st.session_state.pdf_chunks)

                html_content = '<div class="pdf-viewer">\n'
                for i, note in enumerate(notes):
                    html_content += f"<div>{note}</div>\n"
                html_content += '</div>'

                # Display the notes in a "book-like" viewer
                with st.container():
                    st.markdown('<div class="pdf-viewer">', unsafe_allow_html=True)
                    for i, note in enumerate(notes):
                        st.markdown('<div>', unsafe_allow_html=True)
                        st.markdown(note, unsafe_allow_html=False)  # Render Markdown properly
                        st.markdown('</div>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                html_content = generate_html_from_markdown(notes)
                # Convert the HTML content to PDF
                pdf = html_to_pdf(html_content)
                # Provide the download button
                st.download_button(
                    label="Download Formulas as PDF",
                    data=pdf,
                    file_name="smart_formulas.html",
                    mime="application/formula"
                )
            if st.button("Generate Formula-Sheet"):
                TIME = True
                gen_form()
                TIME = False
        
        with exam_tab:
            st.subheader("PYQ Section")
            def gen_pyq():
                notes = generate_enhanced_pyqs(st.session_state.pdf_chunks)
                html_content = '<div class="pdf-viewer">'
                html_content += '</div>'

                # Display the notes in a "book-like" viewer
                with st.container():
                    st.markdown('<div>', unsafe_allow_html=True)
                    for i, note in enumerate(notes):
                        st.markdown(note, unsafe_allow_html=False)  # Render Markdown properly
                        st.markdown('</div>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                html_content = generate_html_from_markdown(notes)
                # Convert the HTML content to PDF
                pdf = html_to_pdf(html_content)

                # Provide the download button
                st.download_button(
                    label="Download PYQ as PDF",
                    data=pdf,
                    file_name="smart_pyq.pdf",
                    mime="application/pyq"
                )
            if st.button("Generate PYQ's"):
                TIME = True
                gen_pyq()
                TIME = False

        with video_tab:
            def gen_txt():
                if st.session_state.pdf_chunks:
                    lnks = generate_enhanced_lnks(st.session_state.pdf_chunks)
                    lnks = [topic.strip() for topic in lnks[0].split(',')]
                    print(lnks[0])
                    if lnks:
                        for lnk in lnks:
                            st.markdown(lnk)
                    else:
                        st.warning("No Suggestions found.")
                else:
                    st.info("Upload study material to fetch web recommendations.")
            def gen_vid():
                if st.session_state.pdf_chunks:
                    # topic = extract_main_topic(st.session_state.pdf_chunks)
                    # search_query = f"{topic} concept explained"
                    # st.info(f"📌 Searching YouTube for: *{search_query}*")

                    videos = get_valid_youtube_urls(st.session_state.pdf_chunks)
                    # print(videos)
                    
                    if videos:
                        for video, topic in videos:
                            if video:
                                print(video)
                                print(type(video))
                                st.video(video[0])
                                st.markdown(f"**{topic}**")
                    else:
                        st.warning("No videos found.")
                else:
                    st.info("Upload study material to fetch video recommendations.")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.subheader("🛜 Web-References")
                TIME = True
                gen_txt()
            with col2:
                st.subheader("🎬 Video-References")
                gen_vid()
            with col3:
                st.subheader("📚 Make Notes")
                personal_notes2 = st.text_area("Jot something down:", key='notes2', height=1500, label_visibility="collapsed")
                TIME = False

            
            
            


        with tests_tab:
            st.subheader("Test Section")

            difficulty = st.selectbox("Select difficulty level", ["Easy", "Medium", "Hard"])
            qtype = st.selectbox("Select Question type", ["MCQ", "Short Answer", "Long Answer"])
            if "questions" not in st.session_state:
                st.session_state.questions = []
            if "revealed" not in st.session_state:
                st.session_state.revealed = {}
            if "attempts" not in st.session_state:
                st.session_state.attempts = {}

            def generate_and_store_questions():
                
                raw = generate_test_questions(st.session_state.pdf_chunks, difficulty, qtype)
                # st.write("Raw output:", raw)  # Show Gemini response
                
                if qtype == "MCQ":
                    parsed = parse_mcqs(raw)
                else:
                    parsed = parse_qa(raw)
                # st.write("Parsed questions:", parsed)  # Debug parsing
                
                st.session_state.questions = parsed
                st.session_state.revealed = {i: False for i in range(len(parsed))}
                st.session_state.attempts = {i: 0 for i in range(len(parsed))}


            if st.button("Generate Questions"):
                generate_and_store_questions()

            dic = {1: 'A', 2: 'B', 3: 'C', 4 :'D'}

            if st.session_state.questions:
                for i, q in enumerate(st.session_state.questions):
                    st.markdown(f"**Q{i+1}:** {q['question']}")
                    if 'options' in q:
                        selected = st.radio("Choose:", q["options"], key=f"radio_{i}")
                    else:
                        selected = st.text_input("Your Answer:", key=f"input_{i}")
                    
                    if st.session_state.attempts[i] == 3:
                        st.error(f"Correct answer: {q['answer']}")

                    if st.button("Submit", key=f"submit_btn_{i}"):
                        st.session_state.attempts[i] += 1
                        st.session_state.revealed[i] = True
                        if 'options' in q:
                            is_correct = dic[q["options"].index(selected) + 1] == q["answer"]
                        else:
                            is_correct = validate_answer(q["answer"], selected, difficulty)
                        
                    #     time.sleep(3.5)  # Let animation play before continuing

                    if st.session_state.revealed.get(i, False):
                        # st.session_state.attempts[i] += 1
                        # st.session_state.revealed[i] = True
                        if 'options' in q and dic[q["options"].index(selected) + 1] == q["answer"]:
                            st.success("Correct!")
                        elif 'options' not in q and validate_answer(q["answer"], selected, difficulty) == True:
                            st.success("Correct!")
                        else:
                            st.error("Incorrect.")
                            if "hint" in q and q["hint"]:
                                # if st.checkbox("Show Hint", key=f"hint_{i}"):
                                st.info(q["hint"])
                    st.markdown("---")

            if st.session_state.questions:
                if st.button("Reset Test"):
                    st.session_state.questions = []
                    st.session_state.revealed = {}
                    st.session_state.attempts = {}
                    for i in range(20):
                        st.session_state.pop(f"radio_{i}", None)
            



        # with Memory_Map:
        #     render_memory_map_tab()
else:
    st.info("Upload PDF files to get started.")

