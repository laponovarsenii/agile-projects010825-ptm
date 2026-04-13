from rest_framework import serializers

from projects.models import User


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email")


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        read_only_fields = ("id", "date_joined", "last_login", "is_active")
        exclude = ("password", "is_superuser", "is_staff", "user_permissions", "groups")


