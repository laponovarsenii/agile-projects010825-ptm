from django.db import models


class Tag(models.Model):
    title = models.CharField(unique=True, max_length=50)

    def __str__(self):
        return self.title
