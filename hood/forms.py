from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post

class SignUpForm(UserCreationForm):

    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )
class EditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email',)
class NewPostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ['editor', 'pub_date']
