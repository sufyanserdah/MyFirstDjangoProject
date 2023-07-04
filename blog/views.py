from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from django.urls import reverse, reverse_lazy
from .models import Post,Like
from users.models import Profile
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from convert_to_queryset import list_to_queryset
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    View,
)
from .forms import ProfileModelForm,PostModelForm,CommentModelForm

@login_required
def like_unlike_post(request):
    user = request.user
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post_obj = Post.objects.get(id = post_id)
        profile = Profile.objects.get(user=user)
        if profile in post_obj.liked.all():
            post_obj.liked.remove(profile)
        else:
            post_obj.liked.add(profile)
        like,created=Like.objects.get_or_create(user=profile,post_id=post_id)
        if not created:
            if like.value=='Like':
                like.value='Unlike'
            else:
                like.value='Like'
            post_obj.save()
            like.save()
        else:
            like.value='Like'
    return redirect('blog-home')        
                
@login_required          
def home(request):
    ordering =['-date_posted']
    profile = Profile.objects.get(user = request.user)
    nopro = Profile.objects.exclude(user = request.user)
    
    a = Profile.objects.all()
    a = set(a)
    
    b = profile.get_friends()
    c = a.difference(b)
    p_form = PostModelForm()
    c_form = CommentModelForm( )
    post_added=False
    if 'submit_p_form' in request.POST:
        print(request.POST)
            
        p_form = PostModelForm(request.POST, request.FILES )

        if p_form.is_valid():
            instance = p_form.save(commit=False)
            instance.author = profile
            instance.save()
            p_form=PostModelForm()
            post_added = True
    if 'submit_c_form' in request.POST:

        c_form = CommentModelForm(request.POST )

        if c_form.is_valid():
            instance = c_form.save(commit=False)
            instance.user = profile
            instance.post = Post.objects.get(id=request.POST.get('post_id'))
            instance.save()
            c_form = CommentModelForm()   
    context = {
        'posts':Post.objects.all().order_by('-date_posted'),
        'user': request.user,
        'pos': profile.get_posts_no,
        'im': Profile.objects.filter(user= request.user),
        'profile':profile,
        'friends': profile.get_friends(),
        'nofriend': c,
        'p_form':p_form,
        'c_form':c_form,
        'post_added':post_added,
    }
    return render(request, 'blog/home.html', context)
@login_required
def profile(request):
    profile = Profile.objects.get(user = request.user)
    form = ProfileModelForm(request.POST or None, request.FILES or None, instance=profile)
    confirm = False
    p_form = PostModelForm()
    c_form = CommentModelForm( )
    post_added=False
    if 'submit_p_form' in request.POST:
        print(request.POST)
            
        p_form = PostModelForm(request.POST, request.FILES )

        if p_form.is_valid():
            instance = p_form.save(commit=False)
            instance.author = profile
            instance.save()
            p_form=PostModelForm()
            post_added = True
    if 'submit_c_form' in request.POST:

        c_form = CommentModelForm(request.POST )

        if c_form.is_valid():
            instance = c_form.save(commit=False)
            instance.user = profile
            instance.post = Post.objects.get(id=request.POST.get('post_id'))
            instance.save()
            c_form = CommentModelForm()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            confirm = True
    context ={
        'profile':profile,
        'form':form,
        'confirm':confirm,
                'friends': profile.get_friends(),
        
        'p_form':p_form,
        'c_form':c_form,
        'post_added':post_added,
    }
    
    return render(request, 'blog/profile.html',context)

class AddPostView(CreateView, LoginRequiredMixin, UserPassesTestMixin):
    model = Post
    template_name = 'blog/home.html'
    fields= ['content']
    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    def get_success_url(self):
        return reverse('blog-home' )
    
    
    
class PostDetailView(DetailView,LoginRequiredMixin):
    model = Post
    
class AddPostView(CreateView, LoginRequiredMixin, UserPassesTestMixin):
    model = Post
    template_name = 'blog/home.html'
    fields= ['content']
    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    
class PostDeleteView(DeleteView, LoginRequiredMixin):
    model = Post
    template_name='blog/confirm_del.html'
    success_url = reverse_lazy('blog-home')
    def get_object(self,*args,**kwargs):
        pk = self.kwargs.get('pk')
        obj = Post.objects.get(pk=pk)
        if not obj.author.user == self.request.user:
            messages.warning(self.request, 'you must be the author of this post in order to delete')
        return obj
class PostUpdateView(LoginRequiredMixin, UpdateView):
    form_class = PostModelForm
    model = Post
    template_name = 'blog/update.html'
    success_url = ''

    def form_valid(self, form):
        profile = Profile.objects.get(user=self.request.user)
        if form.instance.author == profile:
            return super().form_valid(form)
        else:
            form.add_error(None, "You need to be the author of the post in order to update it")
            return super().form_invalid(form)