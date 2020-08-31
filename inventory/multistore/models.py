from django.db import models
from django.conf import settings
from datetime import datetime



class SKU(models.Model):
    sku_code = models.CharField(max_length=64)

    def __str__(self):
        return f'{self.sku_code}'

class Location(models.Model):
    location_name = models.CharField(max_length=64)

    def __str__(self):
        return f'{self.location_name}'

class Stock(models.Model):

    timestamp = models.DateTimeField(auto_now=True)
    order_no = models.CharField(max_length=64)
    sku = models.ForeignKey(SKU, on_delete=models.DO_NOTHING)
    quantity = models.IntegerField()
    location = models.ForeignKey(Location, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f'{self.timestamp}, {self.order_no}, {self.sku}, {self.quantity}, {self.location}, {self.user}'
