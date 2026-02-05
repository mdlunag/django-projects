from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Sum
from datetime import date
from dateutil.relativedelta import relativedelta
from .models import FinancialRecord, Label
from .groq_client import parse_question
import json

@login_required
def ask_agent(request):
    question = request.GET.get("q")
    if not question:
        return JsonResponse({"error": "No question provided"}, status=400, json_dumps_params={"ensure_ascii": False})

    # Recuperamos historial del usuario de la sesión
    history = request.session.get("chat_history", [])

    # Recuperamos todas las etiquetas del usuario
    labels = list(Label.objects.filter(user=request.user).values("id", "name", "type"))

    # Llamamos a Groq pasando la pregunta, etiquetas y historial
    parsed = parse_question(question, available_labels=labels, history=history)

    print(parsed)

    # Guardamos pregunta y respuesta en el historial
    history.append({"role": "user", "content": question})
    history.append({"role": "assistant", "content": json.dumps(parsed)})
    request.session["chat_history"] = history

    bot_answer = parsed.get("bot_answer", "")
    if bot_answer:
        return JsonResponse({
            "answer": bot_answer,},
            json_dumps_params={"ensure_ascii": False}
        )

    invalid_question_message = parsed.get("placeholder", "")
    if invalid_question_message:
        return JsonResponse({
        "answer": invalid_question_message,},
        json_dumps_params={"ensure_ascii": False}
    )

    # Tipo de registro: 'expense' o 'income'
    record_type = parsed.get("type", "expense")

    # Categoria detectada por Groq
    label_name = parsed.get("category")
    label_obj = None

    if label_name:
        label_obj = next(
            (
                l for l in labels
                if (l["name"].lower() == label_name.lower() or f"{l['name']} ({l['type']})".lower() == label_name.lower())
                and l["type"] == record_type
            ),
            None
        )
        if not label_obj:
            return JsonResponse({
                "error": f"No encontré la categoría '{label_name}' en tu lista.",
                "options": [l for l in labels if l["type"] == record_type]
            })
        label_name = label_obj["name"]

    # Queryset base
    qs = FinancialRecord.objects.filter(user=request.user, type=record_type)

    # Filtrar por categoría si aplica
    if label_obj:
        qs = qs.filter(label_id=label_obj["id"])

    # Filtrar por periodo
    period = parsed.get("period")
    if isinstance(period, dict):
        qs = qs.filter(date__gte=period.get("start_date"), date__lte=period.get("end_date"))
    elif period == "last_month":
        today = date.today()
        start = today.replace(day=1) - relativedelta(months=1)
        end = today.replace(day=1)
        qs = qs.filter(date__gte=start, date__lt=end)
    elif period == "this_month":
        today = date.today()
        start = today.replace(day=1)
        qs = qs.filter(date__gte=start, date__lte=today)

    # Total de gastos o ingresos
    total = qs.aggregate(total=Sum("amount"))["total"] or 0
    tipo_texto = "gastado" if record_type == "expense" else "ingresado"

    top_category_text = ""
    if not label_obj and record_type == "expense":
        top_cat = (
            qs.values("label__name")
            .annotate(total_cat=Sum("amount"))
            .order_by("-total_cat")
            .first()
        )
        if top_cat and top_cat["label__name"]:
            top_category_text = f" La categoría con más {tipo_texto} es {top_cat['label__name']} con {top_cat['total_cat']}€."

    return JsonResponse({
        "answer": f"Has {tipo_texto} {total}€ en {label_name if label_name else 'total'}." + top_category_text,
    }, json_dumps_params={"ensure_ascii": False})
