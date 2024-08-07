# myapp/views.py
from rest_framework import viewsets
from .models import SymbolPerformance, TopLoser, TopGainer
from .serializers import SymbolPerformanceSerializer, TopLoserSerializer, TopGainerSerializer

class SymbolPerformanceViewSet(viewsets.ModelViewSet):
    queryset = SymbolPerformance.objects.all()
    serializer_class = SymbolPerformanceSerializer

class TopLoserViewSet(viewsets.ModelViewSet):
    queryset = TopLoser.objects.all()
    serializer_class = TopLoserSerializer

class TopGainerViewSet(viewsets.ModelViewSet):
    queryset = TopGainer.objects.all()
    serializer_class = TopGainerSerializer


# myapp/views.py
from django.shortcuts import render

def index(request):
    return render(request, 'index.html')


# myapp/views.py
from django.http import HttpResponse

def home(request):
    return HttpResponse("Welcome to the Stock Market Data Dashboard")
