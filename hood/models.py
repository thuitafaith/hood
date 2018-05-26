from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
"""
Initialiazing the Profile model

"""
class Profile(models.Model):
    user_profile = models.OneToOneField(User)
    user_photo = models.ImageField(upload_to='pics/',null=True,blank
                                      =True)
    name= models.CharField(max_length=80,default=False)
    bio = models.TextField(blank=True,null=True)
    location= models.CharField(max_length=100,null=True)
    email= models.CharField(max_length=100)
    email_confirmed = models.BooleanField(default=False)
    national_identity = models.CharField(max_length=50)
    neighborhood = models.ForeignKey('Neighborhood', related_name ='hood_area',null=True)

    def save_profile(self):
        self.save()
    def delete_profile(self):
        self.delete()
@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user_profile=instance)
    instance.profile.save()


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
