# myapp/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'symbol_performance', views.SymbolPerformanceViewSet)
router.register(r'top_losers', views.TopLoserViewSet)
router.register(r'top_gainers', views.TopGainerViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
