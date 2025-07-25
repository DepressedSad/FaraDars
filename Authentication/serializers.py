from rest_framework import serializers

class EmailSerializer(serializers.Serializer):
    email=serializers.EmailField()

class OTPVerifySerializer(serializers.Serializer):
    email=serializers.EmailField()
    code=serializers.CharField(max_length=6)