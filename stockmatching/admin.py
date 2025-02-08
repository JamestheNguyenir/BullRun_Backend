from django.contrib import admin

from .models import Stock, StockMatch, StockPrice, UserProfile
# Register your models here.

admin.site.register(UserProfile)
admin.site.register(Stock)
admin.site.register(StockMatch)
admin.site.register(StockPrice)
