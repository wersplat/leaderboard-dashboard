import pytest
from unittest.mock import patch
from ocr_backend.ocr_engine import process_image  # Assuming process_image handles OCR parsing

# Mock OCR function to simulate OCR processing
def mock_process_image(image_url):
    return {
        "mvp": "Player1",
        "winner": "Team A",
        "stats": {
            "PTS": 25,
            "AST": 5,
            "REB": 10
        }
    }

def test_ocr_parsing():
    # Mock the process_image function to avoid real OCR calls
    with patch('ocr_backend.ocr_engine.process_image', side_effect=mock_process_image):
        image_url = "http://example.com/sample_image.jpg"
        result = process_image(image_url)
        
        # Assertions to verify the result
        assert "error" not in result  # Ensure no errors occurred
        assert "mvp" in result  # Ensure MVP field is returned
        assert "winner" in result  # Ensure winner field is returned
        assert isinstance(result['stats'], dict)  # Ensure stats are returned in a dict format
        assert result['mvp'] == "Player1"  # Verify MVP value
        assert result['winner'] == "Team A"  # Verify Winner value
        assert result['stats']['PTS'] == 25  # Verify Points value