from django.db import models
from django.contrib.auth.models import User
# Create your models here.
"""
Initialiazing the Profile model

"""
class Profile(models.Model):
    user_profile = models.OneToOneField(User)
    name= models.CharField(max_length=80,default=False)
    bio = models.TextField(blank=True,null=True)
    location= models.CharField(max_length=100,null=True)
    email= models.CharField(max_length=100)
    national_identity = models.CharField(max_length=50)
    neighborhood = models.ForeignKey('Neighborhood', related_name ='hood_area',null=True)
"""
Initialiazing the Neighborhood model

"""
class Neighborhood(models.Model):
    name = models.CharField(max_length=80,default=False)
    location = models.CharField(max_length=60,null=True)
    user_profile = models.ForeignKey('Profile',null=True,related_name ='hood_owner')
"""
Initialiazing the Business model

"""
class Business(models.Model):
    business_name = models.CharField(max_length=80,default=False)
    email = models.CharField(max_length=80)
    neighborhood = models.ForeignKey('Neighborhood')
    user_profile = models.ForeignKey('Profile',null=True)
