from datetime import datetime

from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import action, api_view
from rest_framework.exceptions import NotFound
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.parsers import MultiPartParser

from projects.models import Project
from projects.serializers import (
    CreateProjectSerializer,
    ProjectDetailSerializer,
    ProjectListSerializer,
)
from projects.serializers.project_file import ProjectFileSerializer,UploadProjectFileSerializer

# Задача 3 ViewSet и кастомный экшн
# Вместо отдельных классов нужен единый ProjectViewSet, который управляет и проектами, и их файлами.

# Что нужно реализовать
# ProjectViewSet
# Кастомный экшн files:
# экшн работает с конкретным объектом
# получить объект проекта
# получить объект проекта, создать файл


class ProjectViewSet(ModelViewSet):
    def get_queryset(self):
        queryset = Project.objects.all()

        date_from = self.request.query_params.get("date_from")
        date_to = self.request.query_params.get("date_to")

        if date_from:
            date_from = timezone.make_aware(datetime.strptime(date_from, "%Y-%m-%d"))

            queryset = queryset.filter(created_at__gte=date_from)

        if date_to:
            date_to = (
                timezone.make_aware(datetime.strptime(date_to, "%Y-%m-%d"))
                if date_from
                else timezone.now().strftime("%Y-%m-%d")
            )

            queryset = queryset.filter(created_at__lte=date_to)

        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return ProjectListSerializer
        if self.action in ["create", "update", "partial_update"]:
            return CreateProjectSerializer

        return ProjectDetailSerializer

    @action(detail=True, methods=["get", "post"], parser_classes=[MultiPartParser])
    def files(self, request, *args, **kwargs):
        project = self.get_object()

        if request.method == "GET":
            files = project.files.all()
            serializer = ProjectFileSerializer(files, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        serializer = UploadProjectFileSerializer(data=request.data, context={"project":project})
        
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response({"msg":'File was successfully upload'}, status=status.HTTP_201_CREATED)

class ProjectsListAPIView(APIView):
    def get_objects(self):
        queryset = Project.objects.all()

        date_from = self.request.query_params.get("date_from")
        date_to = self.request.query_params.get("date_to")

        if date_from:
            date_from = timezone.make_aware(datetime.strptime(date_from, "%Y-%m-%d"))

            queryset = queryset.filter(created_at__gte=date_from)

        if date_to:
            date_to = (
                timezone.make_aware(datetime.strptime(date_to, "%Y-%m-%d"))
                if date_from
                else timezone.now().strftime("%Y-%m-%d")
            )

            queryset = queryset.filter(created_at__lte=date_to)

        return queryset

    def get(self, request: Request) -> Response:
        projects = self.get_objects()

        if not projects.exists():
            return Response(data=[], status=status.HTTP_204_NO_CONTENT)

        serializer = ProjectListSerializer(projects, many=True)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )

    def post(self, request: Request) -> Response:
        serializer = CreateProjectSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()

            return Response(
                serializer.validated_data,
                status=status.HTTP_201_CREATED,
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )


class ProjectDetailAPIView(APIView):
    def get_object(self) -> Project:
        pk = self.kwargs["pk"]
        try:
            obj = Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            raise NotFound(f"Tag with {pk} ID not found")
        return obj

    def get(self, request: Request, *args, **kwargs) -> Response:
        project = self.get_object()

        serializer = ProjectDetailSerializer(project)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )

    def put(self, request: Request, *args, **kwargs) -> Response:
        project = self.get_object()

        serializer = CreateProjectSerializer(
            instance=project,
            data=request.data,
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save()

            return Response(
                serializer.validated_data,
                status=status.HTTP_200_OK,
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )

    def delete(self, request: Request, *args, **kwargs) -> Response:
        project = self.get_object()

        project.delete()

        return Response(
            data={"message": "Project was deleted successfully"},
            status=status.HTTP_200_OK,
        )


@api_view(["GET"])
def get_all_projects(request: Request) -> Response:
    queryset = Project.objects.all()

    if not queryset.exists():
        return Response(
            [],
            status=status.HTTP_200_OK,
        )
    serialized_data = ProjectListSerializer(queryset, many=True)

    return Response(data=serialized_data.data, status=status.HTTP_200_OK)
