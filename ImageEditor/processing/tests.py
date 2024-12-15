from unittest.mock import patch, MagicMock
from django.test import SimpleTestCase
from processing.views import ProcessImage
from processing.helper import blur, color_to_grayscale, clr_to_bw, encrypt_image, decrypt_image, img_to_pdf, resize, sharp
import numpy as np
import cv2


class TestHelperFunctions(SimpleTestCase):
    """Unit tests for the helper functions."""

    def setUp(self):
        # Create a dummy image for testing
        self.test_image = np.ones((100, 100, 3), dtype=np.uint8) * 255

    def test_blur(self):
        result = blur(self.test_image)
        self.assertIsNotNone(result)

    def test_color_to_grayscale(self):
        result = color_to_grayscale(self.test_image)
        self.assertIsNotNone(result)

    def test_clr_to_bw(self):
        result = clr_to_bw(self.test_image)
        self.assertIsNotNone(result)

    def test_encrypt_image(self):
        result = encrypt_image(self.test_image, key=123)
        self.assertIsNotNone(result)

    def test_decrypt_image(self):
        encrypted_image = encrypt_image(self.test_image, key=123)
        decrypted_image = decrypt_image(np.asarray(bytearray(encrypted_image.getvalue()), dtype=np.uint8), key=123)
        self.assertIsNotNone(decrypted_image)

    def test_img_to_pdf(self):
        result = img_to_pdf(self.test_image)
        self.assertIsNotNone(result)

    def test_resize(self):
        result = resize(self.test_image, width=50, height=50)
        self.assertIsNotNone(result)

    def test_sharp(self):
        result = sharp(self.test_image)
        self.assertIsNotNone(result)


class TestProcessImageView(SimpleTestCase):
    """Unit tests for the ProcessImage view."""

    @patch('processing.views.Image.objects.get')
    @patch('urllib.request.urlopen')
    def test_post_valid_choice(self, mock_urlopen, mock_get):
        # Mock Image object
        mock_image = MagicMock()
        mock_image.img.url = 'http://example.com/test-image.png'
        mock_get.return_value = mock_image

        # Mock the URL open to return valid image data
        mock_image_data = np.ones((100, 100, 3), dtype=np.uint8) * 255  # Dummy white image
        _, encoded_image = cv2.imencode('.png', mock_image_data)
        mock_urlopen.return_value = MagicMock(read=lambda: encoded_image.tobytes())

        # Mock request object
        mock_request = MagicMock()
        mock_request.session = {'id': 1}
        mock_request.POST = {'type': 'Preview'}

        # Instantiate the view and call post
        view = ProcessImage()
        response = view.post(mock_request, choice=0)  # Valid choice (grayscale)
        self.assertEqual(response.status_code, 200)

    @patch('processing.views.Image.objects.get')
    @patch('urllib.request.urlopen')
    def test_post_invalid_choice(self, mock_urlopen, mock_get):
        # Mock Image object
        mock_image = MagicMock()
        mock_image.img.url = 'http://example.com/test-image.png'
        mock_get.return_value = mock_image

        # Mock the URL open (though it won't be used)
        mock_urlopen.return_value = MagicMock(read=lambda: b'image data')

        # Mock request object
        mock_request = MagicMock()
        mock_request.session = {'id': 1}

        # Instantiate the view and call post
        view = ProcessImage()
        response = view.post(mock_request, choice=999)  # Invalid choice
        self.assertEqual(response.status_code, 200)
        self.assertIn("Invalid Option", str(response.content))
