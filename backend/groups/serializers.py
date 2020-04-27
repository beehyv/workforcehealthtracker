from rest_framework import serializers

from groups.models import UserGroup


class UserGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserGroup
        fields = ('id','name',)
