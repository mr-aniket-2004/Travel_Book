from django.contrib import admin
from .models import Profile_master ,TravelDiary ,Plan_trip , Categories, blogs, gallary



# Register your models here.

admin.site.register(Profile_master)
admin.site.register(TravelDiary)
admin.site.register(Plan_trip)
admin.site.register(Categories)
admin.site.register(blogs)
admin.site.register(gallary)