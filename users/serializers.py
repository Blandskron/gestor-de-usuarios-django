from django.contrib.auth import password_validation
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["grupos"] = list(user.groups.values_list("name", flat=True))
        token["permisos"] = sorted(user.get_all_permissions())
        token["username"] = user.username
        return token


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("id", "username", "email", "first_name", "last_name", "password")
        read_only_fields = ("id",)

    def validate_password(self, value):
        # Al crear aún no existe una instancia; este objeto temporal permite que
        # el validador de similitud compare contraseña, username y email.
        user = User(
            username=self.initial_data.get(
                "username", getattr(self.instance, "username", "")
            ),
            email=self.initial_data.get("email", getattr(self.instance, "email", "")),
            first_name=self.initial_data.get(
                "first_name", getattr(self.instance, "first_name", "")
            ),
            last_name=self.initial_data.get(
                "last_name", getattr(self.instance, "last_name", "")
            ),
        )
        password_validation.validate_password(value, user=user)
        return value

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        if "password" in validated_data:
            password = validated_data.pop("password")
            instance.set_password(password)
        return super().update(instance, validated_data)
