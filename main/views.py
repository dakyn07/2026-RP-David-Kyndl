from django.shortcuts import render
from .models import Match

def home(request):
    # Vytáhneme všechny zápasy seřazené podle času startu
    matches = Match.objects.all().order_by('start_time')
    
    # Předáme je do šablony pod názvem 'zapasy'
    return render(request, 'index.html', {'zapasy': matches})