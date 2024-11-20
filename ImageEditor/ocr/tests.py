from django.test import TestCase, Client
from django.urls import reverse_lazy
from unittest.mock import patch
from core.models import Image
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
import os

class OCRUploadTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.upload_url = reverse_lazy('ocr:upload')
        self.valid_language = list(settings.OCR_LANGUAGES.keys())[0]  # Choose a valid language
        self.invalid_language = 'xx'  # Assume 'xx' is not a valid language
        self.test_image_path = os.path.join('test_data', 'test_valid.png')
        with open(self.test_image_path, 'rb') as img_file:
            self.test_image = SimpleUploadedFile(
                name='test_valid.png',
                content=img_file.read(),
                content_type='image/png'
            )

    @patch('ocr.views.ocr')  # Mock the OCR function
    def test_valid_submission(self, mock_ocr):
        mock_ocr.return_value = "Extracted text from OCR"
        
        response = self.client.post(self.upload_url, {
            'img': self.test_image,
            'language': self.valid_language
        })

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Extracted text from OCR")
        self.assertTemplateUsed(response, 'ocr/result.html')

    def test_missing_file_submission(self):
        response = self.client.post(self.upload_url, {
            'language': self.valid_language
        })

        self.assertEqual(response.status_code, 302)  # Redirect back to form
        self.assertRedirects(response, self.upload_url)

    def test_invalid_language_submission(self):
        response = self.client.post(self.upload_url, {
            'img': self.test_image,
            'language': self.invalid_language
        })

        self.assertEqual(response.status_code, 302)  # Redirect back to form
        self.assertRedirects(response, self.upload_url)

    @patch('ocr.views.ocr')
    def test_ocr_error_handling(self, mock_ocr):
        mock_ocr.side_effect = Exception("OCR processing error")

        response = self.client.post(self.upload_url, {
            'img': self.test_image,
            'language': self.valid_language
        })

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.upload_url)

    def test_get_upload_page(self):
        response = self.client.get(self.upload_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ocr/upload.html')
        self.assertContains(response, "form")  # Ensure form is rendered
        self.assertContains(response, settings.DEFAULT_OCR_LANG)
