from django.urls import path

from Travel_Book import settings
from . import views

urlpatterns = [
    path('',views.Dashboard, name='dashboard'),
    path('profile/',views.profile_view, name='profile'),
    path('trip/',views.mytrip, name='trip'),
    path('add_diary/',views.add_diary, name='add_diary'),
    path('diary/<int:id>/', views.diary_detail, name='diary_detail'),
    path('edit_diary/<int:id>/', views.edit_diary, name='edit_diary'),
    path('delete_diary/<int:id>/', views.delete_diary, name='delete_diary'),
    path('plan_trip/',views.plan_trip, name='plan_trip'),
    path('edit_plantrip/<int:id>/',views.edit_plantrip, name='edit_plantrip'),
    path('delete_plantrip/<int:id>/',views.delete_plan_trip, name='delete_plan_trip'),
    path('blogs/',views.Blogs, name='blogs'),
    path('create_blog/',views.create_blog, name='create_blog'),
    path('blog_details/<int:id>/', views.blog_details, name='blog_details'),
    path('delete_blog/<int:id>/', views.delete_blog, name='delete_blog'),
    path('gallery/',views.gallery, name='gallery'),
    path('upload_photo/',views.upload_photo, name='upload_photo'),  
    path('delete_photo/<int:id>/',views.delete_photo, name='delete_photo'),
    path('journey/',views.journey, name='journey'),
    path('change_password/',views.change_password, name='change_password'),
    path('check-username/', views.check_username, name='check_username'),
    path('check-email/', views.check_email, name='check_email'),
    path('logout/',views.Userlogout, name='logout'),

]


