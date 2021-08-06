from django.urls import path
from django.views.generic.base import TemplateView
from . import views


urlpatterns = [
    path('products/', views.ProductListView.as_view(), name="products"),
    path('<int:product_id>/', views.ProductDetailView, name='product_detail'),
    path('add-product/', views.ProductCreateView.as_view(), name='add_product'),
    path('cart/', views.CartView.as_view(), name='cart'),
    path('success/', TemplateView.as_view(template_name="shop/payment_success.html"), name='payment_success'),
]