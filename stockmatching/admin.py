from django.contrib import admin

from .models import Stock, StockMatch
# Register your models here.

admin.register(Stock)
admin.register(StockMatch)