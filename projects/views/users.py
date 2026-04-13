from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from projects.models import User
from projects.serializers import UserListSerializer


class UserListApiView(APIView):
    def get(self, request: Request):
        all_users = User.objects.all()
        project_name = request.query_params.get('project_name')
        if project_name:
            all_users = all_users.filter(project__name=project_name)
        serializer = UserListSerializer(all_users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



