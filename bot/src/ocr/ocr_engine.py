from tesseract import TesseractOCR

def run_ocr(image):
    """
    Perform OCR on the given image using Tesseract.

    Args:
        image: PIL Image object to process.

    Returns:
        str: Extracted text from the image.
    """
    tesseract = TesseractOCR()
    extracted_text = tesseract.image_to_string(image)
    return extracted_text