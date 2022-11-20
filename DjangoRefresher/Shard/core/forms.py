from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django import forms
from django.forms import ModelForm
from .models import User,Post,Profile,Comment


class MyUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label =  'Username'
        self.fields['password1'].label = 'Enter Password'
        self.fields['password2'].label = 'Verify Password'

        self.fields['username'].help_text = ''
        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''

    class Meta:
        model = User
        fields = ['username','password1','password2']
    
class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title','text','image']

        
class LoginForm(AuthenticationForm):
    class Meta:
        model = User

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['bio','avatar']

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['text']