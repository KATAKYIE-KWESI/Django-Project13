from django.urls import path
from . import views

urlpatterns = [
    path('', views.register, name='register'),
    path('firstpage/', views.firstpage, name='firstpage'),
    path('log_in/', views.log_in, name='log_in'),
    path('logout/', views.logout, name='logout'),

]