from django.db import models
from django.core.validators import MinLengthValidator


# Задание 2 Дмитрий
# Создайте модель Task со следующими полями:
# Название задачи: строковое поле, уникальное, минимальная длина названия - 10 символов
# Описание: большое строковое поле, может быть пустым
# Статус: строковое поле максимальной длины в 15 символов, должно быть полем выбора разных статусов. По умолчанию все задачи новые
# Приоритет: строковое поле максимальной длины в 15 символов, должно быть полем выбора разных приоритетов
# Проект: связь с моделью Project, при удалении проекта все задачи должны удаляться
# Дата создания задачи: поле, поддерживающее и дату, и время, заполняется автоматически только при создании
# Дата обновления: поле, поддерживающее и дату, и время, заполняется автоматически всегдаДата удаления: поле, в котором может ничего не быть


class Task(models.Model):
    
    class Status(models.IntegerChoices):
        new = 1,"New"
        in_progress = 2,"In progress"
        done = 3,"Done"
        cancelled = 4,"Cancelled"
    
    class Priority(models.IntegerChoices):
        low = 1,"Low"
        medium = 2,"Medium"
        high = 3,"High"
        crirtical = 4,"Critical"
        
    
    name = models.CharField(
        max_length=100,
        unique=True,
        validators=[MinLengthValidator(10)],
        verbose_name="Название задачи"
    ),
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Описание"
    )
    status = models.PositiveSmallIntegerField(
        choices=Status,
        default=Status.new,
        verbose_name="Статус"
    ),
    priority = models.PositiveSmallIntegerField(
        choices=Priority,
        verbose_name="Приоритет"
    ),
    project = models.ForeignKey(
        "Project",
        related_name="tasks", 
        on_delete=models.CASCADE, 
        verbose_name="Проект"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    ),
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата обновления"
    ),
    deleted_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name="Дата удаления"
    )
    due_date = models.DateTimeField(
        blank=True,
        null=True,
    )