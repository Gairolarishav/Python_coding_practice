from django.db import models

class PublishedManager(models.Manager):
    """Post.published.all() returns only published posts."""

    def get_queryset(self):
        return super().get_queryset().filter(status="published")