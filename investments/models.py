from django.db import models
from django.core.exceptions import ValidationError

from authentication.models import User
from stockmatching.models import Stock, UserProfile

class Investment(models.Model):
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="investments")
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    stock_ticker = models.CharField(max_length=10)  # Store ticker separately
    amount_invested = models.DecimalField(max_digits=12, decimal_places=2)
    time_bought = models.DateField()
    price_at_purchase = models.DecimalField(max_digits=12, decimal_places=2)  # Price per share at purchase

    def save(self, *args, **kwargs):
        # Check if the user has enough liquidity before proceeding
        if self.profile.total_liquidity < self.amount_invested:
            raise ValidationError("Insufficient liquidity to make the investment.")
        
        # Proceed with saving the investment
        super().save(*args, **kwargs)

        # Update the liquidity after the investment is saved
        self.profile.total_liquidity -= self.amount_invested
        self.profile.save()