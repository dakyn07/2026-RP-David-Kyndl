from django.contrib import admin, messages
from django.utils import timezone
from .models import Team, Player, Match, Goal, Card, Penalty

# --- MIXINY A POMOCNÉ TŘÍDY ---

class MatchEventMixin:
    """Omezí výběr hráčů v adminu pouze na ty, kteří hrají daný zápas."""
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "player":
            object_id = request.resolver_match.kwargs.get('object_id')
            if object_id:
                try:
                    match_obj = Match.objects.get(pk=object_id)
                    kwargs["queryset"] = Player.objects.filter(
                        team__in=[match_obj.home_team, match_obj.away_team]
                    )
                except Match.DoesNotExist:
                    pass
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

# --- INLINE EDITACE (Góly, Karty, Tresty) ---

class GoalInline(MatchEventMixin, admin.TabularInline):
    model = Goal
    extra = 1

class CardInline(MatchEventMixin, admin.TabularInline):
    model = Card
    extra = 1

class PenaltyInline(MatchEventMixin, admin.TabularInline):
    model = Penalty
    extra = 1

# --- HLAVNÍ ADMIN ROZHRANÍ PRO ZÁPAS ---

@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    # Přidali jsme sloupce pro stav běhu a aktuální minutu
    list_display = ('__str__', 'home_score', 'away_score', 'status', 'is_running', 'display_minute', 'start_time')
    list_filter = ('home_team__league', 'status', 'is_running')
    
    # Definice tlačítek v menu "Akce"
    actions = ['start_timer', 'pause_timer', 'finish_match']

    def display_minute(self, obj):
        """Zobrazí minutu přímo v seznamu zápasů"""
        return f"{obj.current_minute}'"
    display_minute.short_description = "Aktuální minuta"

    @admin.action(description="▶ Spustit / Pokračovat v čase")
    def start_timer(self, request, queryset):
        for match in queryset:
            if not match.is_running:
                match.status = 'LIVE'
                match.last_start_time = timezone.now()
                match.is_running = True
                match.save()
        self.message_user(request, "Časomíra byla spuštěna.", messages.SUCCESS)

    @admin.action(description="⏸ Pozastavit čas (Pauza / Konec třetiny)")
    def pause_timer(self, request, queryset):
        for match in queryset:
            if match.is_running:
                now = timezone.now()
                # Spočítáme, kolik uběhlo od posledního kliku na START
                diff = (now - match.last_start_time).total_seconds()
                # Přičteme to k celkovému času zápasu
                match.current_elapsed_seconds += int(diff)
                match.is_running = False
                match.save()
        self.message_user(request, "Časomíra byla pozastavena.", messages.WARNING)

    @admin.action(description="🏁 Ukončit zápas (FIN)")
    def finish_match(self, request, queryset):
        for match in queryset:
            if match.is_running:
                now = timezone.now()
                diff = (now - match.last_start_time).total_seconds()
                match.current_elapsed_seconds += int(diff)
            
            match.is_running = False
            match.status = 'FIN'
            match.save()
        self.message_user(request, "Zápas byl označen jako ukončený.", messages.INFO)

    def get_inline_instances(self, request, obj=None):
        """Dynamicky vybere, které inliny se zobrazí podle ligy (Hokej vs Fotbal)."""
        inlines = [GoalInline]
        
        if obj:
            league = obj.home_team.league
            if league == 'NHL':
                inlines.append(PenaltyInline)
            elif league == 'CHANCE':
                inlines.append(CardInline)
        else:
            # Při vytváření nového zápasu zobrazíme vše
            inlines.extend([CardInline, PenaltyInline])
            
        return [inline(self.model, self.admin_site) for inline in inlines]

# --- OSTATNÍ ADMINY ---

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'league', 'division')
    list_filter = ('league',)

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('name', 'number', 'team', 'position')
    list_filter = ('team__league', 'team', 'position')
    search_fields = ('name',)