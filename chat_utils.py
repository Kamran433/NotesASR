from gemini_utils import query_gemini

def chat_with_pdf(question, context_chunks):
    if not context_chunks:
        return "No context available.", [], ""
    # Limit context to first 10 chunks for prompt
    context = "\n\n".join(context_chunks[:10])
    prompt = f"""
You are an AI assistant helping with study notes. The student asked: "{question}"

Context from their notes:
{context}

Please answer the question with the following format:

Answer: [Provide a detailed and lengthy answer to the question]
References: [List 3-5 detailed quotes from the above context that support your answer, as bullet points starting with '-', also mention the page number where it was found ]
Tip: [Provide few interesting tips or related facts from the notes or trusted sources like wikipedia]
"""
    try:
        response = query_gemini(prompt)
        # Parse the response based on the expected format
        ans_idx = response.find("Answer:")
        ref_idx = response.find("References:")
        tip_idx = response.find("Tip:")
        if ans_idx == -1 or ref_idx == -1 or tip_idx == -1:
            raise ValueError("Unexpected response format")
        answer = response[ans_idx+len("Answer:"):ref_idx].strip()
        refs_section = response[ref_idx+len("References:"):tip_idx].strip()
        tip = response[tip_idx+len("Tip:"):].strip()
        # Extract each reference line
        refs = []
        for line in refs_section.splitlines():
            line = line.strip()
            if line.startswith("-"):
                refs.append(line.lstrip("- ").strip())
        return answer, refs, tip
    except Exception as e:
        # Return error placeholders on failure
        return "Error processing question.", [], ""