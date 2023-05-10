from rest_framework import serializers

from .models import FriendRequest


class FriendRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = FriendRequest
        fields = ('id', 'to_user', 'from_user', 'status', 'created_at',)
        read_only_fields = ('from_user', 'status',)
