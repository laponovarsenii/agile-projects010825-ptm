from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from projects.models import Task
from projects.serializers.tasks import TaskListSerializer


@api_view(['GET',])
def get_all_tasks(request: Request) -> Response:
    all_tasks = Task.objects.all()

    if not all_tasks.exists():
        return Response(
            data=[],
            status=status.HTTP_200_OK,
        )

    serialized_data = TaskListSerializer(all_tasks, many=True)

    return Response(
        data=serialized_data.data,
        status=status.HTTP_200_OK
    )
