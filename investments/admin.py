from django.contrib import admin

from .models import Investment, UserProfile
# Register your models here.

admin.register(Investment)
admin.register(UserProfile)