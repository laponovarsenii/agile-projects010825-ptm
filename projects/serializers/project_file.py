"""Задача 2 Сериализаторы файлов
Для работы с файлами нужны два сериализатора: один для вывода (GET), другой для приёма загрузки (POST).
Что нужно реализовать
ProjectFileSerializer — для вывода списка файлов
Поля: id, name, file, created_at

UploadProjectFileSerializer — для приёма загружаемого файла
Наследуется от serializers.Serializer
Единственное поле: FileField тип

Реализовать метод validate_file(self, value):
Если value.name.isascii() возвращает False → ValidationError с сообщением
Если расширение не входит в список допустимых → ValidationError с перечислением расширений
Если размер > 2 МБ → ValidationError
При успешной проверке вернуть value

Реализовать метод create(self, validated_data):
Получить project
Получить файл
Сохранить файл на диск
Создать запись ProjectFile
Добавить файл к проекту
Вернуть созданный объект
"""
from django.db import transaction
from rest_framework import serializers
from projects.models import ProjectFile
from projects.utils.file_helpers import check_extension, check_file_size, ALLOWED_EXTENSIONS, save_file, create_file_path



class ProjectFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectFile
        fields = [ "id", "name", "file", "created_at"]


class UploadProjectFileSerializer(serializers.Serializer):
    file = serializers.FileField()

    def validate_file(self, value):
        if not value.name.isascii():
            raise serializers.ValidationError("Имя файла должно быть в фомате ascii")
        if not check_extension(value, ALLOWED_EXTENSIONS):
            raise serializers.ValidationError(f"Допустимые раcширения {ALLOWED_EXTENSIONS}")
        if not check_file_size(value):
            raise serializers.ValidationError("Размер файла должен быть не больше 2Мб")
        return value


    def create(self, validated_data):
         file = validated_data["file"]
         project = self.context.get("project")
         file_path = create_file_path(project.name, file.name)
         try :
             with transaction.atomic():
                 save_file(file_path, file)
                 project_file = ProjectFile.objects.create(name=file.name, file=file_path)
                 project.files.add(project_file)
         except Exception as e:
            raise ValueError("Не удалось сохранить файл")
         return project_file
