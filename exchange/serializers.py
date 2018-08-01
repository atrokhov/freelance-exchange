from django.contrib.auth.models import User, Group
from .models import Notice, Profile

from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
        class Meta:
                model = User
                fields = ('url', 'username', 'email', 'password', 'groups', 'is_active')

class GroupSerializer(serializers.HyperlinkedModelSerializer):
        class Meta:
                model = Group
                fields = ('url', 'name')

class NoticeSerializer(serializers.HyperlinkedModelSerializer):
        class Meta:
                model = Notice
                fields = ('url', 'author', 'title', 'body', 'pub_date', 'done', 'price', 'executor')

class ProfileSerializer(serializers.HyperlinkedModelSerializer):
        class Meta:
                model = Profile
                fields = ('url', 'user', 'current_balance')
