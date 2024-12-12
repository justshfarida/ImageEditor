from django.test import TestCase, Client
from io import BytesIO
import numpy as np
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from unittest.mock import patch
import os
from core.models import Image
from processing.helper import blur, color_to_grayscale, img_to_pdf, clr_to_bw, resize, encrypt_image, decrypt_image, sharp


class AdminTests(TestCase):
    def test_admin_registration(self):
        from django.contrib.admin.sites import site
        from processing.admin import SinImgAdmin
        self.assertIn(Image, site._registry)
        self.assertIsInstance(site._registry[Image], SinImgAdmin)


class HelperTests(TestCase):
    def setUp(self):
        # Create a 100x100 dummy black image
        self.test_img = np.zeros((100, 100, 3), dtype=np.uint8)

    def test_blur(self):
        result = blur(self.test_img)
        self.assertIsInstance(result, BytesIO)

    def test_color_to_grayscale(self):
        result = color_to_grayscale(self.test_img)
        self.assertIsInstance(result, BytesIO)

    def test_img_to_pdf(self):
        result = img_to_pdf(self.test_img)
        self.assertIsInstance(result, BytesIO)

    def test_clr_to_bw(self):
        result = clr_to_bw(self.test_img)
        self.assertIsInstance(result, BytesIO)

    def test_resize(self):
        result = resize(self.test_img, width=50, height=50)
        self.assertIsInstance(result, BytesIO)

    def test_encrypt_and_decrypt_image(self):
        # Test encryption
        encrypted = encrypt_image(self.test_img, key=123)
        self.assertIsInstance(encrypted, BytesIO)

        # Test decryption
        decrypted = decrypt_image(self.test_img, key=123)
        self.assertIsInstance(decrypted, BytesIO)

    def test_sharp(self):
        result = sharp(self.test_img)
        self.assertIsInstance(result, BytesIO)

class ViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.upload_url = reverse("processing:upload")
        self.choice_url = reverse("processing:select_choice")
        self.process_url = reverse("processing:process", kwargs={"choice": 0})

        # Create test files using SimpleUploadedFile
        self.test_image_path = os.path.join('test_data', 'test_valid.png')
        with open(self.test_image_path, 'rb') as img_file:
            self.sample_image = SimpleUploadedFile(
                name='test_valid.png',
                content=img_file.read(),
                content_type='image/png'
            )

        self.test_pdf_path = os.path.join('test_data', 'test_valid.pdf')
        with open(self.test_pdf_path, 'rb') as pdf_file:
            self.sample_pdf = SimpleUploadedFile(
                name='test_valid.pdf',
                content=pdf_file.read(),
                content_type='application/pdf'
            )

        # Create mock image object and store its ID in the session
        self.image = Image.objects.create(img="test_image.png")
        session = self.client.session
        session["id"] = self.image.id
        session.save()

    def test_get_upload_page(self):
        response = self.client.get(self.upload_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "sinimg/upload.html")

    def test_post_valid_image(self):
        response = self.client.post(self.upload_url, {"img": self.sample_image})
        self.assertEqual(response.status_code, 302)  # Redirect after upload
        self.assertIn("id", self.client.session)  # Session contains uploaded image ID

    @patch("processing.helper.color_to_grayscale")
    def test_post_grayscale_processing(self, mock_grayscale):
        mock_grayscale.return_value = self.sample_image

        response = self.client.post(self.process_url, {"type": "Preview"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "image/png")

    @patch("processing.helper.img_to_pdf")
    def test_post_pdf_processing(self, mock_pdf):
        mock_pdf.return_value = self.sample_pdf

        process_url = reverse("processing:process", kwargs={"choice": 1})
        response = self.client.post(process_url, {"type": "Download"})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.has_header("Content-Disposition"))
        self.assertIn("demo.pdf", response["Content-Disposition"])

    def test_missing_file_submission(self):
        response = self.client.post(self.upload_url, {})
        self.assertEqual(response.status_code, 302)  # Redirect back to form
        self.assertRedirects(response, self.upload_url)
