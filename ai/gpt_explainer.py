import openai
import os
from dotenv import load_dotenv
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

def explain_filing(filing_name, filing_type, jurisdiction):
    prompt = f"""
    Explain the importance of the following compliance filing in simple terms:
    Filing: {filing_name}
    Type: {filing_type}
    Jurisdiction: {jurisdiction}

    Keep it brief, clear, and professional.
    """
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
        max_tokens=150,
    )
    return response.choices[0].message["content"].strip()
