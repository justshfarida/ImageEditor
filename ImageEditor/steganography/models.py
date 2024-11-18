from django.db import models

class SteganographyImage(models.Model):
    original_image = models.ImageField(upload_to='steganography/originals/')
    encoded_image = models.ImageField(upload_to='steganography/encoded/', blank=True, null=True)
    message = models.TextField(blank=True, null=True)  # Hidden message

    def __str__(self):
        return f"Image {self.id}"
