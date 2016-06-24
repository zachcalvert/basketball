from django.contrib import admin

from schedule.models import Season, Game


class GameInline(admin.TabularInline):
    model = Game
    extra = 0
    show_change_link = True
    readonly_fields = ['date', 'home_team', 'home_points', 'away_points', 'away_team']
    exclude = ['tipoff', 'boxscore_link', 'statlines']
    can_delete = False


class GameAdmin(admin.ModelAdmin):
    readonly_fields = ('season', 'date', 'result')
    exclude = ['home_team', 'away_team', 'home_points', 'away_points', 'tipoff', 'statlines', 'boxscore_link']
    list_display = ('date', 'home_team', 'home_points', 'away_points', 'away_team')


class SeasonAdmin(admin.ModelAdmin):
	list_display = ('year',)
	inlines = [GameInline,]


admin.site.register(Game, GameAdmin)
admin.site.register(Season, SeasonAdmin)