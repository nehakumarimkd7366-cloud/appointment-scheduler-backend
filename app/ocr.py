from PIL import Image
import pytesseract

# Windows ke liye explicit path (safe)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_text_from_image(file):
    """
    Takes an uploaded image file and returns extracted text + confidence
    """
    image = Image.open(file)
    text = pytesseract.image_to_string(image)

    confidence = 0.85 if text.strip() else 0.3
    return text.strip(), confidence
