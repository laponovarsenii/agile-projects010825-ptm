# from django.urls import path
from rest_framework.routers import DefaultRouter
from projects.views.projects import ProjectViewSet


# urlpatterns = [
#     path('', ProjectsListAPIView.as_view()),
#     path('<int:pk>/', ProjectDetailAPIView.as_view()),
# ]

router = DefaultRouter()
router.register('',ProjectViewSet, basename='projects')

urlpatterns = []
urlpatterns += router.urls
