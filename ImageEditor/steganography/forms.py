from django import forms
from .models import SteganographyImage

class EncodeForm(forms.ModelForm):
    class Meta:
        model = SteganographyImage
        fields = ['original_image', 'message']

class DecodeForm(forms.Form):
    encoded_image = forms.ImageField()
