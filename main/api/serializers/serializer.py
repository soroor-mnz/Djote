from rest_framework import serializers

from Djote.errors import PERMISSION_DENIED
from main.models import Note
from user.api.serializers.serializers import UserReadSerializer


class NoteReadSerializer(serializers.ModelSerializer):
    user = UserReadSerializer()
    title = serializers.CharField()
    content = serializers.CharField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()

    class Meta:
        model = Note
        fields = ['id', 'user', 'title', 'content', 'created_at', 'updated_at']


class NoteWriteSerializer(serializers.ModelSerializer):
    title = serializers.CharField(required=True, allow_null=False, allow_blank=False)
    content = serializers.CharField(required=True, allow_null=False, allow_blank=False)

    class Meta:
        model = Note
        fields = ["title", "content"]

    def to_representation(self, instance):
        return NoteReadSerializer().to_representation(instance)

    def create(self, validated_data):
        validated_data["user"] = self.context.get("request").user
        return super(NoteWriteSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        if instance.user != self.context.get("request").user:
           raise serializers.ValidationError(PERMISSION_DENIED)
        return super(NoteWriteSerializer, self).update(instance, validated_data)
