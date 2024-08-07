# myapp/serializers.py
from rest_framework import serializers
from .models import SymbolPerformance, TopLoser, TopGainer

class SymbolPerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SymbolPerformance
        fields = '__all__'

class TopLoserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TopLoser
        fields = '__all__'

class TopGainerSerializer(serializers.ModelSerializer):
    class Meta:
        model = TopGainer
        fields = '__all__'
