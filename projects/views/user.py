from rest_framework import status

from projects.serializers import UserListSerializer, UserDetailSerializer
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from projects.models import User

class UserViewSet(ModelViewSet):
    queryset = User.objects.filter(is_active=True)

    def get_serializer_class(self):
        if self.action == 'list':
            return UserListSerializer
        return UserDetailSerializer

    def destroy(self, request, *args, **kwargs):
        user = self.get_object()
        user.is_active = False
        user.save()
        return Response({'detail': 'User has been deleted'}, status=status.HTTP_200_OK)