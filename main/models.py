from django.db import models

class Team(models.Model):
    name = models.CharField(max_length=100)
    logo_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name

class Match(models.Model):
    STATUS_CHOICES = [
        ('PRE', 'Neproběhlo'),
        ('LIVE', 'Živě'),
        ('FIN', 'Ukončeno'),
    ]

    home_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='home_matches')
    away_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='away_matches')
    home_score = models.IntegerField(default=0)
    away_score = models.IntegerField(default=0)
    status = models.CharField(max_length=4, choices=STATUS_CHOICES, default='PRE')
    start_time = models.DateTimeField()

    def __str__(self):
        return f"{self.home_team} vs {self.away_team} ({self.status})"