from django.core.management.base import BaseCommand
from main.models import Team

class Command(BaseCommand):
    help = 'Naplní DakynScore aktuálními týmy fotbalové Chance Ligy a hokejové NHL 25/26'

    def handle(self, *args, **kwargs):
        # Chance Liga - vše pod divizí 'CZE'
        chance_liga = [
            "AC Sparta Praha", "SK Slavia Praha", "FC Viktoria Plzeň", "FC Baník Ostrava",
            "FK Mladá Boleslav", "FC Slovan Liberec", "SK Sigma Olomouc", "FC Hradec Králové",
            "FK Teplice", "FK Jablonec", "Bohemians Praha 1905", "1.FC Slovácko",
            "MFK Karviná", "FK Pardubice", "FK Dukla Praha", "FC Zlín"
        ]

        # NHL rozdělená podle divizí (zkratky MET, ATL, CEN, PAC)
        nhl_divisions = {
            'ATL': [
            {"name": "Boston Bruins", "logo": "https://cdn.freebiesupply.com/logos/large/2x/boston-bruins-logo.png"},
            {"name": "Florida Panthers", "logo": "https://example.com/panthers_logo.png"},
            {"name": "Montreal Canadiens", "logo": "https://cdn.freebiesupply.com/logos/large/2x/montreal-canadiens-logo.png"},
            {"name": "Ottawa Senators", "logo": "https://example.com/senators_logo.png"},
            {"name": "Tampa Bay Lightning", "logo": "https://example.com/lightning_logo.png"},
            {"name": "Toronto Maple Leafs", "logo": "https://example.com/maple_leafs_logo.png"},
            {"name": "Detroit Red Wings", "logo": "https://example.com/red_wings_logo.png"},
            {"name": "Buffalo Sabres", "logo": "https://example.com/sabres_logo.png"}
            ],
            'MET': [
            {"name": "New York Rangers", "logo": "https://example.com/rangers_logo.png"},
            {"name": "New York Islanders", "logo": "https://example.com/islanders_logo.png"},
            {"name": "New Jersey Devils", "logo": "https://example.com/devils_logo.png"},
            {"name": "Philadelphia Flyers", "logo": "https://example.com/flyers_logo.png"},
            {"name": "Pittsburgh Penguins", "logo": "https://example.com/penguins_logo.png"},
            {"name": "Washington Capitals", "logo": "https://example.com/capitals_logo.png"},
            {"name": "Carolina Hurricanes", "logo": "https://example.com/hurricanes_logo.png"},
            {"name": "Columbus Blue Jackets", "logo": "https://example.com/blue_jackets_logo.png"}
            ],
            'CEN': [
            {"name": "Chicago Blackhawks", "logo": "https://example.com/blackhawks_logo.png"},
            {"name": "Colorado Avalanche", "logo": "https://example.com/avalanche_logo.png"},
            {"name": "Dallas Stars", "logo": "https://example.com/stars_logo.png"},
            {"name": "Minnesota Wild", "logo": "https://example.com/wild_logo.png"},
            {"name": "Nashville Predators", "logo": "https://example.com/predators_logo.png"},
            {"name": "St. Louis Blues", "logo": "https://example.com/blues_logo.png"},
            {"name": "Winnipeg Jets", "logo": "https://example.com/jets_logo.png"},
            {"name": "Utah Hockey Club", "logo": "https://example.com/utah_logo.png"}
            ],
            'PAC': [
            {"name": "Anaheim Ducks", "logo": "https://example.com/ducks_logo.png"},
            {"name": "Calgary Flames", "logo": "https://example.com/flames_logo.png"},
            {"name": "Edmonton Oilers", "logo": "https://example.com/oilers_logo.png"},
            {"name": "Los Angeles Kings", "logo": "https://example.com/kings_logo.png"},
            {"name": "San Jose Sharks", "logo": "https://example.com/sharks_logo.png"},
            {"name": "Seattle Kraken", "logo": "https://example.com/kraken_logo.png"},
            {"name": "Vancouver Canucks", "logo": "https://example.com/canucks_logo.png"},
            {"name": "Vegas Golden Knights", "logo": "https://example.com/vegas_logo.png"}
            ]
        }

        self.stdout.write("Čistím DakynScore od starých dat...")
        Team.objects.all().delete()

        self.stdout.write("Vkládám týmy Chance Ligy...")
        for name in chance_liga:
            Team.objects.create(name=name, league='CHANCE', division='CZE')
        
        self.stdout.write("Vkládám týmy NHL podle divizí...")
        for div_code, teams in nhl_divisions.items():
            for team_data in teams:
                Team.objects.create(name=team_data['name'], league='NHL', division=div_code, logo_url=team_data['logo'])

        self.stdout.write(self.style.SUCCESS('Hotovo! Všechny týmy byly úspěšně importovány s divizemi.'))