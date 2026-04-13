from rest_framework.routers import DefaultRouter
from projects.views.user import UserViewSet

router = DefaultRouter()
router.register('', UserViewSet, basename='users')

urlpatterns = []

urlpatterns += router.urls
