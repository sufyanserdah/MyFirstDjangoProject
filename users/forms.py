from typing import Any
from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView,LogoutView
from django.urls import reverse_lazy
from blog.models import Post
from .models import Profile
from crispy_forms.helper import FormHelper
class RegisterForm(UserCreationForm):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None
        self.fields['username'].help_text = None
        self.fields['email'].help_text = None
        self.fields["username"].widget.attrs.update({
            "class":"input100",
            
            "type":"text",
            "name":"fullname",
            "placeholder":"Full name",
        })
        self.fields["email"].widget.attrs.update({
            "class":"input100",
           
            "type":"text",
            "name":"email",
            "placeholder":"Email",
            
            
        })
        self.fields["password1"].widget.attrs.update({
            "class":"input100",
            "type":"password",
            
            "name":"pass",
            "placeholder":"Password",
            
            "id":"password1",
            
            
        })
        self.fields["password2"].widget.attrs.update({
            "class":"input100",
            "type":"password",
            
            "name":"pass2",
            "id":"password2",
           
            "placeholder":"Password Confirm",
            
            
        })
    def clean_email(self):
        email = self.cleaned_data.get("email")
    
        user_count = User.objects.filter(email=email).count()
        if user_count > 0:
            raise forms.ValidationError("this email is already in use")
        return email
            
            
    class Meta:
        model = User
        fields = ['username','email','password1','password2']
       