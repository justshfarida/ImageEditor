from django.db import models

class Steganography(models.Model):
    original_image = models.ImageField(upload_to='steganography/original/')
    encoded_image = models.ImageField(upload_to='steganography/encoded/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
