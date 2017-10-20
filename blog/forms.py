from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Blog


class inputform(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea(attrs={'rows':'5', 'cols':'10','class':'form-control'}),required=True, help_text="fill your story")
    name =  forms.CharField(max_length=60,required=True)
    class Meta:
        model = Blog
        fields = ('name', 'description','category')


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    #bio = forms.CharField(max_length=30, required=False, help_text='Optional.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',)


class editform(forms.Form):

    Edit=forms.CharField(widget=forms.Textarea(attrs={'rows':'5', 'cols':'10','class':'form-control'}),max_length=1000, required=True   )
