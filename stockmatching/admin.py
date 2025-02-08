from django.contrib import admin

from .models import Stock, StockMatch, StockPrice, UserProfile
# Register your models here.

admin.register(UserProfile)
admin.register(Stock)
admin.register(StockMatch)
admin.register(StockPrice)
