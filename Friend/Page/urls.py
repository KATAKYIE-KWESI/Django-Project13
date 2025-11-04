from django.urls import path
from . import views

urlpatterns = [
    path('', views.register, name='register'),
    path('firstpage/', views.firstpage, name='firstpage'),
    path('log_in/', views.log_in, name='log_in'),
    path('log_out/', views.log_out, name='log_out'),
    path('upload-profile/', views.upload_profile_pic, name='upload_profile_pic'),
    path('create-post/', views.create_post, name='create_post'),
    path('delete-post/<int:post_id>/', views.delete_post, name='delete_post'),
]