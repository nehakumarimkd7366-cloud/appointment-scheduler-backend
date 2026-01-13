import re

def extract_entities(text: str):
    text = text.lower()

    # department
    dept_match = re.search(r'\b(dentist|doctor|hospital)\b', text)
    department = dept_match.group(1) if dept_match else None

    # time
    time_match = re.search(r'\b(\d{1,2}\s?(am|pm))\b', text)
    time_phrase = time_match.group(1) if time_match else None

    # date
    date_match = re.search(r'\b(next\s+\w+)\b', text)
    date_phrase = date_match.group(1) if date_match else None

    return {
        "entities": {
            "date_phrase": date_phrase,
            "time_phrase": time_phrase,
            "department": department
        },
        "entities_confidence": 0.85
    }
