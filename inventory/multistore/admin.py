from django.contrib import admin

# Register your models here.
from .models import Stock, SKU, Location

admin.site.register(Stock)
admin.site.register(SKU)
admin.site.register(Location)