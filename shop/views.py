from django.contrib import messages
from django.http import request
from django.shortcuts import redirect, render
from django.views.generic import ListView, DetailView, View
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from . import models
from .forms import ProductCreateForm, AddToCartFrom, CheckoutForm
from vendor.models import Vendor
import random
from .cart import Cart
from .utilities import checkout
import stripe
from django.conf import settings


class ProductListView(ListView):
    model = models.Product
    template_name = "shop/product_list.html"
    paginate_by = 12

    def get_queryset(self):
        qs = models.Product.objects.select_related('category').all()
        return qs



    
def ProductDetailView(request, product_id):
    cart = Cart(request)


    product = models.Product.objects.get(id=product_id)
    product_images = models.ProductImage.objects.filter(product=product)[1:]


    if request.method == "POST":
        form = AddToCartFrom(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            cart.add(product_id=product_id, quantity=quantity, update_quantity=False)
            messages.success(request, 'The product was added to the cart.')
            return redirect('product_detail', product_id=product_id)
    else:
        form = AddToCartFrom(request.POST)


    # querying similar products and it's RELATED_CATEGORIES:(to reduce the number of queries made to get each object in similar products qs) filtered by product category
    similar_products = (
        models.Product.objects.
        select_related('category').
        filter(category=product.category).
        exclude(id=product.id)
    )

    # returning randomized similar products to the context if there are more than 4 or more products in the category
    # otherwise return the all products in the category
    similar_products_list =list(similar_products)
    if len(similar_products_list) >= 4:
        similar_products = random.sample(similar_products_list, 4)
    
    context = {
        'product': product,
        'product_images': product_images,
        'similar_products': similar_products,
        'form': form
    }
    return render(request, 'shop/product_details.html', context)


    



class ProductCreateView(View):

    def get(self, request):
        product_form = ProductCreateForm()
        context = {'product_form': product_form}
        return render(request, 'shop/add_product.html', context)

    def post(self, request):
        product_form = ProductCreateForm(request.POST)
        current_vendor = Vendor.objects.get(vendor=request.user)

        # validating and saving the product form
        if product_form.is_valid():
            product_form.instance.vendor = current_vendor
            product = product_form.save()

            # creating images for the same product that was just created
            images = request.FILES.getlist('images')
            for image in images:
                product_image_obj = models.ProductImage(
                    image = image,
                    product = product
                )
                product_image_obj.save()


            messages.Info(request, "Product created successfully.")
            return redirect('vendor_shop')
        else:
            messages.warning(request, "Something went wrong.")
            return redirect('add_product')
        


class CartView(View):
    def get(self, request):
        cart = Cart(request)

        form = CheckoutForm()

        product_to_remove_id = request.GET.get('remove_from_cart', '')
        product_to_change_quantity_id = request.GET.get('change_quantity', '')
        quantity = request.GET.get('quantity', 0)

        if product_to_remove_id:
            cart.remove(product_to_remove_id)
            return redirect('cart')

        if product_to_change_quantity_id:
            cart.add(product_to_change_quantity_id, quantity, True)
            return redirect('cart')

        context = {'form': form, 'stripe_pub_key': settings.STRIPE_PUB_KEY}
        return render(request, 'shop/cart.html', context)

    def post(self, request):
        cart = Cart(request)
        form = CheckoutForm(request.POST)
        if form.is_valid():
            stripe.api_key =  settings.STRIPE_SECRET_KEY
            stripe_token = form.cleaned_data['stripe_token']
            charge = stripe.Charge.create(
                amount = int(cart.get_total_cost() * 100),
                currency = 'USD',
                description = 'charge form genshop',
                source = stripe_token
            )
            full_name = form.cleaned_data['full_name']
            address = form.cleaned_data['address']
            zip_code = form.cleaned_data['zip_code']
            city = form.cleaned_data['city']
            country = form.cleaned_data['country']
            
            order = checkout(
                request,
                full_name,
                address,
                zip_code,
                city,
                country,
                cart.get_total_cost()
            )

            cart.clear()
            return redirect('payment_success')
