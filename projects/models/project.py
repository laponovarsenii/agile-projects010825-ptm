from django.db import models


class Project(models.Model):
    name = models.CharField(max_length=20)
    description = models.TextField()
    created_at = models.DateField(
        auto_now_add=True
    )


