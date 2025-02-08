from .models import UserProfile, Stock, StockPrice, StockMatch
from rest_framework import serializers


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'

    def validate(self,data):
        if data['total_liquidity'] < 0:
            raise serializers.ValidationError("Liquidity can't be below zero")

class StockPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockPrice
        fields = '__all__'

class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = '__all__'

class StockMatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockMatch
        fields = '__all__'
