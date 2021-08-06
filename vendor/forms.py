from django import forms
from vendor import models


class VendorRegisterationForm(forms.ModelForm):
    class Meta:
        model = models.Vendor
        fields = ['shop_name', 'shop_description', 'phone_number']


