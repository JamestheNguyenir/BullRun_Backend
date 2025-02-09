from .models import UserProfile, Stock
from rest_framework import serializers


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'

class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = '__all__'

