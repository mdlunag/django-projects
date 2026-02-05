from rapidfuzz import process, fuzz
from datetime import date
from dateutil.relativedelta import relativedelta

def match_label(category_text, labels):
    """Fuzzy match category_text with list of labels [{'id':..., 'name':...}]"""
    label_names = [l["name"] for l in labels]
    match, score, idx = process.extractOne(category_text, label_names, scorer=fuzz.WRatio)
    if score < 60:
        return None
    return labels[idx]

def get_period_dates(period):
    """Convert 'last_month', 'this_month' to date ranges"""
    today = date.today()
    if period == "last_month":
        start = today.replace(day=1) - relativedelta(months=1)
        end = today.replace(day=1)
    elif period == "this_month":
        start = today.replace(day=1)
        end = today
    else:
        # custom or fallback
        start = None
        end = None
    return start, end
