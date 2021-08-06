from django.urls import path
from vendor import views


urlpatterns = [
    path('registration/', views.VendorRegistrationView.as_view(), name="vendor_registration"),
    path('my-shop/', views.VendorShopView.as_view(), name="vendor_shop"),
    path('<int:pk>/', views.VendorUpdateView.as_view(), name="vendor_update"),
]