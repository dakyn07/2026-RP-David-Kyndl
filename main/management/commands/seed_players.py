from django.core.management.base import BaseCommand
from main.models import Team, Player

class Command(BaseCommand):
    help = 'Vyčistí databázi a nahraje aktuální reálné soupisky všech týmů Chance Ligy 24/25'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING('🧹 Čistím databázi hráčů...'))
        Player.objects.all().delete()

        # Aktuální soupisky 2024/2025
        rosters = {
            "AC Sparta Praha": [
                (1, "Peter Vindahl", "GK"), (27, "Filip Panák", "DF"), (25, "Asger Sørensen", "DF"),
                (17, "Angelo Preciado", "DF"), (33, "Elias Cobbaut", "DF"), (6, "Kaan Kairinen", "MD"),
                (18, "Lukáš Sadílek", "MD"), (14, "Veljko Birmančević", "FW"), (10, "Albion Rrahmani", "FW"),
                (20, "Qazim Laçi", "MD"), (29, "Ermal Krasniqi", "FW")
            ],
            "SK Slavia Praha": [
                (36, "Jindřich Staněk", "GK"), (1, "Ondřej Kolář", "GK"), (3, "Tomáš Holeš", "DF"),
                (4, "David Zima", "DF"), (5, "Igoh Ogbu", "DF"), (19, "Oscar Dorley", "MD"),
                (17, "Lukáš Provod", "MD"), (10, "Christos Zafeiris", "MD"), (25, "Tomáš Chorý", "FW"),
                (13, "Mojmír Chytil", "FW"), (12, "El Hadji Malick Diouf", "DF")
            ],
            "FC Viktoria Plzeň": [
                (16, "Martin Jedlička", "GK"), (2, "Lukáš Hejda", "DF"), (40, "Sampson Dweh", "DF"),
                (22, "Cadu", "DF"), (6, "Lukáš Červ", "MD"), (23, "Lukáš Kalvach", "MD"),
                (10, "Jan Kopic", "MD"), (37, "Prince Adu", "FW"), (51, "Erik Jirka", "MD"),
                (93, "Rafiu Durosinmi", "FW"), (9, "Ricardinho", "FW")
            ],
            "FC Baník Ostrava": [
                (30, "Jakub Markovič", "GK"), (17, "Michal Frydrych", "DF"), (15, "Patrick Kpozo", "DF"),
                (10, "Matěj Šín", "MD"), (32, "Ewerton", "FW"), (21, "Jiří Klíma", "FW"),
                (9, "David Buchta", "MD"), (5, "Jiří Boula", "MD"), (13, "Karel Pojezný", "DF")
            ],
            "FK Mladá Boleslav": [
                (1, "Matouš Trmal", "GK"), (17, "Marek Suchý", "DF"), (23, "Vasil Kušej", "FW"),
                (10, "Patrik Vydra", "MD"), (14, "Tomáš Ladra", "FW"), (5, "Benson Sakala", "MD")
            ],
            "FC Slovan Liberec": [
                (1, "Hugo Jan Bačkovský", "GK"), (2, "Dominik Plechatý", "DF"), (8, "Lukáš Letenay", "FW"),
                (10, "Ľubomír Tupta", "FW"), (6, "Ivan Varfolomejev", "MD"), (25, "Ahmad Ghali", "MD")
            ],
            "FK Jablonec": [
                (1, "Jan Hanuš", "GK"), (4, "Nemanja Tekijaški", "DF"), (25, "Jan Fortelný", "MD"),
                (10, "Michal Beran", "MD"), (24, "Jan Chramosta", "FW"), (32, "Bienvenue Kanakimana", "FW")
            ],
            "SK Sigma Olomouc": [
                (1, "Tomáš Digaňa", "GK"), (22, "Vít Beneš", "DF"), (7, "Radim Breite", "MD"),
                (10, "Filip Zorvan", "MD"), (14, "Jan Kliment", "FW"), (9, "Lukáš Juliš", "FW")
            ],
            "FC Hradec Králové": [
                (1, "Adam Zadražil", "GK"), (5, "Filip Čihák", "DF"), (6, "Václav Pilař", "MD"),
                (22, "Petr Kodeš", "MD"), (21, "Daniel Vašulín", "FW"), (11, "Adam Griger", "FW")
            ],
            "Bohemians Praha 1905": [
                (1, "Roman Valeš", "GK"), (28, "Lukáš Hůlka", "DF"), (10, "Jan Matoušek", "MD"),
                (19, "Jan Kovařík", "MD"), (20, "Václav Drchal", "FW"), (9, "Abdulla Yusuf Helal", "FW")
            ],
            "1.FC Slovácko": [
                (1, "Milan Heča", "GK"), (6, "Stanislav Hofmann", "DF"), (11, "Milan Petržela", "MD"),
                (13, "Michal Kohút", "MD"), (22, "Rigino Cicilia", "FW"), (10, "Marek Havlík", "MD")
            ],
            "FK Teplice": [
                (1, "Richard Ludha", "GK"), (18, "Nemanja Mićević", "DF"), (20, "Daniel Trubač", "MD"),
                (11, "Filip Horský", "FW"), (10, "Abdoullah Gning", "FW"), (28, "Jan Mareček", "MD")
            ],
            "MFK Karviná": [
                (1, "Jakub Lapeš", "GK"), (22, "Jaroslav Svozil", "DF"), (10, "Kristián Vallo", "MD"),
                (7, "Amar Memić", "MD"), (9, "Martin Regáli", "FW"), (26, "Lucky Ezeh", "FW")
            ],
            "FK Pardubice": [
                (1, "Viktor Budinský", "GK"), (5, "Denis Halinský", "DF"), (10, "Dominik Janošek", "MD"),
                (24, "Vojtěch Patrák", "FW"), (9, "André Leipold", "FW"), (15, "Tomáš Zlatohlávek", "FW")
            ],
            "FC Zlín": [
                (1, "Matej Rakovan", "GK"), (17, "Stanislav Dostál", "GK"), (4, "Jakub Černín", "DF"),
                (14, "Lukáš Bartošák", "DF"), (28, "Tomáš Didiba", "DF"), (6, "Joss Didiba", "MD"),
                (10, "Tomáš Poznar", "FW"), (11, "Youba Dramé", "FW"), (33, "Vukadin Vukadinović", "MD"),
                (19, "Jakub Janetzký", "MD"), (7, "Rudolf Reiter", "MD")
            ],
            "FK Dukla Praha": [
                (1, "Matúš Hruška", "GK"), (15, "Jan Peterka", "DF"), (11, "Jakub Hora", "MD"),
                (10, "Muris Mešanović", "FW"), (8, "Štěpán Šebrle", "MD"), (22, "Jakub Řezníček", "FW")
            ],



            # --- NHL: ATLANTICKÁ DIVIZE ---
            "Boston Bruins": [(1, "Jeremy Swayman", "GK"), (73, "Charlie McAvoy", "DF"), (88, "David Pastrňák", "FW"), (63, "Brad Marchand", "FW"), (18, "Pavel Zacha", "FW")],
            "Florida Panthers": [(72, "Sergei Bobrovsky", "GK"), (5, "Aaron Ekblad", "DF"), (16, "Aleksander Barkov", "FW"), (19, "Matthew Tkachuk", "FW")],
            "Toronto Maple Leafs": [(60, "Joseph Woll", "GK"), (44, "Morgan Rielly", "DF"), (34, "Auston Matthews", "FW"), (16, "Mitch Marner", "FW")],
            "Tampa Bay Lightning": [(88, "Andrei Vasilevskiy", "GK"), (77, "Victor Hedman", "DF"), (86, "Nikita Kucherov", "FW"), (21, "Brayden Point", "FW")],
            "Detroit Red Wings": [(39, "Ville Husso", "GK"), (53, "Moritz Seider", "DF"), (71, "Dylan Larkin", "FW"), (23, "Lucas Raymond", "FW")],
            "Buffalo Sabres": [(1, "Ukko-Pekka Luukkonen", "GK"), (26, "Rasmus Dahlin", "DF"), (72, "Tage Thompson", "FW"), (12, "Jiří Kulich", "FW")],
            "Ottawa Senators": [(35, "Linus Ullmark", "GK"), (72, "Thomas Chabot", "DF"), (7, "Brady Tkachuk", "FW"), (18, "Tim Stützle", "FW")],
            "Montreal Canadiens": [
                (35, "Samuel Montembeault", "GK"),
                (75, "Jakub Dobeš", "GK"),
                (53, "Noah Dobson", "DF"),
                (21, "Kaiden Guhle", "DF"),
                (45, "Alexandre Carrier", "DF"),
                (72, "Arber Xhekaj", "DF"),
                (47, "Jayden Struble", "DF"),
                (48, "Lane Hutson", "DF"),
                (8, "Mike Matheson", "DF"),
                (20, "Juraj Slafkovský", "FW"),
                (14, "Nick Suzuki", "FW"),
                (13, "Cole Caufield", "FW"),
                (92, "Patrik Laine", "FW"),
                (77, "Kirby Dach", "FW"),
                (93, "Ivan Demidov", "FW"),
                (15, "Alex Newhook", "FW"),
                (11, "Brendan Gallagher", "FW"),
                (17, "Josh Anderson", "FW"),
                (24, "Phillip Danault", "FW"),
                (71, "Jake Evans", "FW"),
                (90, "Joseph Veleno", "FW"),
                (76, "Zachary Bolduc", "FW"),
                (85, "Alexandre Texier", "FW"),
                (91, "Oliver Kapanen", "FW"),
            ],
            # --- NHL: METROPOLITNÍ DIVIZE ---
            "New York Rangers": [(31, "Igor Shesterkin", "GK"), (23, "Adam Fox", "DF"), (10, "Artemi Panarin", "FW"), (93, "Mika Zibanejad", "FW")],
            "Carolina Hurricanes": [(31, "Frederik Andersen", "GK"), (74, "Jaccob Slavin", "DF"), (88, "Martin Nečas", "FW"), (20, "Sebastian Aho", "FW")],
            "New Jersey Devils": [(25, "Jacob Markström", "GK"), (7, "Dougie Hamilton", "DF"), (86, "Jack Hughes", "FW"), (18, "Ondřej Palát", "FW")],
            "Washington Capitals": [(79, "Charlie Lindgren", "GK"), (74, "John Carlson", "DF"), (8, "Alex Ovechkin", "FW"), (18, "Jakub Vrána", "FW")],
            "New York Islanders": [(30, "Ilya Sorokin", "GK"), (8, "Noah Dobson", "DF"), (13, "Mathew Barzal", "FW"), (14, "Bo Horvat", "FW")],
            "Philadelphia Flyers": [(33, "Samuel Ersson", "GK"), (6, "Travis Sanheim", "DF"), (11, "Travis Konecny", "FW"), (94, "Matvei Michkov", "FW")],
            "Pittsburgh Penguins": [(35, "Tristan Jarry", "GK"), (58, "Kris Letang", "DF"), (87, "Sidney Crosby", "FW"), (71, "Evgeni Malkin", "FW")],
            "Columbus Blue Jackets": [(90, "Elvis Merzlikins", "GK"), (8, "Zach Werenski", "DF"), (86, "Kirill Marchenko", "FW"), (5, "David Jiříček", "DF")],

            # --- NHL: CENTRÁLNÍ DIVIZE ---
            "Dallas Stars": [(29, "Jake Oettinger", "GK"), (4, "Miro Heiskanen", "DF"), (21, "Jason Robertson", "FW"), (24, "Roope Hintz", "FW")],
            "Colorado Avalanche": [(40, "Alexandar Georgiev", "GK"), (8, "Cale Makar", "DF"), (29, "Nathan MacKinnon", "FW"), (96, "Mikko Rantanen", "FW")],
            "Winnipeg Jets": [(37, "Connor Hellebuyck", "GK"), (44, "Josh Morrissey", "DF"), (55, "Mark Scheifele", "FW"), (81, "Kyle Connor", "FW")],
            "Nashville Predators": [(74, "Juuse Saros", "GK"), (59, "Roman Josi", "DF"), (91, "Steven Stamkos", "FW"), (9, "Filip Forsberg", "FW")],
            "St. Louis Blues": [(50, "Jordan Binnington", "GK"), (55, "Colton Parayko", "DF"), (25, "Robert Thomas", "FW"), (18, "Radek Faksa", "FW")],
            "Minnesota Wild": [(32, "Filip Gustavsson", "GK"), (7, "Brock Faber", "DF"), (97, "Kirill Kaprizov", "FW"), (12, "Matt Boldy", "FW")],
            "Utah Hockey Club": [(39, "Connor Ingram", "GK"), (50, "Sean Durzi", "DF"), (9, "Clayton Keller", "FW"), (11, "Dylan Guenther", "FW")],
            "Chicago Blackhawks": [(34, "Petr Mrázek", "GK"), (4, "Seth Jones", "DF"), (98, "Connor Bedard", "FW"), (15, "Lukas Reichel", "FW")],

            # --- NHL: PACIFICKÁ DIVIZE ---
            "Vancouver Canucks": [(35, "Thatcher Demko", "GK"), (43, "Quinn Hughes", "DF"), (9, "J.T. Miller", "FW"), (17, "Filip Hronek", "DF")],
            "Edmonton Oilers": [(72, "Stuart Skinner", "GK"), (2, "Evan Bouchard", "DF"), (97, "Connor McDavid", "FW"), (29, "Leon Draisaitl", "FW")],
            "Vegas Golden Knights": [(36, "Logan Thompson", "GK"), (7, "Alex Pietrangelo", "DF"), (9, "Jack Eichel", "FW"), (48, "Tomáš Hertl", "FW")],
            "Los Angeles Kings": [(31, "David Rittich", "GK"), (8, "Drew Doughty", "DF"), (11, "Anze Kopitar", "FW"), (9, "Adrian Kempe", "FW")],
            "Seattle Kraken": [(31, "Philipp Grubauer", "GK"), (29, "Vince Dunn", "DF"), (10, "Matty Beniers", "FW"), (17, "Jaden Schwartz", "FW")],
            "Calgary Flames": [(80, "Dan Vladař", "GK"), (11, "Mikael Backlund", "FW"), (47, "Connor Zary", "FW"), (62, "Kevin Bahl", "DF")],
            "Anaheim Ducks": [(36, "John Gibson", "GK"), (7, "Radko Gudas", "DF"), (19, "Troy Terry", "FW"), (11, "Trevor Zegras", "FW")],
            "San Jose Sharks": [(41, "Vitek Vanecek", "GK"), (71, "Macklin Celebrini", "FW"), (11, "William Eklund", "FW"), (5, "Cody Ceci", "DF")],
        }

        success_count = 0
        for team_name, players in rosters.items():
            try:
                # Najdeme tým (musí se v administraci jmenovat PŘESNĚ takto)
                team = Team.objects.get(name=team_name)
                
                for num, name, pos in players:
                    Player.objects.create(team=team, name=name, number=num, position=pos)
                
                self.stdout.write(self.style.SUCCESS(f"✅ {team_name} nasazen."))
                success_count += 1
            except Team.DoesNotExist:
                self.stdout.write(self.style.ERROR(f"❌ Tým '{team_name}' nebyl nalezen. Zkontroluj název v Adminu!"))

        self.stdout.write(self.style.SUCCESS(f'✨ Hotovo! Úspěšně nasazeno {success_count} týmů.'))