from groq import Groq
from django.conf import settings
import json
import datetime

client = Groq(api_key=settings.GROQ_API_KEY)

SYSTEM_PROMPT = f"""
You are an assistant for a personal expense tracker.
The user may ask in Spanish, Catalan, or English and may have typos.
Today is {datetime.date.today()}
If the user asks for incomes/expenses in a given period of time (optionally for a specific category) return only a JSON with these fields:
- type: "expense" or "income"
- category: string (normalized from Available labels list, return wihtout the word specified in parenthesis). Match the user input if possible but Important! if NO category is specified in the question even if there are available labels, just return empty string.
- period: "last_month", "this_month", or provide {{"start_date":"YYYY-MM-DD","end_date":"YYYY-MM-DD"}} for custom periods.
  If not specified, return empty string. Only "this_month" or "last_month" are allowed as string periods, otherwise provide start_date and end_date.
If question is valid just return JSON with the 3 specified keys (type, category, period), not other keys like placeholder not JSON + text.
OTERWHISE If the question is not related to how much spent/income the user had or you don't see clearly what the user wants, just answer with regular natural language, do NEVER return an empty json or string text with JSON, just one or the other.
Remember, not all incomes/expenses have a category, so if none is specified just return empty string for category in the JSON!
Be friendly, send some emojis when conversating."""

def parse_question(question: str, available_labels=None, history=None) -> dict:
    """
    available_labels: list of dicts with user's labels, e.g.
    [{"id": 1, "name": "Comida", "type": "expense"}, ...]
    history: list of dicts with past messages for context
    """
    print(f"User question: {question}")

    if available_labels is None:
        available_labels = []
    if history is None:
        history = []

    # Convertimos etiquetas en un texto para el prompt
    labels_text = ""
    if available_labels:
        labels_text = "Available labels (not user input): " + ", ".join(f"{l['name']} ({l['type']})" for l in available_labels)

    # Construimos los mensajes para Groq, incluyendo historial
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    for h in history:
        messages.append({"role": h["role"], "content": h["content"]})

    # Añadimos la pregunta actual
    messages.append({"role": "user", "content": f"{labels_text}\nUser question: {question}"})

    # Llamamos al API de Groq
    resp = client.chat.completions.create(
        model=settings.GROQ_MODEL,
        messages=messages,
        temperature=0,
    )

    answer_dict = {"placeholder": "jeje el bot no zap que contezta"}

    # Intentamos parsear la respuesta como JSON
    try:
        answer = resp.choices[0].message.content
        print(answer)
        answer_dict["bot_answer"] = answer
        json_dict = json.loads(answer)
        print(answer_dict)
        if isinstance(json_dict, dict):
            return json_dict
    except Exception as e:
        # Si falla el JSON, devolvemos campos vacíos
        print(e)
    return answer_dict
        #return {"type": "", "category": "", "period": ""}
