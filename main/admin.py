from django.contrib import admin
from .models import Team, Player, Match, Goal

class GoalInline(admin.TabularInline):
    model = Goal
    extra = 1

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "player":
            # Získání ID zápasu z URL (objekt, který právě měníme)
            # Django admin používá v URL cestu /change/ID/
            object_id = request.resolver_match.kwargs.get('object_id')
            
            if object_id:
                # Najdeme aktuální zápas v databázi
                match = Match.objects.get(pk=object_id)
                # Vyfiltrujeme hráče, kteří patří buď do domácího, nebo hostujícího týmu
                kwargs["queryset"] = Player.objects.filter(
                    team__in=[match.home_team, match.away_team]
                ).order_by('team', 'name')
            else:
                # Pokud vytváříme nový zápas, seznam hráčů bude prázdný (dokud zápas neuložíme)
                kwargs["queryset"] = Player.objects.none()
                
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    model = Goal
    extra = 1

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "player":
            # 1. Pokusíme se získat ID zápasu z URL (pro editaci existujícího)
            resolved = request.resolver_match
            match_id = resolved.kwargs.get('object_id')
            
            if match_id:
                try:
                    match_obj = Match.objects.get(pk=match_id)
                    # Omezíme výběr na hráče domácího a hostujícího týmu
                    kwargs["queryset"] = Player.objects.filter(
                        team__in=[match_obj.home_team, match_obj.away_team]
                    ).order_by('team__name', 'name')
                except Match.DoesNotExist:
                    pass
            else:
                # 2. Pokud ID v URL není (vytváříme nový zápas), 
                # tak zatím zobrazíme prázdný seznam nebo nic, 
                # protože týmy ještě nejsou vybrané a uložené.
                kwargs["queryset"] = Player.objects.none()

        return super().formfield_for_foreignkey(db_field, request, **kwargs)

@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ('id', 'home_team', 'away_team', 'home_score', 'away_score', 'status', 'start_time')
    list_editable = ('home_score', 'away_score', 'status')
    inlines = [GoalInline]
    
    # Tato drobnost vynutí, aby se Inline formuláře znovu načetly správně
    def save_formset(self, request, form, formset, change):
        formset.save()

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'league', 'division')
    ordering = ('pk',)

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('name', 'number', 'team', 'position')
    list_filter = ('team', 'position')
    search_fields = ('name',)

@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = ('match', 'player')