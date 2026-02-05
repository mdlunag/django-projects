from groq import Groq
import json

client = Groq()


SYSTEM_PROMPT = """
You are an intent parser for a personal expense tracker.

Return ONLY valid JSON.

Do NOT invent category names.
If a category is mentioned, return it as raw text.

Fields:
- intent
- category_text (string or null)
- period
"""

def parse_question(question: str) -> dict:
    resp = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": question},
        ],
        temperature=0,
    )

    return json.loads(resp.choices[0].message.content)
