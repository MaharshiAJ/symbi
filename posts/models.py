from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.urls import reverse_lazy

from symbi.models import InterestTag


class ActivityPost(models.Model):
    class PostStatus(models.IntegerChoices):
        DRAFT = 1, _("Draft")
        PUBLISHED = 2, _("Published")
        ARCHIVED = 3, _("Archived")

    class Meta:
        db_table = "activity_posts"
        verbose_name_plural = "Activity Posts"

    poster = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=1023)
    status = models.IntegerField(default=PostStatus.DRAFT, choices=PostStatus.choices)
    tags = models.ManyToManyField(InterestTag, related_name="activity_tags")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse_lazy(
            "posts:post_details",
            kwargs={
                "poster": self.poster,
                "title": self.title,
            },
        )
