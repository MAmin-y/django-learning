from django.urls import path
from . import views

urlpatterns = [
    path('', views.projects, name = "projects"),
    path('single_project/<str:argum>/', views.single_project, name = "single_project"),
    path('create_project/', views.create_project, name = "create_project"),
    path('update_project/<str:argum>/', views.update_project, name = "update_project"),
    path('delete_project/<str:argum>/', views.delete_project, name = "delete_project"),
]