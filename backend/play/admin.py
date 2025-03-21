from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Player, Race, Empire, Game
from celestial.models import System, Planet, AsteroidBelt

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
    readonly_fields = ('name', 'player', 'race', 'get_link')
    fields = ('get_link', 'name', 'player', 'race')
    
    def get_link(self, obj):
        return mark_safe(f'<a href="/admin/play/empire/{obj.id}/change/">View Details</a>')
    get_link.short_description = "Actions"

class SystemInline(admin.TabularInline):
    model = System
    extra = 0
    readonly_fields = ('x', 'y', 'star', 'get_planets', 'get_asteroid_belts', 'get_link')
    fields = ('get_link', 'x', 'y', 'star', 'get_planets', 'get_asteroid_belts')
    
    def get_link(self, obj):
        return mark_safe(f'<a href="/admin/celestial/system/{obj.id}/change/">View Details</a>')
    get_link.short_description = "Actions"
    
    def get_planets(self, obj):
        return ", ".join([f"Planet {p.id} (Orbit {p.orbit})" for p in obj.planets.all()])
    get_planets.short_description = "Planets"
    
    def get_asteroid_belts(self, obj):
        return ", ".join([f"Asteroid Belt {b.id} (Orbit {b.orbit})" for b in obj.asteroid_belts.all()])
    get_asteroid_belts.short_description = "Asteroid Belts"

@admin.register(Empire)
class EmpireAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'player', 'race', 'game')
    list_filter = ('player__player_type', 'race', 'game')
    search_fields = ('name', 'race__name', 'player__player_type')
    raw_id_fields = ('player', 'race', 'game')
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'player', 'race', 'game')
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
        ('Owned Celestial Bodies', {
            'fields': ('get_planets', 'get_asteroid_belts'),
            'classes': ('readonly',)
        }),
    )
    readonly_fields = (
        'mineral_capacity', 'organic_capacity',
        'radioactive_capacity', 'exotic_capacity',
        'get_planets', 'get_asteroid_belts'
    )
    
    def get_planets(self, obj):
        planets = []
        for p in obj.owned_planets.all():
            link = f'<a href="/admin/celestial/planet/{p.id}/change/">Planet {p.id}</a>'
            planets.append(f"{link} (System {p.system.id}, Orbit {p.orbit})")
        return mark_safe("<br>".join(planets))
    get_planets.short_description = "Planets"
    
    def get_asteroid_belts(self, obj):
        belts = []
        for b in obj.owned_asteroid_belts.all():
            link = f'<a href="/admin/celestial/asteroidbelt/{b.id}/change/">Asteroid Belt {b.id}</a>'
            belts.append(f"{link} (System {b.system.id}, Orbit {b.orbit})")
        return mark_safe("<br>".join(belts))
    get_asteroid_belts.short_description = "Asteroid Belts"

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('id', 'turn', 'created', 'modified')
    search_fields = ('id',)
    inlines = [EmpireInline, SystemInline]
    readonly_fields = ('created', 'modified')
    fieldsets = (
        ('Basic Information', {
            'fields': ('turn', 'created', 'modified')
        }),
    )

