from rest_framework import serializers
from core.models import TrainingFragment, RequestFragment


class TaggableManagerField(serializers.Field):

    def to_representation(self, obj):
        ret = []
        ret = obj.names()
        return ret


class UserField(serializers.Field):

    def to_representation(self, obj):
        ret = {'id': obj.id, 'name': obj.username}
        return ret


class TrainingFragmentSerializer(serializers.ModelSerializer):

    tags = TaggableManagerField()
    contributor = UserField()

    class Meta:
        model = TrainingFragment
        fields = ('id', 'label', 'text', 'tags', 'contributor')


class RequestFragmentSerializer(serializers.ModelSerializer):

    tags = TaggableManagerField()
    sender = UserField()

    class Meta:
        model = RequestFragment
        fields = ('id', 'label', 'text', 'tags', 'sender')
