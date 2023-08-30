from . import views 
from django.urls import path
from django.contrib.auth import views as user_view
from .views import PostDetailView, AddPostView,like_unlike_post, PostDeleteView,PostUpdateView
urlpatterns = [
    path('', views.home, name="blog-home"),
    
    path('logout/', user_view.LogoutView.as_view(), name="blog-logout"),
    path('profile/',views.profile,name="profile"),
    path('post/<int:pk>/', views.details ,name='post-detail'),
    # path('home/new/', views.home , name="blog-post"),
    path('liked/', views.like_unlike_post,name='like-post-view' ),
    path('liked_profile/', views.like_unlike_post_profile,name='like-post-view-profile' ),
    path('liked_post/<int:pk>/', views.like_unlike_post_detail,name='like-post-view-post-detail' ),
    path('liked_post_list/<int:pk>/', views.like_unlike_post_list2,name='like-post-view-post-list2' ),
  
    path('<pk>/delete/', PostDeleteView.as_view(), name="post-delete"),
    path('<pk>/update/', PostUpdateView.as_view(), name="post-update"),
    path('search/', views.search_post, name="search"),
]
