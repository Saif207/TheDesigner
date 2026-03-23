from django.db import models
import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# Kuwait governorates
GOVERNORATES = [
    ('capital', 'Capital (العاصمة)'),
    ('hawalli', 'Hawalli (حولي)'),
    ('farwaniya', 'Farwaniya (الفروانية)'),
    ('ahmadi', 'Ahmadi (الأحمدي)'),
    ('jahra', 'Jahra (الجهراء)'),
    ('mubarak', 'Mubarak Al-Kabeer (مبارك الكبير)'),
]

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_modified = models.DateTimeField(auto_now=True)
    phone = models.CharField(max_length=20, blank=True)
    address1 = models.CharField(max_length=200, blank=True, verbose_name="Block & Street")
    address2 = models.CharField(max_length=200, blank=True, verbose_name="House/Apartment")
    governorate = models.CharField(max_length=20, choices=GOVERNORATES, blank=True, verbose_name="Governorate")
    area = models.CharField(max_length=100, blank=True, verbose_name="Area (e.g. Salmiya)")
    country = models.CharField(max_length=100, blank=True, default="Kuwait")

    def __str__(self):
        return self.user.username

# Automatically create a profile when a new user signs up
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()

post_save.connect(create_profile, sender=User)

class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Categories"

class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=10)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(default=0, decimal_places=2, max_digits=6)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    description = models.CharField(max_length=1000,default='', blank=True, null=True)
    image = models.ImageField(upload_to='uploads/products/')
    #Add Sale
    is_sale = models.BooleanField(default=False)
    sale_Price = models.DecimalField(default=0, decimal_places=2, max_digits=6)
    
    def __str__(self):
        return self.name 
    
class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    address = models.CharField(max_length=250,default='', blank=True, null=False)
    phone = models.CharField(max_length=20,default='', blank=False)
    date = models.DateField(default=datetime.datetime.today)
    status = models.BooleanField(default=False) 

    def __str__(self):
        return self.product