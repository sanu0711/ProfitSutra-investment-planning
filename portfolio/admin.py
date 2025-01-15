from django.contrib import admin
from .models import Portfolio, UserStock, recommStock
# Register your models here.

admin.site.register(Portfolio)
admin.site.register(recommStock)
admin.site.register(UserStock)
