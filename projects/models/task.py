from django.core.validators import MinLengthValidator
from django.db import models
from django.contrib.auth.models import User


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
        critical = 4,"Critical"


    name = models.CharField(
        max_length=100,
        unique=True,
        validators=[MinLengthValidator(10)],
        verbose_name="Название задачи",
        null=True,
        blank=True,
    )

    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Описание"
    )

    status = models.PositiveSmallIntegerField(
        choices=Status,
        default=Status.new,
        verbose_name="Статус"
    )

    priority = models.PositiveSmallIntegerField(
        choices=Priority,
        verbose_name="Приоритет",
        default=Priority.low,
    )

    project = models.ForeignKey(
        "Project",
        related_name="tasks",
        on_delete=models.CASCADE,
        verbose_name="Проект",
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания",
        null=True,
        blank=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата обновления",
        null=True,
        blank=True,
    )

    deleted_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name="Дата удаления"
    )

    due_date = models.DateTimeField(
        blank=True,
        null=True,
    )

    tags = models.ManyToManyField(
        "Tag",
        blank=True,
        related_name="tasks"
    )
    assignee = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='assignee_tasks',
        blank=True,
        null=True
    )

    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='creator_tasks',
        blank=True,
        null=True
    )
