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
        if not self.pk:  # If it's a new investment
            if self.profile.total_liquidity < self.amount_invested:
                raise ValidationError("Insufficient liquidity to make the investment.")

            # Reduce liquidity and increase total investments
            self.profile.total_liquidity -= self.amount_invested
            self.profile.total_investments += self.amount_invested
            self.profile.save()

        super().save(*args, **kwargs)

