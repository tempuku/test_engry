from rest_framework import serializers


class AuthKeySerializer(serializers.Serializer):
    auth_key = serializers.CharField(required=True)
