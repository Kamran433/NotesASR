import fitz  # PyMuPDF

def parse_pdf(uploaded_files):
    if not uploaded_files or len(uploaded_files) == 0:
        raise ValueError("No files uploaded.")
    
    chunks = []
    for uploaded_file in uploaded_files:
        try:
            file_bytes = uploaded_file.read()
            # Open the PDF from bytes
            with fitz.open(stream=file_bytes, filetype="pdf") as doc:
                # Add a marker for new document
                chunks.append(f"--- Document: {uploaded_file.name} ---")
                # Extract text from each page
                for page in doc:
                    text = page.get_text().strip()
                    if text:
                        chunks.append(text)
        except Exception as e:
            print(f"Failed to parse {uploaded_file.name}: {e}")
    return chunks