from gemini_utils import query_gemini

def generate_enhanced_lnks(chunks):
    if not chunks:
        return []
    notes_text = "\n".join(chunks)
    prompt = (
    "You are given some academic notes below. Your task is to perform the following steps:\n\n"
    "1. Read and understand the notes carefully.\n"
    "2. Extract most relevant topic names or keywords from the notes.\n"
    "3. Search the internet for all possible study notes or videos for study help from [trusted sources].\n"
    "4. Provide the url's of all such websites. \n"
    "Notes:\n"
    f"{notes_text}\n\n"
    "Important:\n"
    "- Do NOT include any explanations or extra text.\n"
    "- Only output the list of url's seperated by commas, each url should be a separate string.\n"
)
    try:
        # AIzaSyDrjChlO476KR7sQlBQZT2tjOkympgh_uE
        output = query_gemini(prompt)
        # Split the output into sections by paragraphs
        return [section for section in output.strip().split("\n\n") if section]
    except Exception as e:
        return ["Error generating notes."]

def generate_enhanced_vids(chunks):
    if not chunks:
        return []
    notes_text = "\n".join(chunks)
    prompt = (
    "You are given some academic notes below. Your task is to perform the following steps:\n\n"
    "1. Read and understand the notes carefully.\n"
    "2. Extract most relevant topic names or keywords from the notes.\n"
    "Notes:\n"
    f"{notes_text}\n\n"
    "Important:\n"
    "- Do NOT include any explanations or extra text.\n"
    "- Only output the list of topic names or keywords seperated by commas, each topic names or keywords should be a separate string.\n"
)
    try:
        # AIzaSyDrjChlO476KR7sQlBQZT2tjOkympgh_uE
        output = query_gemini(prompt)
        # Split the output into sections by paragraphs
        return [section for section in output.strip().split("\n\n") if section]
    except Exception as e:
        return ["Error generating notes."]

def generate_enhanced_pyqs(chunks):
    if not chunks:
        return []
    notes_text = "\n".join(chunks)
    prompt = (
        "You are given the following notes. Your task is to carefully analyze the content and generate atleast [5] structured, [professional] [lengthy] and question papers suitable for academic use. The question paper should cover all key chapters and topics mentioned in the notes and include a balanced mix of question types (e.g., short answer, long answer, multiple choice, fill in the blanks, student enrollment number based numericals if applicable). Ensure that the questions are clear, unambiguous, and test both conceptual understanding and practical application. The final output should be [well-formatted in Markdown] for easy readability and further use by educators. Also provide answer key for everything except long type and short type questions and the end, properly separated from the Question Paper."
        "The markdown format should be of top quality"
        "[I NEED A COMPLETE QUESTION-PAPER AND IT SHOULD BE IN THE BEST MARKDOWN FORMAT, EASILY READABLE AND NOT JUMBLED]"
        "[Put the MCQS in a better spacious format with options in the next line and each sepated from each other similar to four corners of a rectangle. ]"
        "\n\n"
        f"Notes:\n{notes_text}\n\n"
        "Only return the (Question Paper), (MATHEMATICAL-EQUATIONS) and (questions) [MCQ's] in [advanced markdown formatting] without any extra explanation."
    )
    try:
        output = query_gemini(prompt)
        # Split the output into sections by paragraphs
        return [section for section in output.strip().split("\n\n") if section]
    except Exception as e:
        return ["Error generating notes."]
def generate_enhanced_formulas(chunks):
    if not chunks:
        return []
    notes_text = "\n".join(chunks)
    prompt = (
        "You are a helpful, experienced Professor with advanced knowledge. "
        "Given the following notes, extract all the formulas from the notes provided into clean, readable, and long and detailed formula sheet for each chapter and topic for your students. "
        "\n\n"
        f"Notes:\n{notes_text}\n\n"
        "Return the formula sheet and (MATHEMATICAL-EQUATIONS) in markdown format."
    )
    try:
        output = query_gemini(prompt)
        return [section for section in output.strip().split("\n\n") if section]
    except Exception as e:
        return ["Error generating notes."]
def generate_enhanced_notes(chunks):
    if not chunks:
        return []
    notes_text = "\n".join(chunks)
    prompt = (
        "You are a helpful, experienced Professor with advanced knowledge. "
        "Given the following notes, improve them into clean, readable, and [long] and [detailed] study notes for each chapter and topic for your students. "
        "Fix grammar mistakes, clarify concepts, and highlight key ideas in a [detailed and lengthy way].\n\n"
        "THE NOTES SHOULD BE REALLY DETAILED AND EACH CONCEPT SHOULD BE EXPLAINED IN AN EXTREMELY [DETAILED] MANNER"
        "INCLUDE FIGURES IF POSSIBLE"
        "LEAVE NO TOPIC UNEXPLAINED"
        f"Notes:\n{notes_text}\n\n"
        "Return the improved notes and (MATHEMATICAL-EQUATIONS) in [markdown format]."
    )
    try:
        output = query_gemini(prompt)
        return [section for section in output.strip().split("\n\n") if section]
    except Exception as e:
        return ["Error generating notes."]

def extract_reference_snippets(chunks, term):
    return [c for c in chunks if term.lower() in c.lower()]

def generate_fact(chunks):
    if not chunks:
        return ""
    notes_text = " ".join(chunks)
    prompt = (
        "Pick one interesting, lesser-known tip or fact from these notes or from the internet. Only return that one thing.\n\n"
        f"Notes:\n{notes_text}"
    )
    try:
        return query_gemini(prompt)
    except Exception as e:
        return ""