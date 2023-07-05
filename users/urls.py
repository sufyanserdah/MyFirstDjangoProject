from . import views
from django.urls import path

from django.contrib.auth.views import LoginView,LogoutView

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
    path('<slug>/', views.ProfileDetailView.as_view(), name="profile-detail-view"),
       path('check-username/', views.check_username, name='check-username'),
  

]
htmx_views=[
]
urlpatterns += htmx_views