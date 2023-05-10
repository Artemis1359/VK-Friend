from django.db import models
from django.contrib.auth.models import User

STATUS_CHOICES = (
    ('pending', 'Заявка ожидает решения',),
    ('accepted', 'Заявка принята',),
    ('rejected', 'Заявка отклонена',),
)


class FriendRequest(models.Model):
    from_user = models.ForeignKey(
        User,
        related_name='friend_requests_sent',
        on_delete=models.CASCADE
    )
    to_user = models.ForeignKey(
        User,
        related_name='friend_requests_received',
        on_delete=models.CASCADE
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default=STATUS_CHOICES[0][0],
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (('to_user', 'from_user'),)

    def __str__(self):
        f'{self.from_user.username} -> {self.to_user.username} ({self.status})'
