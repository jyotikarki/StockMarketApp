# myapp/models.py
from django.db import models

class SymbolPerformance(models.Model):
    symbol = models.TextField()
    daily_closing_price = models.FloatField()
    percentage_change_1day = models.FloatField()
    percentage_change_30days = models.FloatField()
    percentage_change_365days = models.FloatField()

class TopLoser(models.Model):
    symbol = models.TextField()
    percentage_change_1day = models.FloatField()

class TopGainer(models.Model):
    symbol = models.TextField()
    percentage_change_1day = models.FloatField()
