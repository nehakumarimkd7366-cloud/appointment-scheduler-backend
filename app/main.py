from fastapi import FastAPI, Form, UploadFile, File
from app.extractor import extract_entities
from app.normalizer import normalize_data
from app.ocr import extract_text_from_image

app = FastAPI()

# Health check
@app.get("/")
def root():
    return {"status": "API running"}

# -----------------------------
# TEXT INPUT ENDPOINT
# -----------------------------
@app.post("/parse/text")
async def parse_text(text: str = Form(...)):
    # Step 1: OCR (text input)
    ocr_output = {
        "raw_text": text,
        "confidence": 0.90
    }

    # Step 2: Entity extraction
    entity_output = extract_entities(text)

    if not all(entity_output["entities"].values()):
        return {
            "status": "needs_clarification",
            "message": "Ambiguous date/time or department"
        }

    # Step 3: Normalization
    normalized = normalize_data(
        entity_output["entities"]["date_phrase"],
        entity_output["entities"]["time_phrase"]
    )

    # Step 4: Final response
    return {
        "appointment": {
            "department": entity_output["entities"]["department"].capitalize(),
            "date": normalized["date"],
            "time": normalized["time"],
            "tz": "Asia/Kolkata"
        },
        "status": "ok"
    }

# -----------------------------
# IMAGE INPUT ENDPOINT (OCR)
# -----------------------------
@app.post("/parse/image")
async def parse_image(file: UploadFile = File(...)):
    text, confidence = extract_text_from_image(file.file)

    entity_output = extract_entities(text)

    if not all(entity_output["entities"].values()):
        return {
            "status": "needs_clarification",
            "message": "Ambiguous date/time or department"
        }

    normalized = normalize_data(
        entity_output["entities"]["date_phrase"],
        entity_output["entities"]["time_phrase"]
    )

    return {
        "appointment": {
            "department": entity_output["entities"]["department"].capitalize(),
            "date": normalized["date"],
            "time": normalized["time"],
            "tz": "Asia/Kolkata"
        },
        "status": "ok"
    }
