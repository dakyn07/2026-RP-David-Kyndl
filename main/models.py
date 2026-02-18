from django.db import models
from django.utils import timezone

class Team(models.Model):
    LEAGUE_CHOICES = [('CHANCE', 'Chance Liga'), ('NHL', 'NHL')]
    DIVISION_CHOICES = [
        ('CZE', 'Česko'), ('ATL', 'Atlantická divize'),
        ('MET', 'Metropolitní divize'), ('CEN', 'Centrální divize'), ('PAC', 'Pacifická divize'),
    ]
    name = models.CharField(max_length=100)
    league = models.CharField(max_length=20, choices=LEAGUE_CHOICES, default='CHANCE')
    division = models.CharField(max_length=5, choices=DIVISION_CHOICES, default='CZE')
    logo_url = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.get_league_display()})"

class Player(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='players')
    name = models.CharField(max_length=100)
    number = models.IntegerField()
    position = models.CharField(max_length=50, choices=[
        ('GK', 'Brankář'), ('DF', 'Obránce'), ('MD', 'Záložník'), ('FW', 'Útočník')
    ])

    def __str__(self):
        return f"{self.number}. {self.name} ({self.team.name})"

class Match(models.Model):
    STATUS_CHOICES = [('PRE', 'Neproběhlo'), ('LIVE', 'Živě'), ('FIN', 'Ukončeno')]
    home_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='home_matches')
    away_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='away_matches')
    home_score = models.IntegerField(default=0)
    away_score = models.IntegerField(default=0)
    status = models.CharField(max_length=4, choices=STATUS_CHOICES, default='PRE')
    start_time = models.DateTimeField()

    def __str__(self):
        return f"{self.home_team.name} vs {self.away_team.name}"

    @property
    def start_time_iso(self):
        """Vrátí plánovaný start v ISO formátu pro JavaScriptové odpočty."""
        return self.start_time.isoformat()

    @property
    def current_minute(self):
        """Vypočítá aktuální minutu zápasu na základě času od start_time."""
        if self.status == 'LIVE':
            now = timezone.now()
            if now > self.start_time:
                diff = now - self.start_time
                curr = int(diff.total_seconds() // 60) + 1
                
                # Definujeme konec podle ligy (NHL/CHANCE = hokej, ostatní = fotbal)
                is_hockey = self.home_team.league in ['NHL', 'CHANCE']
                limit = 60 if is_hockey else 90
                
                # Pokud už jsme přes limit, ale status je stále LIVE (ještě se neuložilo FIN)
                # Zobrazíme raději limit (60 nebo 90), než aby tam skákalo 95'
                return curr if curr <= limit else limit
            return 1
        
        if self.status == 'FIN':
            return "Konec"
            
        return 0
    
class Goal(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='goals')
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    minute = models.PositiveIntegerField(default=0)
    is_penalty = models.BooleanField(default=False)

    class Meta:
        ordering = ['minute']

class Card(models.Model):
    CARD_TYPES = [('Y', 'Žlutá'), ('R', 'Červená')]
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='cards')
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    minute = models.PositiveIntegerField(default=0)
    card_type = models.CharField(max_length=1, choices=CARD_TYPES)

    class Meta:
        ordering = ['minute']

class Penalty(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='penalties')
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    minute = models.PositiveIntegerField(default=0)
    duration = models.IntegerField(default=2)

    class Meta:
        ordering = ['minute']