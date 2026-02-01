import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = """
You are a voice bot answering interview questions as ME.
Responses should sound confident, human, concise, and authentic.
No buzzwords. No corporate fluff.
"""

def get_ai_response(user_question: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_question}
        ],
        temperature=0.6,
        max_tokens=150
    )

    return response.choices[0].message.content.strip()
