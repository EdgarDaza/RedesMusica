from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('favorites/', views.favorites, name='favorites'),
    path('playlists/', views.playlists_view, name='playlists'),
    path('profile/', views.profile_view, name='profile'),
    path('api/deezer/', views.deezer_search, name='deezer_api'),
    path('update_profile/', views.update_profile, name='update_profile'),

]
