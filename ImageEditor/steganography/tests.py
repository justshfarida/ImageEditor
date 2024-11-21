from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from PIL import Image
import io

class SteganographyTests(TestCase):
    def setUp(self):
        self.image = self.create_image()
        self.message = "Hidden message"

    def create_image(self):
        """Create a sample in-memory image."""
        img = Image.new("RGB", (100, 100), color="blue")
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)
        return SimpleUploadedFile("test.png", buffer.read(), content_type="image/png")

    def test_encode_view(self):
        """Test the encode functionality."""
        response = self.client.post(reverse("steganography:upload", args=["encode"]), {
            "image": self.image,
            "message": self.message,
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Message Encoded Successfully")

    def test_decode_view(self):
        """Test the decode functionality."""
        # First, encode an image
        from steganography.utils import encode_message
        encoded_image = encode_message(self.image, self.message)

        uploaded_image = SimpleUploadedFile("encoded.png", encoded_image.getvalue(), content_type="image/png")
        response = self.client.post(reverse("steganography:upload", args=["decode"]), {
            "image": uploaded_image,
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.message)
