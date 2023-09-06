from . import views
from django.urls import path
from blog.views import detail_view
from django.contrib.auth.views import LoginView,LogoutView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.register,name="blog-register"),
    path('login/', views.login_user,name="blog-login"),
    path('my-invites/', views.invites_received_view, name="my-invites-view"),
    path('all-profiles/', views.ProfileListView.as_view(), name="all-profiles-view"),
    path('to-invite/', views.invite_profiles_list_view, name="invite-profiles-view"),
    path('send-invite/', views.send_invatation, name="send-invite"),
    path('remove-friend/', views.remove_from_friends, name="remove-friend"),
    path('my-invites/accept/', views.accept_invatation, name="accept-invite"),
    path('my-invites//reject', views.reject_invatation, name="reject-invite"),
    path('forgot/forget-password/',views.ForgetPassword,name="forget_password"),
    path('change-password/<token>/', views.ChangePassword,name="change_password"),
    path('<slug>/', detail_view, name="profile-detail-view"),
   
]
