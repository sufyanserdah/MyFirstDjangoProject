from django import http
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from django.urls import reverse, reverse_lazy
from .models import Comment, Post, Like
from users.models import Profile, Relationship
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
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
from .forms import ProfileModelForm, PostModelForm, CommentModelForm
from django.http import HttpResponseRedirect, JsonResponse

@login_required
def home(request):
    ordering = ["-date_posted"]
    profile = Profile.objects.get(user=request.user)
    nopro = Profile.objects.exclude(user=request.user)

    a = Profile.objects.all()

    a = set(a)

    b = set(profile.get_friends2())
    c = a.difference(b)
    p_form = PostModelForm()
    c_form = CommentModelForm()
    post_added = False
    if "submit_p_form" in request.POST:
        print(request.POST)

        p_form = PostModelForm(request.POST, request.FILES)

        if p_form.is_valid():
            instance = p_form.save(commit=False)
            instance.author = profile
            instance.save() 
            p_form = PostModelForm()

            post_added = True
            context = {
        "posts": Post.objects.all().order_by("-date_posted"),
        "user": request.user,
        "pos": profile.get_posts_no,
        "im": Profile.objects.filter(user=request.user),
        "profile": profile,
        "friends": profile.get_friends(),
        "nofriend": c,
        "p_form": p_form,
        "c_form": c_form,
        "post_added": post_added,
    }
            return render(request, "blog/post-list.html",context)

    if "submit_c_form" in request.POST:
        c_form = CommentModelForm(request.POST)

        if c_form.is_valid():
            instance = c_form.save(commit=False)
            instance.user = profile
            instance.post = Post.objects.get(id=request.POST.get("post_id"))
            instance.save()

            c_form = CommentModelForm()
            context = {
        "posts": Post.objects.all().order_by("-date_posted"),
        "user": request.user,
        "pos": profile.get_posts_no,
        "im": Profile.objects.filter(user=request.user),
        "profile": profile,
        "friends": profile.get_friends(),
        "nofriend": c,
        "p_form": p_form,
        "c_form": c_form,
        "post_added": post_added,
    }
            return render(request, "blog/post-list.html",context)
    context = {
        "posts": Post.objects.all().order_by("-date_posted"),
        "user": request.user,
        "pos": profile.get_posts_no,
        "im": Profile.objects.filter(user=request.user),
        "profile": profile,
        "friends": profile.get_friends(),
        "nofriend": c,
        "p_form": p_form,
        "c_form": c_form,
        "post_added": post_added,
    }
    return render(request, "blog/home.html", context)


@login_required
def profile(request):
    print(request.path)
    profile = Profile.objects.get(user=request.user)
    form = ProfileModelForm(
        request.POST or None, request.FILES or None, instance=profile
    )

    confirm = False

    c_form = CommentModelForm()
    post_added = False
   
            
    if "submit_c_form" in request.POST:
        c_form = CommentModelForm(request.POST)

        if c_form.is_valid():
            instance = c_form.save(commit=False)
            instance.user = profile
            instance.post = Post.objects.get(id=request.POST.get("post_id"))
            instance.save()
            c_form = CommentModelForm()
            context = {
        "posts": profile.get_all_authors_posts(),
        "user": request.user,
        "im": Profile.objects.filter(user=request.user),
        "profile": profile,
        "friends": profile.get_friends(),
        "c_form": c_form,
        "post_added": post_added,
        "pos": profile.get_posts_no,
        "post":Post.objects.get(id=request.POST.get("post_id")),
        "form": form,
        "confirm": confirm,
        
        
        
        
    }
            return render(request, "blog/profile.html",context)



    context = {
        "posts": profile.get_all_authors_posts(),
        "user": request.user,
        "im": Profile.objects.filter(user=request.user),
        "profile": profile,
        "friends": profile.get_friends(),
        "c_form": c_form,
        "post_added": post_added,
        "pos": profile.get_posts_no,
        
        "form": form,
        "confirm": confirm,
        
        
        
        
    }

    return render(request, "blog/profile.html", context)



def search_post(request):
    print(request.path)
    if request.method == "POST":
        
        searched = request.POST['searched']
        print(searched+"   kf;aklfksal;")
        if(searched==''):
            return render(request, "blog/search-results.html")
        else:
            posts= Post.objects.filter(content__icontains=searched)
            users = User.objects.filter(username__icontains=searched )
        
            
        for post in posts:
            print(post.content)

    
        context = {"posts": posts ,"searched":searched, 'users':users}
        return render(request, "blog/search-results.html", context)
    
    return render(request, "blog/search-results.html")


