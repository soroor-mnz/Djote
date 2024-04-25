from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from user.models import AuthUser


class UserReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthUser
        fields = ["first_name", "last_name", "username", "email", "is_active"]


class UserWriteSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=AuthUser.objects.all())], required=True, allow_blank=False
    )
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    is_staff = serializers.BooleanField(default=True)
    is_active = serializers.BooleanField(default=True)
    email = serializers.EmailField( required=True, allow_blank=False)

    class Meta:
        model = AuthUser
        fields = [
            "password",
            "username",
            "first_name",
            "last_name",
            "is_staff",
            "is_active",
            "email",
        ]

    def to_representation(self, instance):
        return UserReadSerializer().to_representation(instance)

    def create(self, validated_data):
        user = super(UserWriteSerializer, self).create(validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user
