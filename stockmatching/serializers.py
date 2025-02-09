from .models import UserProfile, Stock, StockMatch
from rest_framework import serializers


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'

class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = '__all__'

class StockMatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockMatch
        fields = '__all__'
