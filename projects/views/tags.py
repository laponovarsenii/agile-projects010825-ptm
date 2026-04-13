from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from projects.models import Tag
from projects.serializers import TagSerializer



class TagListCreateAPIView(APIView):
    def get(self, request: Request) -> Response:
        all_tags = Tag.objects.all()
        list_tags = TagSerializer(all_tags, many=True)
        return Response(list_tags.data, status=status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        create_tag = TagSerializer(data=request.data)
        if create_tag.is_valid():
            create_tag.save()
            return Response(create_tag.data, status=status.HTTP_201_CREATED)
        return Response(create_tag.errors, status=status.HTTP_400_BAD_REQUEST)



class TagRetrieveUpdateDestroyApiView(APIView):
    def get_object(self, pk: int) -> Tag:
        try:
            tag = Tag.objects.get(pk=pk)
        except Tag.DoesNotExist:
            raise NotFound(f"Tag by ID - {pk} not found")
        return tag

    def get(self, request, pk):
        tag = self.get_object(pk)
        serializer = TagSerializer(tag)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def put(self, request, pk):
        tag = self.get_object(pk)
        serializer = TagSerializer(instance=tag, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk):
        tag = self.get_object(pk)
        tag.delete()
        return Response(data={}, status=status.HTTP_204_NO_CONTENT)