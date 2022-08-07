from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginuser, name='login'),
    path('logout/', views.logoutuser, name='logout'),
    path('register/', views.register_user, name='register'),
    path('user_account/', views.user_account, name='user_account'),
    path('edit_account/', views.edit_account, name='edit_account'),
    path('create_skill/', views.create_skill, name='create_skill'),
    path('update_skill/<str:argum>/', views.update_skill, name='update_skill'),
    path('delete_skill/<str:argum>/', views.delete_skill, name='delete_skill'),
    path('', views.profiles, name='profiles'),
    path('user_profile/<str:argum>/', views.user_profile, name='user_profile'),
]