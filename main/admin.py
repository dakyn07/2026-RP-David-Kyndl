from django.contrib import admin
from .models import Team, Player, Match, Goal, Card, Penalty

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

class GoalInline(MatchEventMixin, admin.TabularInline):
    model = Goal
    extra = 1

class CardInline(MatchEventMixin, admin.TabularInline):
    model = Card
    extra = 1

class PenaltyInline(MatchEventMixin, admin.TabularInline):
    model = Penalty
    extra = 1

@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'home_score', 'away_score', 'status', 'start_time')
    list_filter = ('home_team__league', 'status')
    
    def get_inline_instances(self, request, obj=None):
        """Dynamicky vybere, které inliny se zobrazí podle ligy."""
        inlines = [GoalInline] # Gól je v obou sportech
        
        if obj: # Pokud už zápas existuje
            league = obj.home_team.league
            if league == 'NHL':
                inlines.append(PenaltyInline)
            elif league == 'CHANCE':
                inlines.append(CardInline)
        else:
            # Při vytváření nového zápasu (kdy ještě nevíme ligu) 
            # můžeme zobrazit vše nebo nic. Zobrazíme raději vše:
            inlines.extend([CardInline, PenaltyInline])
            
        return [inline(self.model, self.admin_site) for inline in inlines]

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'league', 'division')
    list_filter = ('league',)

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('name', 'number', 'team', 'position')
    list_filter = ('team__league', 'team', 'position')
    search_fields = ('name',)