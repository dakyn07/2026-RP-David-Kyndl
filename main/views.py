from django.shortcuts import render, get_object_or_404
from .models import Team, Match, Player
from django.utils import timezone
from django.db.models import Q, Case, When, IntegerField

# Pomocná funkce s dynamickým bodováním
def get_table_data(league_code, division_code=None):
    # Pro NHL (v jakékoliv velikosti písmen) nastavíme 2 body, pro ostatní 3
    win_points = 2 if league_code.upper() == 'NHL' else 3
    
    teams = Team.objects.filter(league=league_code)
    
    if division_code:
        teams = teams.filter(division=division_code)
        
    table = []
    for team in teams:
        stats = {
            'team': team, 
            'played': 0, 
            'points': 0, 
            'goals_scored': 0, 
            'goals_conceded': 0
        }
        # Hledáme pouze ukončené zápasy daného týmu
        team_matches = Match.objects.filter(Q(home_team=team) | Q(away_team=team)).filter(status='FIN')
        
        for m in team_matches:
            stats['played'] += 1
            if m.home_team == team:
                stats['goals_scored'] += m.home_score
                stats['goals_conceded'] += m.away_score
                # Výhra domácích
                if m.home_score > m.away_score: 
                    stats['points'] += win_points
                # Remíza (v NHL bod pro oba)
                elif m.home_score == m.away_score: 
                    stats['points'] += 1
            else:
                stats['goals_scored'] += m.away_score
                stats['goals_conceded'] += m.home_score
                # Výhra hostů
                if m.away_score > m.home_score: 
                    stats['points'] += win_points
                # Remíza
                elif m.away_score == m.home_score: 
                    stats['points'] += 1
        table.append(stats)
    
    # Seřazení podle bodů a následně podle rozdílu skóre (běžné v tabulkách)
    return sorted(table, key=lambda x: (x['points'], x['goals_scored'] - x['goals_conceded']), reverse=True)

def home(request):
    matches = Match.objects.all().order_by('start_time')
    return render(request, 'index.html', {'zapasy': matches})

def league_view(request, league_code):
    l_code = league_code.upper()
    league_name = "Chance Liga" if l_code == 'CHANCE' else l_code
    
    context = {
        'league_name': league_name,
        'is_nhl': (l_code == 'NHL'),
    }

    if l_code == 'NHL':
        context['divisions'] = {
            'Metropolitní': get_table_data('NHL', 'MET'),
            'Atlantická': get_table_data('NHL', 'ATL'),
            'Centrální': get_table_data('NHL', 'CEN'),
            'Pacifická': get_table_data('NHL', 'PAC'),
        }
    else:
        context['table_data'] = get_table_data(l_code)
    
    return render(request, 'league_table.html', context)

def team_detail(request, team_id):
    team = get_object_or_404(Team, pk=team_id)
    
    players = team.players.all().annotate(
        position_order=Case(   
            When(position='GK', then=1),
            When(position='DF', then=2),
            When(position='MD', then=3),
            When(position='FW', then=4),
            output_field=IntegerField(),
        )
    ).order_by('position_order', 'number')
    
    past_matches = Match.objects.filter(
        Q(home_team=team) | Q(away_team=team),
        status='FIN'
    ).order_by('-start_time')[:5]
    
    return render(request, 'team_detail.html', {
        'team': team, 
        'players': players, 
        'past_matches': past_matches
    })