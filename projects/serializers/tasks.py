from rest_framework import serializers

from projects.models import Task


class TaskListSerializer(serializers.ModelSerializer):
   class Meta:
       model = Task
       fields = ['id', 'name', 'status', 'priority']
