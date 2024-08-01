# myproject/urls.py
from django.contrib import admin
from django.urls import path, include
from myapp.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('myapp.urls')),
    path('', home, name='home'),  # Add this line
]