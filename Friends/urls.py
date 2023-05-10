from django.urls import path, include
from rest_framework import routers
from .views import FriendListViewset, FriendRequestViewSet

router = routers.DefaultRouter()
router.register(r'friend-requests', FriendRequestViewSet)
router.register(r'friends', FriendListViewset, basename='friends')

urlpatterns = [
    path('api/', include(router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]
