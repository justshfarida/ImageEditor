from unittest.mock import patch, MagicMock
from django.test import SimpleTestCase
from steg.views import ProcessImage, Upload
from steg.functions import hide_lsb, reveal_lsb
import numpy as np
import cv2
from io import BytesIO


class TestHelperFunctions(SimpleTestCase):
    """Unit tests for the helper functions."""

    def test_hide_lsb(self):
        # Create a sample image
        test_image = np.ones((100, 100, 3), dtype=np.uint8) * 255  # White image
        result = hide_lsb(test_image, "Hidden Message")
        self.assertIsNotNone(result)  # Ensure the function returns a result

    def test_reveal_lsb(self):
        # Create an LSB-encoded image
        test_image = np.ones((100, 100, 3), dtype=np.uint8) * 255  # White image
        _, encoded_image = cv2.imencode('.png', test_image)
        io_buf = BytesIO(encoded_image.tobytes())
        hidden_image = hide_lsb(test_image, "Secret Message")
        hidden_data = np.frombuffer(hidden_image.getvalue(), np.uint8)
        decoded_image = cv2.imdecode(hidden_data, -1)
        
        # Reveal the hidden message
        message, _ = reveal_lsb(decoded_image)
        self.assertEqual(message, "Secret Message")  # Ensure the message is correct


class TestProcessImageView(SimpleTestCase):
    """Unit tests for the ProcessImage view."""

    @patch('steg.views.Steg.objects.get')
    @patch('urllib.request.urlopen')
    def test_post_reveal_lsb(self, mock_urlopen, mock_get):
        # Mock Steg object
        mock_steg = MagicMock()
        mock_steg.img.url = 'http://example.com/test-image.png'
        mock_get.return_value = mock_steg

        # Create a valid LSB-encoded image
        original_image = np.ones((100, 100, 3), dtype=np.uint8) * 255  # White image
        _, encoded_image = cv2.imencode('.png', original_image)
        io_buf = BytesIO(encoded_image.tobytes())

        # Use PIL to create an image compatible with stegano.lsb
        from PIL import Image
        pil_image = Image.open(io_buf)

        # Convert PIL image to NumPy array for OpenCV compatibility
        cv_image = np.array(pil_image)

        # Hide a secret message using the `hide_lsb` function
        hidden_image = hide_lsb(cv_image, "Secret Message")

        # Save the hidden image to a buffer as PNG
        hidden_data = np.frombuffer(hidden_image.getvalue(), np.uint8)

        # Mock the URL open to return the LSB-encoded image data
        mock_urlopen.return_value = MagicMock(read=lambda: hidden_data.tobytes())

        # Mock request object
        mock_request = MagicMock()
        mock_request.session = {'id': 1}
        mock_request.POST = {'type': 'Preview'}

        # Instantiate the view and call post
        view = ProcessImage()
        response = view.post(mock_request, choice=1)  # LSB Reveal
        self.assertEqual(response.status_code, 200)


class TestUploadView(SimpleTestCase):
    """Unit tests for the Upload view."""

    @patch('steg.views.StegForm')
    def test_post_invalid_form(self, mock_form):
        # Mock form
        mock_form_instance = MagicMock()
        mock_form_instance.is_valid.return_value = False
        mock_form.return_value = mock_form_instance

        # Mock request object
        mock_request = MagicMock()
        mock_request.path = '/steg/upload/'  # Mock a valid path

        # Instantiate the view and call post
        view = Upload()
        response = view.post(mock_request)
        self.assertEqual(response.status_code, 302)  # Ensure it redirects correctly
