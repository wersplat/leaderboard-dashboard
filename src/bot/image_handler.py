import requests
import logging
import os

logger = logging.getLogger("discord")

# Use environment variable for OCR API URL
OCR_API_URL = os.getenv("OCR_API_URL", "http://localhost:8000/ocr")

def send_image_to_api(image_url: str) -> dict:
    """
    Sends an image URL to the OCR API and returns the parsed stat data.

    Args:
        image_url (str): The URL of the image to be processed.

    Returns:
        dict: The parsed stat data or an error message.
    """
    try:
        payload = {"image_url": image_url}
        headers = {"Content-Type": "application/json"}
        response = requests.post(OCR_API_URL, json=payload, headers=headers, timeout=10)

        if response.status_code == 200:
            return response.json()
        else:
            logger.error(f"OCR API returned status {response.status_code}: {response.text}")
            return {"error": f"OCR API error {response.status_code}"}

    except Exception as e:
        logger.error(f"Failed to contact OCR API: {e}")
        return {"error": str(e)}