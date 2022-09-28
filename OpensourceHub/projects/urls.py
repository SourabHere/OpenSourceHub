from django.urls import path, include
from . import views

urlpatterns = [

    path('', views.projects , name="projects"),
    path('project/<str:pk>/', views.project , name="project"),
    path('createProject/', views.createProject , name="createproject"),
    
    path('updateprojects/<str:pk>/',views.updateProject,name="updateproject"),
    path('deleteproject/<str:pk>/',views.deleteProjects,name="deleteproject"),
]