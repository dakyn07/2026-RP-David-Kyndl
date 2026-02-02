from django.contrib import admin
from django.urls import path
from main.views import home  # Importujeme tvůj pohled z aplikace main

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'), # Tohle říká: prázdná adresa = funkce home
]