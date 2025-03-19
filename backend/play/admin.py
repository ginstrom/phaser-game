from django.contrib import admin
from .models import Player, Race, Empire, Game, System

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('id', 'player_type')
    list_filter = ('player_type',)
    search_fields = ('player_type',)

@admin.register(Race)
class RaceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

class EmpireInline(admin.TabularInline):
    model = Empire
    extra = 0
    readonly_fields = ('name', 'player', 'race')

class SystemInline(admin.TabularInline):
    model = System
    extra = 0
    readonly_fields = ('x', 'y', 'star')

@admin.register(Empire)
class EmpireAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'player', 'race', 'game')
    list_filter = ('player__player_type', 'race', 'game')
    search_fields = ('name', 'race__name', 'player__player_type')
    raw_id_fields = ('player', 'race', 'game')
    filter_horizontal = ('planets', 'asteroid_belts')
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'player', 'race', 'game')
        }),
        ('Territory', {
            'fields': ('planets', 'asteroid_belts')
        }),
        ('Resource Storage', {
            'fields': (
                'mineral_storage', 'organic_storage',
                'radioactive_storage', 'exotic_storage'
            )
        }),
        ('Resource Capacity', {
            'fields': (
                'mineral_capacity', 'organic_capacity',
                'radioactive_capacity', 'exotic_capacity'
            ),
            'classes': ('readonly',)
        }),
    )
    readonly_fields = (
        'mineral_capacity', 'organic_capacity',
        'radioactive_capacity', 'exotic_capacity'
    )

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('id', 'turn')
    search_fields = ('id',)
    inlines = [EmpireInline, SystemInline]
    fieldsets = (
        ('Basic Information', {
            'fields': ('turn',)
        }),
    )

