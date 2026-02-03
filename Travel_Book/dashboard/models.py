from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile_master(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    about = models.TextField(blank=True,null=True)
    profile_photo = models.ImageField(upload_to='profile_pics/',blank=True,null=True)
    First_name = models.CharField(max_length=100)
    Last_name = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username
    


class Categories(models.Model):
    name = models.CharField(max_length=250)
    descriptions = models.TextField()

    def __str__(self):
        return self.name


class TravelDiary(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    title = models.CharField(max_length=200)
    location = models.CharField(max_length=200)

    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)

    description = models.TextField()
    highlights = models.TextField(blank=True)

    cover_photo = models.ImageField(
        upload_to='travel_diary/',
        null=True,
        blank=True
    )

    is_public = models.BooleanField(default=False)
    categories = models.ForeignKey(Categories ,on_delete=models.CASCADE,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    



class Plan_trip(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    title = models.CharField(max_length=200)
    location = models.CharField(max_length=200)

    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)

    description = models.TextField()
    highlights = models.TextField(blank=True)

    cover_photo = models.ImageField(
        upload_to='travel_diary/',
        null=True,
        blank=True
    )

    is_public = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    categories = models.ForeignKey(Categories ,on_delete=models.CASCADE,blank=True)

    def __str__(self):
        return self.title
    


class blogs(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    title = models.CharField(max_length=500)
    about = models.CharField(max_length=500)
    body = models.TextField()
    categories = models.ForeignKey(Categories ,on_delete=models.CASCADE,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_public = models.BooleanField(default=False)

    def __str__(self):
        return self.title+"---"+self.user.username
    
class gallary(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.ForeignKey(TravelDiary,on_delete=models.CASCADE)
    description = models.TextField()
    is_public= models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='gallary/',null=True,blank=True)

    def __str__(self):
        return self.name.title+"---"+self.user.username
    


