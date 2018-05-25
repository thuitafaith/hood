from django.test import TestCase
from django.contrib.auth.models import User
from .models import Profile,Neighborhood,Business

# Create your tests here.
"""
Initialiazing Test Class Profile

"""
class ProfileTestClass(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("hdy", "hood@gmail.com", "neighborhood")
        self.new_profile =Profile(bio='this is a hood',location='hooding',national_identity='34451234',user_profile=self.user)
    def test_instance(self):
        self.new_profile.save()
        self.assertTrue(isinstance(self.new_profile,Profile))
    def test_save_method(self):
        self.new_profile.save_profile()
        profile = Profile.objects.all()
        self.assertTrue(len(profile)>0)