class AddPostView(CreateView, LoginRequiredMixin, UserPassesTestMixin):
    model = Post
    template_name = "blog/home.html"
    fields = ["content"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("blog-home")


class PostDetailView(DetailView, LoginRequiredMixin):
    model = Post


@login_required
def details(request, pk):
    
    ordering = ["-date_posted"]
    post = Post.objects.filter(pk=pk)
    profile = Profile.objects.get(user=request.user)
    nopro = Profile.objects.exclude(user=request.user)
    print(pk)
    print(post)
    
    
    c_form = CommentModelForm()
    post_added = False

    if "submit_c_form" in request.POST:
        c_form = CommentModelForm(request.POST)

        if c_form.is_valid():
            instance = c_form.save(commit=False)
            instance.user = profile
            instance.post = Post.objects.get(id=pk)
            instance.save()

            c_form = CommentModelForm()
    context = {
        "user": request.user,
        "pos": profile.get_posts_no,
        "profile": profile,

        "c_form": c_form,
        "post_added": post_added,
        
        "post": post.get ,
        
    }
    return render(request, "blog/post_detail.html", context)


class AddPostView(CreateView, LoginRequiredMixin, UserPassesTestMixin):
    model = Post
    template_name = "blog/home.html"
    fields = ["content"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostDeleteView(DeleteView, LoginRequiredMixin):
    model = Post
    template_name = "blog/confirm_del.html"
    success_url = reverse_lazy("profile")

    def get_object(self, *args, **kwargs):
        pk = self.kwargs.get("pk")
        obj = Post.objects.get(pk=pk)
        if not obj.author.user == self.request.user:
            messages.warning(
                self.request, "you must be the author of this post in order to delete"
            )
        return obj


class PostUpdateView(LoginRequiredMixin, UpdateView):
    form_class = PostModelForm
    model = Post
    template_name = "blog/update.html"
    success_url = ""

    def form_valid(self, form):
        profile = Profile.objects.get(user=self.request.user)
        if form.instance.author == profile:
            return super().form_valid(form)
        else:
            form.add_error(
                None, "You need to be the author of the post in order to update it"
            )
            return super().form_invalid(form)


@login_required
def like_unlike_post(request):
    user = request.user
    ordering = ["-date_posted"]
    profile = Profile.objects.get(user=request.user)
    nopro = Profile.objects.exclude(user=request.user)    
    p_form = PostModelForm()
    c_form = CommentModelForm()
    post_added = False
    a = Profile.objects.all()

    a = set(a)

    b = set(profile.get_friends2())
    c = a.difference(b)
    print(type(a))
    print(type(b))
    print(type(c))
    print(a)
    print(b)
    print( bool(c) )
    context = {
        "posts": Post.objects.all().order_by("-date_posted"),
        "user": request.user,
        "pos": profile.get_posts_no,
        "im": Profile.objects.filter(user=request.user),
        "profile": profile,
        "friends": profile.get_friends(),
        "nofriend": c,
        "p_form": p_form,
        "c_form": c_form,
        "post_added": post_added,
    }
    if request.method == "POST":
        post_id = request.POST.get("post_id")
        post_obj = Post.objects.get(id=post_id)
        profile = Profile.objects.get(user=user)
        if profile in post_obj.liked.all():
            post_obj.liked.remove(profile)
        else:
            post_obj.liked.add(profile)
        like, created = Like.objects.get_or_create(user=profile, post_id=post_id)
        if not created:
            if like.value == "Like":
                like.value = "Unlike"
            else:
                like.value = "Like"
            post_obj.save()
            like.save()
        else:
            like.value = "Like"

        return render(request, "blog/post-list.html",context)



@login_required
def like_unlike_post_profile(request):
    user = request.user
    
    ordering = ["-date_posted"]
    profile = Profile.objects.get(user=request.user)
    nopro = Profile.objects.exclude(user=request.user)    
    p_form = PostModelForm()
    c_form = CommentModelForm()
    post_added = False
    a = Profile.objects.all()

    a = set(a)

    b = set(profile.get_friends2())
    c = a.difference(b)
    print(type(a))
    print(type(b))
    print(type(c))
    print(a)
    print(b)
    print( bool(c) )
    form = ProfileModelForm(
        request.POST or None, request.FILES or None, instance=profile
    )
    confirm = False

    context = {
        "posts": profile.get_all_authors_posts(),
        "user": request.user,
        "im": Profile.objects.filter(user=request.user),
        "profile": profile,
        "friends": profile.get_friends(),
        "p_form": p_form,
        "c_form": c_form,
        "post_added": post_added,
        "pos": profile.get_posts_no,
        
        "form": form,
        "confirm": confirm,
    }
    if request.method == "POST":
        post_id = request.POST.get("post_id")
        post_obj = Post.objects.get(id=post_id)
        profile = Profile.objects.get(user=user)
        if profile in post_obj.liked.all():
            post_obj.liked.remove(profile)
        else:
            post_obj.liked.add(profile)
        like, created = Like.objects.get_or_create(user=profile, post_id=post_id)
        if not created:
            if like.value == "Like":
                like.value = "Unlike"
            else:
                like.value = "Like"
            post_obj.save()
            like.save()
        else:
            like.value = "Like"
        print("dfks;kfdslsd")
        return render(request, "blog/user-post-list.html",context)

@login_required
def like_unlike_post_detail(request, pk):
    user = request.user

    ordering = ["-date_posted"]
    post = Post.objects.filter(pk=pk)
    profile = Profile.objects.get(user=request.user)
    nopro = Profile.objects.exclude(user=request.user)
    print(pk)
    print(post)
    form = ProfileModelForm(
        request.POST or None, request.FILES or None, instance=profile
    )
    confirm = False
    
    c_form = CommentModelForm()
    post_added = False

    if "submit_c_form" in request.POST:
        c_form = CommentModelForm(request.POST)

        if c_form.is_valid():
            instance = c_form.save(commit=False)
            instance.user = profile
            instance.post = Post.objects.get(id=pk)
            instance.save()

            c_form = CommentModelForm()
    context = {
        "user": request.user,
        "pos": profile.get_posts_no,
        "profile": profile,

        "c_form": c_form,
        "post_added": post_added,
        
        "post": post.get ,
        "posts": profile.get_all_authors_posts(),
        "user": request.user,
        "im": Profile.objects.filter(user=request.user),
        "friends": profile.get_friends(),
        "c_form": c_form,
        "post_added": post_added,
        "pos": profile.get_posts_no,
        
        "form": form,
        "confirm": confirm,
        
    }
    if request.method == "POST":
        post_id = request.POST.get("post_id")
        post_obj = Post.objects.get(id=post_id)
        profile = Profile.objects.get(user=user)
        if profile in post_obj.liked.all():
            post_obj.liked.remove(profile)
        else:
            post_obj.liked.add(profile)
        like, created = Like.objects.get_or_create(user=profile, post_id=post_id)
        if not created:
            if like.value == "Like":
                like.value = "Unlike"
            else:
                like.value = "Like"
            post_obj.save()
            like.save()
        else:
            like.value = "Like"
        print("dfks;kfdslsd")
        return render(request, "blog/post_detail_body.html",context)


@login_required
def like_unlike_post_list2(request,pk):
    
    post = Post.objects.filter(pk=pk)
    user1 = post[0].author.user
    ordering = ["-date_posted"]
    profile = Profile.objects.get(user=user1)
    c_form = CommentModelForm()


    form = ProfileModelForm(
        request.POST or None, request.FILES or None, instance=profile
    )
    confirm = False
    user2 = request.user
    profile1 = Profile.objects.get(user=user2)
    context = {
        "posts": profile.get_all_authors_posts(),
        "user": request.user,
        "im": Profile.objects.filter(user=user1),
        "profile": profile,
        "profile1":profile1,
        "friends": profile.get_friends(),
        "c_form": c_form,
        "pos": profile.get_posts_no,
        
        "form": form,
        "confirm": confirm,
    }
    if request.method == "POST":
        post_id = request.POST.get("post_id")
        post_obj = Post.objects.get(id=post_id)
        
        print(profile1)
        if profile1 in post_obj.liked.all():
            post_obj.liked.remove(profile1)
        else:
            post_obj.liked.add(profile1)
        like, created = Like.objects.get_or_create(user=profile1, post_id=post_id)
        if not created:
            if like.value == "Like":
                like.value = "Unlike"
            else:
                like.value = "Like"
            post_obj.save()
            like.save()
        else:
            like.value = "Like"
        print("dfks;kfdslsd")
        print(user1)
        return render(request, "users/post-list2.html",context)


@login_required
def like_unlike_post_search(request, s):
    
    searched = s
    
    posts= Post.objects.filter(content__icontains=searched)
    users = User.objects.filter(username__icontains=searched )
    
    user = request.user
    profile = Profile.objects.get(user=request.user)
    c_form = CommentModelForm()
    post_added = False

    context = {
        "user": request.user,
        "pos": profile.get_posts_no,
        "im": Profile.objects.filter(user=request.user),
        "profile": profile,
        "friends": profile.get_friends(),
        "c_form": c_form,
        "post_added": post_added,
        "posts": posts ,
        "searched":searched, 
        'users':users
    }
    if request.method == "POST":
        post_id = request.POST.get("post_id")
        post_obj = Post.objects.get(id=post_id)
        profile = Profile.objects.get(user=user)
        if profile in post_obj.liked.all():
            post_obj.liked.remove(profile)
        else:
            post_obj.liked.add(profile)
        like, created = Like.objects.get_or_create(user=profile, post_id=post_id)
        if not created:
            if like.value == "Like":
                like.value = "Unlike"
            else:
                like.value = "Like"
            post_obj.save()
            like.save()
        else:
            like.value = "Like"

        return render(request, "blog/post_results.html",context)

