from django.shortcuts import render, get_object_or_404
from .models import Team, Match, Player
from django.utils import timezone
from django.db.models import Q, Case, When, IntegerField

def get_table_data(league_code):
    teams = Team.objects.filter(league=league_code)
    table = []
    for team in teams:
        # Tady jsem sjednotil názvy (goals_scored, goals_conceded), aby seděly na HTML
        stats = {
            'team': team, 
            'played': 0, 
            'points': 0, 
            'goals_scored': 0, 
            'goals_conceded': 0
        }
        team_matches = Match.objects.filter(Q(home_team=team) | Q(away_team=team)).filter(status='FIN')
        
        for m in team_matches:
            stats['played'] += 1
            if m.home_team == team:
                stats['goals_scored'] += m.home_score
                stats['goals_conceded'] += m.away_score
                if m.home_score > m.away_score: stats['points'] += 3
                elif m.home_score == m.away_score: stats['points'] += 1
            else:
                stats['goals_scored'] += m.away_score
                stats['goals_conceded'] += m.home_score
                if m.away_score > m.home_score: stats['points'] += 3
                elif m.away_score == m.home_score: stats['points'] += 1
        table.append(stats)
    
    # Seřadíme podle bodů, pak podle rozdílu skóre
    return sorted(table, key=lambda x: x['points'], reverse=True)

def home(request):
    matches = Match.objects.all().order_by('start_time')
    return render(request, 'index.html', {'zapasy': matches})

def league_view(request, league_code):
    # Tady se generují data
    data = get_table_data(league_code.upper())
    league_name = "Chance Liga" if league_code.upper() == 'CHANCE' else league_code.upper()
    
    # POZOR: vracíme 'table_data', aby to sedělo na HTML kód
    return render(request, 'league_table.html', {
        'table_data': data, 
        'league_name': league_name
    })

from django.shortcuts import render, get_object_or_404
from .models import Team, Match, Player
from django.db.models import Q

def team_detail(request, team_id):
    team = get_object_or_404(Team, pk=team_id)
    
    # Definujeme pořadí pozic
    players = team.players.all().annotate(
        position_order=Case(
            When(position='GK', then=1),
            When(position='DF', then=2),
            When(position='MD', then=3),
            When(position='FW', then=4),
            output_field=IntegerField(),
        )
    ).order_by('position_order', 'number') # Nejdřív podle pozice, pak podle čísla dresu
    
    # Zápasy zůstávají stejné
    past_matches = Match.objects.filter(
        Q(home_team=team) | Q(away_team=team),
        status='FIN'
    ).order_by('-start_time')[:5]
    
    return render(request, 'team_detail.html', {
        'team': team, 
        'players': players, 
        'past_matches': past_matches
    })