# myapp/admin.py
from django.contrib import admin
from .models import SymbolPerformance, TopLoser, TopGainer

admin.site.register(SymbolPerformance)
admin.site.register(TopLoser)
admin.site.register(TopGainer)