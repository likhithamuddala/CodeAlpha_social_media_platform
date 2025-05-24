from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),  # This registers '' URL as 'index'
    path('about/', views.about, name='about'),  # example other page
]