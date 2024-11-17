from django.test import SimpleTestCase
from unittest.mock import patch, MagicMock
from palette.functions import get_palette
import numpy as np


class GetPaletteTests(SimpleTestCase):
    @patch('palette.functions.urllib.request.urlopen')
    @patch('palette.functions.cv2.imdecode')
    @patch('palette.functions.ColorThief')
    def test_valid_image_url(self, mock_colorthief, mock_imdecode, mock_urlopen):
        # Mock urllib response
        mock_urlopen.return_value.read.return_value = b'\x89PNG\r\n\x1a\n'  # Simulated image bytes
        # Mock cv2 imdecode to return a valid numpy array (image-like)
        mock_imdecode.return_value = np.zeros((100, 100, 3), dtype=np.uint8)  # Simulated image
        # Mock ColorThief palette extraction
        mock_colorthief.return_value.get_palette.return_value = ['#FFFFFF', '#000000']

        result = get_palette("http://valid-image-url.com")
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)
        self.assertEqual(result, ['#FFFFFF', '#000000'])

    @patch('palette.functions.urllib.request.urlopen')
    def test_invalid_image_url(self, mock_urlopen):
        # Simulate an invalid URL response
        mock_urlopen.side_effect = Exception("Invalid image URL or unsupported image format")

        with self.assertRaises(ValueError):
            get_palette("http://invalid-image-url.com")

    @patch('palette.functions.urllib.request.urlopen')
    @patch('palette.functions.cv2.imdecode')
    def test_unsupported_image_format(self, mock_imdecode, mock_urlopen):
        # Mock urllib response
        mock_urlopen.return_value.read.return_value = b'\x89PNG\r\n\x1a\n'  # Simulated image bytes
        # Simulate imdecode failing to decode image
        mock_imdecode.return_value = None

        with self.assertRaises(ValueError):
            get_palette("http://unsupported-image-format-url.com")
