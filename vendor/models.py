from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.urls import reverse



class Vendor(models.Model):
    vendor = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    shop_name = models.CharField(max_length=50)
    shop_description = models.TextField()
    phone_number = models.CharField(max_length=50)
    slug = models.SlugField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    
    def __str__(self):
        return f"vendor: {self.vendor}"

    def get_absolute_url(self):
        return reverse('vendor_shop')

    def get_balance(self):
        items = self.items.filter(vendor_paid=False, order__vendors__in=[self.id])
        return sum(item.product.price * item.quantity for item in items)


    def get_paid_amount(self):
        items = self.items.filter(vendor_paid=True, order__vendors__in=[self.id])
        return sum(item.product.price * item.quantity for item in items)


    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.shop_name)

        super(Vendor, self).save(*args, **kwargs)
