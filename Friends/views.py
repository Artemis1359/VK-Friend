from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import FriendRequest
from .serializers import FriendRequestSerializer


class FriendRequestViewSet(viewsets.ModelViewSet):
    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            sender = self.request.user
            receiver = serializer.validated_data['to_user']
            if sender == receiver:
                return Response(
                    {'error': 'You can not send friend request to yourself'})
            elif FriendRequest.objects.filter(
                    from_user=sender,
                    to_user=receiver).exists():
                return Response(
                    {'detail': 'Friend request already exists'})
            serializer.save(from_user=sender,)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['PUT'])
    def accept(self, request, pk):
        friend_request = self.get_object()
        if friend_request.status == 'pending':
            if friend_request.from_user != self.request.user:
                friend_request.status = 'accepted'
                friend_request.save()
                return Response({'detail': 'Friend request accepted', },
                                status=status.HTTP_200_OK)
            return Response({'error': 'You can not accept outcoming requests'})
        return Response({'error': 'Request already done'})

    @action(detail=True, methods=['PUT'])
    def reject(self, request, pk):
        friend_request = self.get_object()
        if friend_request.status == 'pending':
            if friend_request.from_user != self.request.user:
                friend_request.status = 'rejected'
                friend_request.save()
                return Response({'detail': 'Friend request rejected', },
                                status=status.HTTP_200_OK)
            return Response({'error': 'You can not reject outcoming requests'})
        return Response({'error': 'Request already done'})

    def list(self, request):
        incoming_requests = FriendRequest.objects.filter(
            to_user=self.request.user,
            status='pending',
            )
        outcoming_requests = FriendRequest.objects.filter(
            from_user=self.request.user,
            status='pending',
        )
        incoming_serializer = FriendRequestSerializer(
            incoming_requests, many=True)
        outcoming_serializer = FriendRequestSerializer(
            outcoming_requests, many=True)
        return Response({'incoming_requests': incoming_serializer.data,
                         'outcoming_requests': outcoming_serializer.data, })


class FriendListViewset(viewsets.ReadOnlyModelViewSet):
    serializer_class = FriendRequestSerializer

    def get_queryset(self):
        user = self.request.user
        return FriendRequest.objects.filter(
            from_user=user, status='accepted'
            ) | FriendRequest.objects.filter(
            to_user=user, status='accepted'
            )
