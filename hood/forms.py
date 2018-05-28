from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Business,Neighborhood

class SignUpForm(UserCreationForm):

    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )
class EditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email',)
class HoodForm(forms.ModelForm):
    class Meta:
        model = Neighborhood
        fields = ('name','location')
