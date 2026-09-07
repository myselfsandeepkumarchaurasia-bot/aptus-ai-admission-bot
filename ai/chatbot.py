import google.generativeai as genai

from ai.prompts import SYSTEM_PROMPT


def create_chatbot(api_key):

    genai.configure(
        api_key=api_key
    )

    model = genai.GenerativeModel(
        "gemini-3.1-flash-lite",
        system_instruction=SYSTEM_PROMPT
    )

    return model


def generate_response(
    model,
    message,
    context=""
):

    prompt = f"""
Knowledge Base:

{context}

Student Question:

{message}

Instructions:

Answer the student using the knowledge base.
If the information is not available, clearly say
that you don't have that information.

Be helpful, professional and concise.
Act as an Aptus Academy admission counsellor.
"""

    response = model.generate_content(
        prompt
    )

    return response.text