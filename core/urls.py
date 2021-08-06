from django.urls import path, include
from django.views.generic import TemplateView
from . import views


urlpatterns = [
    path('', TemplateView.as_view(template_name='core/home.html'), name='home'),
    path('accounts/', include('allauth.urls')),
    path('contact/', TemplateView.as_view(template_name='core/contact.html'), name='contact'),
]