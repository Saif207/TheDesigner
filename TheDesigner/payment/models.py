from django.db import models
from django.contrib.auth.models import User

GOVERNORATES = [
    ('capital', 'Capital (العاصمة)'),
    ('hawalli', 'Hawalli (حولي)'),
    ('farwaniya', 'Farwaniya (الفروانية)'),
    ('ahmadi', 'Ahmadi (الأحمدي)'),
    ('jahra', 'Jahra (الجهراء)'),
    ('mubarak', 'Mubarak Al-Kabeer (مبارك الكبير)'),
]

class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    shipping_full_name = models.CharField(max_length=200)
    shipping_email = models.EmailField(max_length=200)
    shipping_phone = models.CharField(max_length=20, blank=True)
    shipping_block = models.CharField(max_length=100, blank=True)
    shipping_street = models.CharField(max_length=100, blank=True)
    shipping_house = models.CharField(max_length=100, blank=True)
    shipping_area = models.CharField(max_length=100, blank=True)
    shipping_governorate = models.CharField(max_length=20, choices=GOVERNORATES, blank=True)
    shipping_country = models.CharField(max_length=200, default='Kuwait')

    class Meta:
        verbose_name_plural = 'Shipping Address'

    def __str__(self):
        return f'Shipping Address - {str(self.id)}'