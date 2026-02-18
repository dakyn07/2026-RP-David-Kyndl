from django.shortcuts import render, get_object_or_404
from .models import Team, Match, Player, Goal, Card, Penalty
from django.utils import timezone
from django.db.models import Q, Case, When, IntegerField

def get_table_data(league_code, division_code=None):
    win_points = 2 if league_code.upper() == 'NHL' else 3
    
    teams = Team.objects.filter(league=league_code)
    if division_code:
        teams = teams.filter(division=division_code)
        
    table = []
    for team in teams:
        stats = {'team': team, 'played': 0, 'points': 0, 'goals_scored': 0, 'goals_conceded': 0}
        team_matches = Match.objects.filter(Q(home_team=team) | Q(away_team=team)).filter(status='FIN')
        
        for m in team_matches:
            stats['played'] += 1
            if m.home_team == team:
                stats['goals_scored'] += m.home_score
                stats['goals_conceded'] += m.away_score
                if m.home_score > m.away_score: stats['points'] += win_points
                elif m.home_score == m.away_score: stats['points'] += 1
            else:
                stats['goals_scored'] += m.away_score
                stats['goals_conceded'] += m.home_score
                if m.away_score > m.home_score: stats['points'] += win_points
                elif m.away_score == m.home_score: stats['points'] += 1
        table.append(stats)
    
    return sorted(table, key=lambda x: (x['points'], x['goals_scored'] - x['goals_conceded']), reverse=True)

def home(request):
    now = timezone.now()
    live_matches = Match.objects.filter(status='LIVE').order_by('start_time')
    upcoming = Match.objects.filter(status='PRE', start_time__gte=now).order_by('start_time')
    past = Match.objects.filter(status='FIN').order_by('-start_time').prefetch_related('goals__player')
    
    return render(request, 'index.html', {
        'live_matches': live_matches,
        'upcoming': upcoming, 
        'past': past
    })

def match_detail(request, match_id):
    match = get_object_or_404(
        Match.objects.prefetch_related('goals__player', 'cards__player', 'penalties__player'), 
        pk=match_id
    )
    
    is_nhl = match.home_team.league == 'NHL'
    events = []

    for goal in match.goals.all():
        events.append({'type': 'goal', 'data': goal, 'minute': goal.minute})
    
    if is_nhl:
        for p in match.penalties.all():
            events.append({'type': 'penalty', 'data': p, 'minute': p.minute})
    else:
        for c in match.cards.all():
            events.append({'type': 'card', 'data': c, 'minute': c.minute})
    
    events.sort(key=lambda x: x['minute'])

    last_start_iso = ""
    if match.last_start_time:
        last_start_iso = match.last_start_time.isoformat()
    
    return render(request, 'match_detail.html', {
        'match': match,
        'events': events,
        'is_nhl': is_nhl,
        'current_minute': match.current_minute,
        'last_start_iso': last_start_iso
    })

def league_view(request, league_code):
    l_code = league_code.upper()
    context = {'league_name': "Chance Liga" if l_code == 'CHANCE' else l_code, 'is_nhl': (l_code == 'NHL')}
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
            output_field=IntegerField()
        )
    ).order_by('position_order', 'number')
    past_matches = Match.objects.filter(Q(home_team=team) | Q(away_team=team), status='FIN').order_by('-start_time')[:5]
    return render(request, 'team_detail.html', {'team': team, 'players': players, 'past_matches': past_matches})