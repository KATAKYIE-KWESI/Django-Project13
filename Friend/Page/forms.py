from django import forms
from .models import Profile
from .models import Post

class ProfilePicForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_pic']



class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['caption', 'image']
