from rest_framework import serializers


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField(max_length=150)


class ForgetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False, allow_blank=True)
    username = serializers.CharField(required=False, allow_blank=True, max_length=150)


class NewPasswordSerializer(serializers.Serializer):
    otp = serializers.CharField(max_length=6)
    username = serializers.CharField(max_length=150)
    newpassword = serializers.CharField(max_length=16)
