from django.urls import path, include

urlpatterns = [
    path('projects/', include('projects.urls.projects')),
    path('tags/', include('projects.urls.tags')),
    path('tasks/', include('projects.urls.tasks')),
    path('users/', include('projects.urls.user')),
]
