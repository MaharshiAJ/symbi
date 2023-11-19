from django.db import models
from symbi.models import SymbiUser


class ChatRoom(models.Model):
    creator = models.ForeignKey(
        SymbiUser, on_delete=models.CASCADE, related_name="creator"
    )
    members = models.ManyToManyField(SymbiUser, related_name="members")
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # Return names of all members
        member_names = ", ".join([member.username for member in self.members.all()])
        return member_names

    # Get all chatrooms where members contains user
    @classmethod
    def get_chatrooms(cls, user):
        return cls.objects.filter(members__in=[user])


class Message(models.Model):
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    sender = models.ForeignKey(SymbiUser, on_delete=models.CASCADE)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    @classmethod
    def get_messages(cls, chat_room):
        return cls.objects.filter(chat_room=chat_room).order_by("created")
