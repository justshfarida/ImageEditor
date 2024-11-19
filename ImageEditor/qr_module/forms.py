from django import forms

class QRCodeForm(forms.Form):
    data = forms.CharField(label='Data for QR Code', max_length=255)
    fill_color = forms.CharField(label='Fill Color', max_length=50, required=False)
    back_color = forms.CharField(label='Background Color', max_length=50, required=False)

class QRCodeReadForm(forms.Form):
    image = forms.ImageField(label="Upload a QR Code Image")