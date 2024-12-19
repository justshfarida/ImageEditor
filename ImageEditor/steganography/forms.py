from django import forms 
from .models import SteganographyModel

class SteganographyForm(forms.ModelForm):
    class Meta:
        model = SteganographyModel
        fields = "__all__"
