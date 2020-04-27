from django.shortcuts import render
from rest_framework import generics, permissions

from groups.models import UserGroup
from groups.serializers import UserGroupSerializer


class UserGroupList(generics.ListAPIView):
    model = UserGroup
    serializer_class = UserGroupSerializer
    pagination_class = None

    def get_queryset(self):
        return UserGroup.objects.all()

class UserGroupListByManager(generics.ListAPIView):

    model = UserGroup
    serializer_class = UserGroupSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = None

    def get_queryset(self):
        user = self.request.user
        return user.usergroup_set.all()
