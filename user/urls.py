from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'), # type: ignore
    path('login/', views.login, name='login'), # type: ignore
    path('', views.home, name='home'), # type: ignore
]