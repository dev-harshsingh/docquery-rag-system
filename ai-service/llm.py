import os
from google import genai
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv("GEM_API_KEY")

def generate_answer(context_chunks, question):
    """
    Generates an answer using Gemini strictly based on provided context.
    """

    context_text = "\n\n".join(context_chunks)

    prompt = f"""
You are an AI assistant answering questions strictly using the context below.
If the answer is not present in the context, say "I don't know".

Context:
{context_text}

Question:
{question}

Answer in clear and concise language:
"""

    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=prompt
    )

    return response.text


client = genai.Client(api_key=GEMINI_API_KEY)
