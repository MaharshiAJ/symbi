from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class InterestTag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = "interest_tags"
        verbose_name_plural = "Interest Tags"

    def __str__(self):
        return self.name.title()


class SymbiUser(AbstractUser):
    class Pronouns(models.IntegerChoices):
        HE = 1, _("He/Him")
        SHE = 2, _("She/Her")
        THEY = 3, _("They/Them")
        OTHER = 4, _("Other/Prefer Not To Say")

    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=50)
    pronouns = models.IntegerField(
        choices=Pronouns.choices,
        default=Pronouns.OTHER,
    )
    date_of_birth = models.DateField()
    major = models.CharField(max_length=100, default="undeclared")
    interests = models.ManyToManyField(InterestTag, related_name="interests")
    profile_picture = models.ImageField(
        upload_to="profile_pics/", null=True, blank=True
    )
    date_joined = models.DateTimeField(auto_now_add=True)

    REQUIRED_FIELDS = [
        "email",
        "full_name",
        "date_of_birth",
    ]
