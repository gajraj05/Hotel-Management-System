from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_booking, name='create_booking'),
    path('cancel/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    path('checkout/<int:booking_id>/', views.checkout_booking, name='checkout_booking'),
]