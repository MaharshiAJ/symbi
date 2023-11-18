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


class Connection(models.Model):
    class ConnectionStatus(models.IntegerChoices):
        NOT_CONNECTED = 1, _("Not Connected")
        REQUESTED = 2, _("Requested")
        CONNECTED = 3, _("Connected")
        BLOCKED = 4, _("Blocked")

    requester = models.ForeignKey(
        SymbiUser, on_delete=models.CASCADE, related_name="requester"
    )
    receiver = models.ForeignKey(
        SymbiUser, on_delete=models.CASCADE, related_name="receiver"
    )
    status = models.IntegerField(
        choices=ConnectionStatus.choices, default=ConnectionStatus.NOT_CONNECTED
    )
    date_connected = models.DateTimeField("date_connected", auto_now_add=True)

    class Meta:
        unique_together = ["requester", "receiver"]

    # Check if two users are connected
    @classmethod
    def are_connected(cls, user1, user2):
        return cls.objects.filter(
            (models.Q(requester=user1) & models.Q(receiver=user2))
            | (models.Q(requester=user2) & models.Q(receiver=user1))
        ).exists()

    # Get all connection objects regardless of who is requester and receiver
    @classmethod
    def get_connection(cls, user1, user2):
        return cls.objects.filter(
            (models.Q(requester=user1) & models.Q(receiver=user2))
            | (models.Q(requester=user2) & models.Q(receiver=user1))
        ).first()

    # Get all connections where the user was the receiver
    @classmethod
    def get_pending_connections(cls, user):
        return (
            cls.objects.filter(receiver=user)
            .filter(status=Connection.ConnectionStatus.REQUESTED)
            .all()
        )

    # Get all active connections for a user
    @classmethod
    def get_active_connections(cls, user):
        return cls.objects.filter(
            (models.Q(requester=user) | models.Q(receiver=user))
            & models.Q(status=Connection.ConnectionStatus.CONNECTED)
        ).all()

    def __str__(self):
        return f"{self.requester} - {self.receiver}"
