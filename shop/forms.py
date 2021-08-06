from django import forms
from shop import models

class ProductCreateForm(forms.ModelForm):
    class Meta:
        model = models.Product
        fields = [
            'product_name',
            'product_description',
            'price',
            'in_stock',
            'category',
            ]


class AddToCartFrom(forms.Form):
    quantity = forms.IntegerField()


class CheckoutForm(forms.Form):
    SUPPORTED_COUNTRIES = (
        ("uk", "United Kingdom"),
        ("us", "United States of America"),
    )
    
    full_name = forms.CharField(max_length=60)
    address = forms.CharField(max_length=60)
    zip_code = forms.CharField(max_length=12)
    city = forms.CharField(max_length=60)
    country = forms.ChoiceField(choices=SUPPORTED_COUNTRIES)
    stripe_token = forms.CharField(max_length=255)