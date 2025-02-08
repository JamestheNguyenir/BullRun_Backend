from django.db import models
from authentication.models import User
from stockmatching.models import Stock, UserProfile

class Investment(models.Model):
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="investments")
    stock = models.ForeignKey(Stock,on_delete=models.CASCADE)
    amount_invested = models.DecimalField(max_digits=12, decimal_places=2)
    time_bought = models.DateTimeField(auto_now_add=True)
    price_at_purchase = models.DecimalField(max_digits=12, decimal_places=2)  # Price per share at purchase

