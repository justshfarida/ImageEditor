from django import forms 
from steg.models import Steg

class StegForm(forms.ModelForm):
    class Meta:
        model = Steg
        fields = "__all__"