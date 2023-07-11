from typing import Any, Dict
import uuid
from django.db.models.query import QuerySet
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import get_user_model
from blog.forms import CommentModelForm, PostModelForm, ProfileModelForm
from users.models import Profile, ProfileManager, Relationship
from .helpers import send_forget_password_mail
from .forms import RegisterForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.views import PasswordChangeView
from .validators import *
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    View,
)
from django.db.models import Q
from blog.models import Post,User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
def logout_required(function=None, logout_url=settings.LOGOUT_URL):
    actual_decorator = user_passes_test(
        lambda u: not u.is_authenticated,
        login_url=logout_url
    )
    if function:
        return actual_decorator(function)
    return actual_decorator
@logout_required
def register(request):
    
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")
            form.save()
            messages.success(request,f'Account created for {username} ')
            return redirect('blog-login')
        else:
            messages.error(request,f'Account failed to create')
    else:
        
        form = RegisterForm()
    context={
        "form":form
        
    }    
    return render(request,'users/register.html',context)

@logout_required
def login_user(request):
    
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        
        try:
            user = authenticate(request, username=User.objects.get(email = username), password = password)
        except:
            user = None
            
        
        if user is not None:
            login(request,user)
            return redirect('blog-home')
        else:
            
            try:
                user = User.objects.get(username=User.objects.get(email = username))
            except User.DoesNotExist:
                messages.warning(request,"Invalid Login, Email does not exist")
            
            else:
                try:
                    user =  User.objects.get(password=password)
                except:
                    messages.warning(request,"Wrong password")

            
                # messages.warning(request,"Invalid Login, please check your username and password")
            
            return redirect('blog-login')

    else:

        return render(request,'users/login.html')

@login_required
def accept_invatation(request):
    if request.method=="POST":
        pk = request.POST.get('profile_pk')
        sender = Profile.objects.get(pk=pk)
        receiver = Profile.objects.get(user=request.user)
        rel = get_object_or_404(Relationship, sender=sender, receiver=receiver)
        if rel.status == 'send':
            rel.status = 'accepted'
            rel.save()
    return redirect('my-invites-view')


        



def ForgetPassword(request):
    print('hello')
    try:
        if request.method == 'POST':
            username = request.POST.get('username')
            
            if not User.objects.filter(username=username).first():
                messages.success(request, 'Not user found with this username.')
                return redirect('forget_password')
            
            user_obj = User.objects.get(username = username)
            token = str(uuid.uuid4())
            print(token)
            profile_obj= Profile.objects.get(user = user_obj)
            profile_obj.forget_password_token = token
            profile_obj.save()
            print({user_obj.email})
            send_forget_password_mail(user_obj.email , token)
            
            messages.success(request, 'An email is sent.')
            return redirect('forget_password')
                
    
    
    except Exception as e:
        print(e)
    return render(request , 'users/forget-password.html')



def ChangePassword(request , token):
    context = {}
    
    
    try:
        profile_obj = Profile.objects.filter(forget_password_token = token).first()
        context = {'user_id' : profile_obj.user.id}
        
        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('reconfirm_password')
            user_id = request.POST.get('user_id')
            
            if user_id is  None:
                messages.success(request, 'No user id found.')
                return redirect(f'/change-password/{token}/')
                
            
            if  new_password != confirm_password:
                messages.success(request, 'both should  be equal.')
                return redirect(f'/change-password/{token}/')
                         
    
            user_obj = User.objects.get(id = user_id)
            if LengthValidator().validate(new_password):
                messages.warning(request, "The password must contain at least 9 charachters: ")
                return redirect(f'/change-password/{token}/')
            if UppercaseValidator().validate(new_password):
                messages.warning(request, 'The password must contain at least 1 uppercase letter, A-Z.')
                return redirect(f'/change-password/{token}/')
           
            if  NumberValidator().validate(new_password):
                messages.warning(request, 'The password must contain at least 1 digit, 0-9.')
                return redirect(f'/change-password/{token}/')    
                
            
            if SymbolValidator().validate(new_password):
                messages.warning(request, "The password must contain at least 1 special character: " +
                  "()[]{}|\`~!@#$%^&*_-+=;:'\",<>./?")
                return redirect(f'/change-password/{token}/')
           
            if RepeatedValidator().validate(new_password):
                messages.warning(request, 'The password cannot be the same as previously used passwords.')
                return redirect(f'/change-password/{token}/')
            user_obj.set_password(new_password)
            user_obj.save()
            return redirect('blog-login')
            
            
            
        
        
    except Exception as e:
        print(e)
    
    return render(request , 'users/change-password.html' , context)
