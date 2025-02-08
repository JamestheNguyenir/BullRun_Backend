from .models import UserProfile
from rest_framework import serializers


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'

    def validate(self,data):
        if data['total_liquidity'] < 0:
            raise serializers.ValidationError("Liquidity can't be below zero")
