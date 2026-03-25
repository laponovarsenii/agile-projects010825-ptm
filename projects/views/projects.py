from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from projects.models import Project
from projects.serializers import ProjectListSerializer


@api_view(['GET'])
def get_all_projects(request: Request) -> Response:
    queryset = Project.objects.all()

    if not queryset.exists():
        return Response(
            [],
            status=status.HTTP_200_OK,
        )
    serialized_data = ProjectListSerializer(
        queryset, many=True
    )

    return Response(
        data=serialized_data.data,
        status=status.HTTP_200_OK
    )
