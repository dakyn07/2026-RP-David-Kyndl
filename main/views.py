from django.shortcuts import render, get_object_or_404
from .models import Team, Match, Player
from django.utils import timezone
from django.db.models import Q

def get_table_data(league_code):
    teams = Team.objects.filter(league=league_code)
    table = []
    for team in teams:
        stats = {'team': team, 'played': 0, 'points': 0, 'goals_for': 0, 'goals_against': 0}
        team_matches = Match.objects.filter(Q(home_team=team) | Q(away_team=team)).filter(status='FIN')
        
        for m in team_matches:
            stats['played'] += 1
            if m.home_team == team:
                stats['goals_for'] += m.home_score
                stats['goals_against'] += m.away_score
                if m.home_score > m.away_score: stats['points'] += 3
                elif m.home_score == m.away_score: stats['points'] += 1
            else:
                stats['goals_for'] += m.away_score
                stats['goals_against'] += m.home_score
                if m.away_score > m.home_score: stats['points'] += 3
                elif m.away_score == m.home_score: stats['points'] += 1
        table.append(stats)
    return sorted(table, key=lambda x: x['points'], reverse=True)

def home(request):
    matches = Match.objects.all().order_by('start_time')
    return render(request, 'index.html', {'zapasy': matches})

def league_view(request, league_code):
    table = get_table_data(league_code.upper())
    league_name = "Chance Liga" if league_code.upper() == 'CHANCE' else "NHL"
    return render(request, 'league_table.html', {'table': table, 'league_name': league_name})

def team_detail(request, team_id):
    team = get_object_or_404(Team, pk=team_id)
    players = team.players.all().order_by('number')
    all_matches = Match.objects.filter(Q(home_team=team) | Q(away_team=team)).order_by('-start_time')
    return render(request, 'team_detail.html', {'team': team, 'players': players, 'matches': all_matches})