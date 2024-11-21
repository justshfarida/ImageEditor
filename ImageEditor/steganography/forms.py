from django import forms

class EncodeForm(forms.Form):
    image = forms.ImageField(label="Select an image to encode")
    message = forms.CharField(label="Message to encode", widget=forms.Textarea, required=True)

class DecodeForm(forms.Form):
    image = forms.ImageField(label="Select an image to decode")
