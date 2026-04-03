from django import forms
from .models import ShippingAddress

GOVERNORATES = [
    ('', 'Select Governorate'),
    ('capital', 'Capital (العاصمة)'),
    ('hawalli', 'Hawalli (حولي)'),
    ('farwaniya', 'Farwaniya (الفروانية)'),
    ('ahmadi', 'Ahmadi (الأحمدي)'),
    ('jahra', 'Jahra (الجهراء)'),
    ('mubarak', 'Mubarak Al-Kabeer (مبارك الكبير)'),
]

class ShippingForm(forms.ModelForm):

    shipping_full_name = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
        required=True
    )
    shipping_email = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
        required=True
    )
    shipping_phone = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number (e.g. 99xxxxxx)'}),
        required=True
    )
    shipping_block = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Block Number'}),
        required=True
    )
    shipping_street = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Street Name/Number'}),
        required=True
    )
    shipping_house = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'House/Apartment Number'}),
        required=True
    )
    shipping_area = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Area (e.g. Salmiya, Rumaithiya)'}),
        required=True
    )
    shipping_governorate = forms.ChoiceField(
        label="",
        choices=GOVERNORATES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=True
    )
    shipping_country = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
        required=True,
        initial='Kuwait'
    )

    class Meta:
        model = ShippingAddress
        fields = ['shipping_full_name', 'shipping_email', 'shipping_phone',
                  'shipping_block', 'shipping_street', 'shipping_house',
                  'shipping_area', 'shipping_governorate', 'shipping_country']
        exclude = ['user',]