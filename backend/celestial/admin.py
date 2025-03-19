from django.contrib import admin
from .models import System, Star, Planet, AsteroidBelt

@admin.register(Star)
class StarAdmin(admin.ModelAdmin):
    list_display = ('id', 'star_type')
    list_filter = ('star_type',)
    search_fields = ('star_type',)

@admin.register(System)
class SystemAdmin(admin.ModelAdmin):
    list_display = ('id', 'x', 'y', 'star', 'game')
    list_filter = ('game',)
    search_fields = ('x', 'y', 'star__star_type')
    raw_id_fields = ('star', 'game')

@admin.register(Planet)
class PlanetAdmin(admin.ModelAdmin):
    list_display = ('id', 'system', 'orbit', 'mineral_production', 'organic_production')
    list_filter = ('system',)
    search_fields = ('system__x', 'system__y', 'orbit')
    raw_id_fields = ('system',)
    fieldsets = (
        ('Basic Information', {
            'fields': ('system', 'orbit')
        }),
        ('Resource Production', {
            'fields': (
                'mineral_production', 'organic_production',
                'radioactive_production', 'exotic_production'
            )
        }),
        ('Storage Capacity', {
            'fields': (
                'mineral_storage_capacity', 'organic_storage_capacity',
                'radioactive_storage_capacity', 'exotic_storage_capacity'
            )
        }),
    )

@admin.register(AsteroidBelt)
class AsteroidBeltAdmin(admin.ModelAdmin):
    list_display = ('id', 'system', 'orbit', 'mineral_production', 'organic_production')
    list_filter = ('system',)
    search_fields = ('system__x', 'system__y', 'orbit')
    raw_id_fields = ('system',)
    fieldsets = (
        ('Basic Information', {
            'fields': ('system', 'orbit')
        }),
        ('Resource Production', {
            'fields': (
                'mineral_production', 'organic_production',
                'radioactive_production', 'exotic_production'
            )
        }),
    )

