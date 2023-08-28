from django import forms
from crispy_forms.helper import FormHelper
from typing import Any

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
            
            "style":"opacity:0; height: 40px; width: 200px;",
            
            
            
            
            
        })
        
    class Meta:
        model = Post
        fields=('content','post_image')
       
        
class ProfileModelForm(forms.ModelForm):
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
            "style":" background:transparent",
            "id":"fullname",
            "type":"text",
            "name":"fullname",
            "placeholder":"What about today?",
            
            
            
        })
    class Meta:
        model = Comment
        fields =('body',)