class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'users/detail.html'
    
    # context ={
    #     'posts':profile.get_all_authors_posts() ,
    #     'user': request.user,
    #     'im': Profile.objects.filter(user= request.user),
    #     'profile':profile,
    #     'friends': profile.get_friends(),
    #     'p_form':p_form,
    #     'c_form':c_form,
    #     'post_added':post_added,
    #     'pos': profile.get_posts_no,
    #     'profile':profile,
    #     'form':form,
    #     'confirm':confirm,
    #     'friends': profile.get_friends(),
        
    #     'p_form':p_form,
    #     'c_form':c_form,
    #     'post_added':post_added,
    # }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(username__iexact=self.request.user)
        profile = Profile.objects.get(user=user)
        
        rel_r = Relationship.objects.filter(sender=profile)
        rel_s = Relationship.objects.filter(receiver=profile)
        rel_receiver = []
        rel_sender = []
        
        for item in rel_r:
            rel_receiver.append(item.receiver.user)
        for item in rel_s:
            rel_sender.append(item.sender.user)
        context["rel_receiver"] = rel_receiver
        context["rel_sender"] = rel_sender
        context['posts'] = self.get_object().get_all_authors_posts()
        context['len_posts'] = True if len(self.get_object().get_all_authors_posts()) > 0 else False
        context['profile'] = profile
        
        context['user'] = user
        
        return context

@login_required
def reject_invatation(request):
    if request.method=="POST":
        pk = request.POST.get('profile_pk')
        receiver = Profile.objects.get(user=request.user)
        sender = Profile.objects.get(pk=pk)
        rel = get_object_or_404(Relationship, sender=sender, receiver=receiver)
        rel.delete()
    return redirect('my-invites-view')

@login_required
def invites_received_view(request):
    profile = Profile.objects.get(user=request.user)
    qs = Relationship.objects.invatations_received(profile)
    results = list(map(lambda x: x.sender, qs))
    is_empty = False
    if len(results) == 0:
        is_empty = True

    context = {
        'qs': results,
        'is_empty': is_empty,
    }

    return render(request, 'users/my_invites.html', context)

@login_required
def profiles_list_view(request):
    user = request.user
    qs = Profile.objects.get_all_profiles(user)

    context = {'qs': qs}

    return render(request, 'users/profile_list.html', context)

class ProfileListView(ListView):
    model = Profile
    template_name="users/profile_list.html"
    context_object_name = 'qs'
    def get_queryset(self):
        qs = Profile.objects.get_all_profiles(self.request.user)
        return qs
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(username__iexact=self.request.user)
        profile = Profile.objects.get(user=user)
        rel_r = Relationship.objects.filter(sender=profile)
        rel_s = Relationship.objects.filter(receiver=profile)
        rel_receiver = []
        rel_sender = []
        for item in rel_r:
            rel_receiver.append(item.receiver.user)
        for item in rel_s:
            rel_sender.append(item.sender.user)
        context["rel_receiver"] = rel_receiver
        context["rel_sender"] = rel_sender
        context['is_empty'] = False
        if len(self.get_queryset()) == 0:
            context['is_empty'] = True

        return context

@login_required
def invite_profiles_list_view(request):
    user = request.user
    qs = Profile.objects.get_all_profiles_to_invite(user)

    context = {'qs': qs}

    return render(request, 'users/to_invite_list.html', context)

@login_required
def send_invatation(request):
    if request.method=='POST':
        pk = request.POST.get('profile_pk')
        user = request.user
        sender = Profile.objects.get(user=user)
        receiver = Profile.objects.get(pk=pk)

        rel = Relationship.objects.create(sender=sender, receiver=receiver, status='send')

        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('profile')

@login_required
def remove_from_friends(request):
    if request.method=='POST':
        pk = request.POST.get('profile_pk')
        user = request.user
        sender = Profile.objects.get(user=user)
        receiver = Profile.objects.get(pk=pk)

        rel = Relationship.objects.filter(
            (Q(sender=sender) & Q(receiver=receiver)) | (Q(sender=receiver) & Q(receiver=sender))
        )
        rel.delete()
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('profile')
