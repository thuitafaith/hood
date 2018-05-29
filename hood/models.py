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
    user_photo = models.ImageField(upload_to='pics/',null=True)
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

    @classmethod
    def update_profile_hood(cls, user_id, value):
        cls.objects.filter(user_profile=user_id).update(neighborhood=value)

    @classmethod
    def update_profile_neighborhood(cls,user_id,value):
        cls.objects.filter(user_profile=id).update(profile_neighborhood=value)

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user_profile=instance)
    instance.profile.save()


"""
Initialiazing the Neighborhood model

"""
class Neighborhood(models.Model):
    name = models.CharField(max_length=80)
    location = models.CharField(max_length=60,null=True)
    user_profile = models.ForeignKey('Profile',null=True,related_name ='hood_owner')

    def __str__(self):
        return str(self.name)


"""
Initialiazing the Business model

"""
class Business(models.Model):
    business_name = models.CharField(max_length=80)
    email = models.CharField(max_length=80)
    neighborhood = models.ForeignKey('Neighborhood')
    user_profile = models.ForeignKey('Profile')
class Post(models.Model):
    title = models.CharField(max_length=80)
    description = models.TextField()
    editor = models.ForeignKey(User)
    pub_date = models.DateTimeField(auto_now_add=True)
    post_image = models.ImageField(upload_to='pics/',null=True)
    neighborhood = models.ForeignKey('Neighborhood',null=True)
