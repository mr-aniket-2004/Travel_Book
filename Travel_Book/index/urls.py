from django.urls import path
from . import views

urlpatterns = [
    path('',views.index, name='index'),
    path('userlogin/',views.UserLogin, name='userlogin'),
    path('resgister/',views.UserRegister, name='resgister'),
    
]