from django.contrib import admin
from django.urls import path

from projects.views.projects import get_all_projects
from projects.views.tasks import get_all_tasks

urlpatterns = [
    path('admin/', admin.site.urls),
    path('projects/', get_all_projects),
    path('tasks/', get_all_tasks),
]
