from django.db import models
from authentication.models import User


class UserProfile(models.Model):
    class Levels(models.TextChoices):
        High = 'high', 'High'
        Medium = 'medium', 'Medium'
        Low = 'low', 'Low'
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    total_investments = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    total_liquidity = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    risk_factor = models.CharField(max_length=10,choices=Levels.choices)
    created_at = models.DateTimeField(auto_now_add=True)

class Stock(models.Model):
    class Levels(models.TextChoices):
        High = 'high', 'High'
        Medium = 'Medium', 'Medium'
        Low = 'low', 'Low'

    symbol = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to="stock_logos/", null=True, blank=True)
    risk_level = models.CharField(max_length=10, choices=Levels.choices, default=Levels.Low)
    liquidity = models.CharField(max_length=10, choices=Levels.choices, default=Levels.Medium)
    description = models.TextField()


class StockMatch(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    liked = models.BooleanField(default=False)

class StockPrice(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name="historical_prices")
    date = models.DateField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
