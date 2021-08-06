from django.db import models
from django.utils.text import slugify
from vendor.models import Vendor
from django.core.validators import MinValueValidator
from django.conf import settings
from django.urls import reverse
from django.contrib.auth import get_user_model

class ProductCatrgory(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name





class Product(models.Model):
    product_name = models.CharField(max_length=50)
    product_description = models.TextField()
    price = models.DecimalField(max_digits=20, decimal_places=2)
    in_stock = models.BooleanField(default=True)
    slug = models.SlugField(max_length=48)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    category = models.ForeignKey(ProductCatrgory, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product_name}-{self.id}"

    class Meta:
        ordering = ['-created_at']


    def get_absolute_url(self):
        return reverse('product_detail', args=[self.id])

    
    def get_product_main_image(self):
        return self.productimage_set.all()[0]

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.product_name)

        super(Product, self).save(*args, **kwargs)


        
class ProductImage(models.Model):
    image = models.ImageField(upload_to='ProductImages')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)




class Order(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    paid_amount = models.DecimalField(max_digits=8, decimal_places=2)
    vendors = models.ManyToManyField(Vendor, related_name='orders')

    # address fields
    SUPPORTED_COUNTRIES = (
        ("uk", "United Kingdom"),
        ("us", "United States of America"),
    )

    full_name = models.CharField(max_length=60)
    address = models.CharField("Address line 1", max_length=60)
    zip_code = models.CharField("ZIP / Postal code", max_length=12)
    city = models.CharField(max_length=60)
    country = models.CharField(max_length=3, choices=SUPPORTED_COUNTRIES)


    class Meta:
        ordering = ['-created_at']

    def is_empty(self):
        return self.OrderItem_set.all().count() == 0

    def cart_count(self):
        return sum(i.quantity for i in self.OrderItem_set.all())

    def total_price(self):
        return sum(i.product.price for i in self.OrderItem_set.all())



class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='items')
    vendor_paid = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def get_total_price(self):
        return self.price * self.quantity