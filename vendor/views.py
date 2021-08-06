from django.http import request
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from vendor import forms
from shop.models import Product
from vendor import models
from django.template.defaultfilters import slugify
from django.views.generic.edit import UpdateView
# Create your views here.


class VendorRegistrationView(LoginRequiredMixin,FormView):
    template_name = "vendor/vendor_registration.html"
    form_class = forms.VendorRegisterationForm
    success_url = reverse_lazy('home')


    def form_valid(self, form):
        response = super().form_valid(form)
        form.instance.vendor = self.request.user
        user_profile = self.request.user.get_profile()
        user_profile.is_vendor = True
        user_profile.save()
        form.save()
        return response


class VendorShopView(View):
    def get(self, request):
        if request.user.get_profile().is_vendor:
            vendor = models.Vendor.objects.get(vendor=request.user)
            vendor_products = Product.objects.filter(vendor=vendor)
            current_vendor = models.Vendor.objects.get(vendor=request.user)
            vendor_orders = current_vendor.orders.all()
            
            



            context = {
                'vendor': vendor,
                'vendor_products': vendor_products,
                'vendor_orders': vendor_orders
                }    
            return render(request, 'vendor/vendor_shop.html', context=context)
        return render(request, 'errors/not_a_vendor.html', status=401)


class VendorUpdateView(UpdateView):
    template_name = 'vendor/vendor_update.html'
    model = models.Vendor
    fields = ['shop_name', 'shop_description', 'phone_number']