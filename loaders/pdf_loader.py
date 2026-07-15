from pathlib import Path
import fitz
import pytesseract
from PIL import Image
import io

def load_pdf(path: Path):
    doc = fitz.open(path)
    page_count = len(doc)
    
    text_content = []
    scanned_pages = 0
    total_chars = 0
    
    for page in doc:
        text = page.get_text()
        if len(text.strip()) < 10:
            # Fallback to OCR
            pix = page.get_pixmap()
            img = Image.open(io.BytesIO(pix.tobytes()))
            ocr_text = pytesseract.image_to_string(img)
            text_content.append(ocr_text)
            scanned_pages += 1
        else:
            text_content.append(text)
        total_chars += len(text_content[-1])

    raw_text = "\n".join(text_content)
    
    metadata = {
        "page_count": page_count,
        "scanned_pages": scanned_pages
    }
    
    return raw_text, "pdf", "en", metadata
