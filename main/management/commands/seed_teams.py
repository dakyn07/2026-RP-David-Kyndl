from django.core.management.base import BaseCommand
from main.models import Team

class Command(BaseCommand):
    help = 'Naplní DakynScore aktuálními týmy fotbalové Chance Ligy 25/26 se Zlínem'

    def handle(self, *args, **kwargs):
        chance_liga_25_26 = [
            "AC Sparta Praha", 
            "SK Slavia Praha", 
            "FC Viktoria Plzeň", 
            "FC Baník Ostrava", 
            "FK Mladá Boleslav", 
            "FC Slovan Liberec", 
            "SK Sigma Olomouc", 
            "FC Hradec Králové", 
            "FK Teplice", 
            "FK Jablonec", 
            "Bohemians Praha 1905", 
            "1.FC Slovácko", 
            "MFK Karviná", 
            "FK Pardubice", 
            "FK Dukla Praha",
            "FC Zlín"
        ]

        nhl_teams = [
            "Boston Bruins", "Florida Panthers", "Montreal Canadiens", "Ottawa Senators",
            "Tampa Bay Lightning", "Toronto Maple Leafs", "Detroit Red Wings", "Buffalo Sabres",
            "New York Rangers", "New York Islanders", "New Jersey Devils", "Philadelphia Flyers",
            "Pittsburgh Penguins", "Washington Capitals", "Carolina Hurricanes", "Columbus Blue Jackets",
            "Chicago Blackhawks", "Colorado Avalanche", "Dallas Stars", "Minnesota Wild",
            "Nashville Predators", "St. Louis Blues", "Winnipeg Jets", "Utah Hockey Club",
            "Anaheim Ducks", "Calgary Flames", "Edmonton Oilers", "Los Angeles Kings",
            "San Jose Sharks", "Seattle Kraken", "Vancouver Canucks", "Vegas Golden Knights"
        ]

        self.stdout.write("Čistím DakynScore od starých dat...")
        Team.objects.all().delete()

        self.stdout.write("Vkládám aktuální týmy (včetně Zlína)...")
        for name in chance_liga_25_26:
            Team.objects.create(name=name, league='CHANCE')
        
        for name in nhl_teams:
            Team.objects.create(name=name, league='NHL')

        self.stdout.write(self.style.SUCCESS('Hotovo! DakynScore má správné složení pro sezónu 25/26.'))
