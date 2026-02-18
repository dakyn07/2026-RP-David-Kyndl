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
    # Odstraněno is_running a přidáno list_editable pro rychlé změny
    list_display = ('__str__', 'home_score', 'away_score', 'status', 'display_minute', 'start_time')
    list_editable = ('home_score', 'away_score', 'status')
    list_filter = ('home_team__league', 'status')
    
    # Ponechali jsme jen akci pro ruční ukončení (pokud by automat selhal)
    actions = ['force_finish_match']

    def display_minute(self, obj):
        """Zobrazí minutu přímo v seznamu zápasů"""
        return f"{obj.current_minute}'"
    display_minute.short_description = "Minuta"

    @admin.action(description="🏁 Označit jako ukončené")
    def force_finish_match(self, request, queryset):
        queryset.update(status='FIN')
        self.message_user(request, "Vybrané zápasy byly ukončeny.", messages.INFO)

    def get_inline_instances(self, request, obj=None):
        """Dynamicky vybere, které inliny se zobrazí podle ligy (NHL = hokej, Chance = hokej/fotbal)."""
        inlines = [GoalInline]
        
        if obj:
            league = obj.home_team.league.upper()
            # NHL má tresty, ostatní (včetně Chance, pokud ji hraješ jako fotbal) mají karty
            if league == 'NHL':
                inlines.append(PenaltyInline)
            else:
                inlines.append(CardInline)
        else:
            # Při vytváření nového zápasu zobrazíme vše
            inlines.extend([CardInline, PenaltyInline])
            
        return [inline(self.model, self.admin_site) for inline in inlines]

# --- OSTATNÍ ADMINY ---

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'league', 'division')
    list_filter = ('league', 'division')
    search_fields = ('name',)

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('name', 'number', 'team', 'position')
    list_filter = ('team__league', 'team', 'position')
    search_fields = ('name',)

# Registrace modelů pro samostatné úpravy
admin.site.register(Goal)
admin.site.register(Card)
admin.site.register(Penalty)