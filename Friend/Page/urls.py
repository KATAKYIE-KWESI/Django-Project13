from django.urls import path
from . import views

urlpatterns = [
    path('', views.register, name='register'),
    path('firstpage/', views.firstpage, name='firstpage'),
    path('log_in/', views.log_in, name='log_in'),
    path('log_out/', views.log_out, name='log_out'),

]