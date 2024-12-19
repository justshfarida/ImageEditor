from unittest import TestCase
from unittest.mock import patch, MagicMock
from qr_module.utils import generate_qr_code, read_qr_code
import requests
import numpy as np
import io


class QRCodeUtilsTests(TestCase):
    @patch("cloudinary.uploader.upload")
    def test_generate_qr_code_valid(self, mock_upload):
    # Mock Cloudinary response
        mock_upload.return_value = {"url": "http://example.com/temp_qr.png"}
        
        result = generate_qr_code("Test Data", "black", "white")
        
        self.assertEqual(result, "http://example.com/temp_qr.png")
        mock_upload.assert_called_once()

    @patch("cloudinary.uploader.upload")
    def test_generate_qr_code_invalid_colors(self, mock_upload):
        mock_upload.return_value = {"url": "http://example.com/temp_qr.png"}
        
        with self.assertRaises(ValueError) as context:
            generate_qr_code("Test Data", "invalid-color", "white")
        
        self.assertIn("Error generating QR code", str(context.exception))

    
    @patch("cv2.QRCodeDetector.detectAndDecode")
    @patch("requests.get")
    def test_read_qr_code_valid_image(self, mock_requests_get, mock_detect_and_decode):
        # Mock a valid image fetch from requests
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = np.zeros((100, 100, 3), dtype=np.uint8).tobytes()
        mock_requests_get.return_value = mock_response
        
        # Mock OpenCV's QRCodeDetector behavior
        mock_detect_and_decode.return_value = ("Test Data", None, None)
        
        result = read_qr_code("http://valid-image-url.com")
        
        self.assertEqual(result, "Test Data")
        mock_requests_get.assert_called_once_with("http://valid-image-url.com")
        mock_detect_and_decode.assert_called_once()

        
    @patch("cv2.QRCodeDetector.detectAndDecode")
    @patch("requests.get")
    def test_read_qr_code_no_qr_data(self, mock_requests_get, mock_detect_and_decode):
        # Mock a valid image fetch from requests
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = np.zeros((100, 100, 3), dtype=np.uint8).tobytes()
        mock_requests_get.return_value = mock_response
        
        # Simulate no data being detected
        mock_detect_and_decode.return_value = ("", None, None)
        
        result = read_qr_code("http://valid-image-url.com")
        
        self.assertIsNone(result)
        mock_requests_get.assert_called_once_with("http://valid-image-url.com")
        mock_detect_and_decode.assert_called_once()

    
    @patch("requests.get")
    def test_read_qr_code_invalid_url(self, mock_requests_get):
        # Simulate a request exception
        mock_requests_get.side_effect = requests.exceptions.RequestException("Invalid URL")
        
        result = read_qr_code("http://invalid-url.com")
        
        self.assertIsNone(result)
        mock_requests_get.assert_called_once_with("http://invalid-url.com")
