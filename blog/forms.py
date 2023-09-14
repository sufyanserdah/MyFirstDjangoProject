from django import forms
from crispy_forms.helper import FormHelper
from typing import Any
from django.forms import ImageField, FileInput

from users.models import Profile
from .models import Post,Comment
class PostModelForm(forms.ModelForm):
    
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.fields["content"].help_text = None
        self.fields['content'].label = ""
        self.fields["content"].widget.attrs.update({
            "class":"w-full p-3 fs-16",
            "style":"height: 75px;resize: none;color: #666666;    border-radius: 5px;",
            "type":"text",
            "name":"cont",
            "id":"cont", 
            
            "placeholder":"What about today?",
            
            
            
        })
        self.fields["post_image"].help_text = None
        self.fields['post_image'].label = ""
    
        self.fields["post_image"].widget.attrs.update({
            "name":"post_image",
            "id":"post_image", 
           
            "style":"opacity:0%; height: 40px; width: 29px; margin-left:5%;position: absolute;",
            
            
            
            
            
        })
        
    class Meta:
        model = Post
        fields=('content','post_image')
       
        
class ProfileModelForm(forms.ModelForm):
    image = ImageField(widget=FileInput)
    bgimage = ImageField(widget=FileInput)
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.fields["image"].help_text = None
        self.fields['image'].label = ""
        self.fields["image"].widget.attrs.update({
            
            "style":"     margin-left: 2%; margin-bottom: -28%; height: 12px; width: 37%; position: absolute; opacity:0%", 

        })
        self.fields["bgimage"].help_text = None
        self.fields['bgimage'].label = ""
        self.fields["bgimage"].widget.attrs.update({
            
                        "style":"    margin-left: 55%; margin-bottom: -13%; height: 15px; width: 30%; position: absolute;opacity:0%", 


        })
    class Meta:
        model = Profile
        fields = ('image','bgimage')
        
        
        
        
        
class CommentModelForm(forms.ModelForm):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.fields["body"].help_text = None
        self.fields['body'].label = ""
        self.fields["body"].widget.attrs.update({
            "class":"p-2 fs-14 pl-3",
            "style":" background:transparent; width:100%;",
            "id":"fullname",
            "type":"text",
            "name":"fullname",
            "placeholder":"What about today?",
            
            
            
            
        })
    class Meta:
        model = Comment
        fields =('body',)