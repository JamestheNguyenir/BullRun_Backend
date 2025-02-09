from django.contrib import admin

from .models import Stock, StockMatch, UserProfile
# Register your models here.

admin.site.register(UserProfile)
admin.site.register(Stock)
admin.site.register(StockMatch)

