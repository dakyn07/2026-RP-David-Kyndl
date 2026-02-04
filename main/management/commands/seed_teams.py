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
                "Boston Bruins", "Florida Panthers", "Montreal Canadiens", "Ottawa Senators",
                "Tampa Bay Lightning", "Toronto Maple Leafs", "Detroit Red Wings", "Buffalo Sabres"
            ],
            'MET': [
                "New York Rangers", "New York Islanders", "New Jersey Devils", "Philadelphia Flyers",
                "Pittsburgh Penguins", "Washington Capitals", "Carolina Hurricanes", "Columbus Blue Jackets"
            ],
            'CEN': [
                "Chicago Blackhawks", "Colorado Avalanche", "Dallas Stars", "Minnesota Wild",
                "Nashville Predators", "St. Louis Blues", "Winnipeg Jets", "Utah Hockey Club"
            ],
            'PAC': [
                "Anaheim Ducks", "Calgary Flames", "Edmonton Oilers", "Los Angeles Kings",
                "San Jose Sharks", "Seattle Kraken", "Vancouver Canucks", "Vegas Golden Knights"
            ]
        }

        self.stdout.write("Čistím DakynScore od starých dat...")
        Team.objects.all().delete()

        self.stdout.write("Vkládám týmy Chance Ligy...")
        for name in chance_liga:
            Team.objects.create(name=name, league='CHANCE', division='CZE')
        
        self.stdout.write("Vkládám týmy NHL podle divizí...")
        for div_code, teams in nhl_divisions.items():
            for name in teams:
                Team.objects.create(name=name, league='NHL', division=div_code)

        self.stdout.write(self.style.SUCCESS('Hotovo! Všechny týmy byly úspěšně importovány s divizemi.'))