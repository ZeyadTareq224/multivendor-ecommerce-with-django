from django.contrib import admin
from shop import models

admin.site.register(models.ProductCatrgory)
admin.site.register(models.ProductImage)
admin.site.register(models.Product)
admin.site.register(models.OrderItem)
admin.site.register(models.Order)


