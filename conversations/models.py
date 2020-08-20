from django.db import models
from core import models as core_models


class Conversation(core_models.TimeStampedModel):

    """ Conversation Model Definition """

    participants = models.ManyToManyField(
        "users.User", related_name="converstation", blank=True
    )

    def __str__(self):
        # 이 함수는 좀더 개량의 여지가 있음.
        usernames = []
        for user in self.participants.all():
            usernames.append(user.username)
            # string을 만들어주는 join
        return ", ".join(usernames)

    def count_message(self):
        # conversation에는 message라는 property를 가지지 않는다.
        # 하지만 foreign key로 연결되면 다른 class에서 property를 사용할 수 있다.
        return self.messages.count()

    count_message.short_description = "Number of messages"

    def count_participants(self):
        return self.participants.count()

    count_participants.short_description = "Number of participanats"


class Message(core_models.TimeStampedModel):

    """ Message Model Definition """

    # 유저에게 message를 쓸 수 있지만, Conversation에서 하는게 낫다.
    message = models.TextField()
    user = models.ForeignKey(
        "users.User", related_name="messages", on_delete=models.CASCADE
    )
    conversation = models.ForeignKey(
        "Conversation", related_name="messages", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.user} says: {self.message}"

