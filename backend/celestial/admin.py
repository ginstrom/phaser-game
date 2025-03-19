from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import System, Star, Planet, AsteroidBelt
from .forms import PlanetForm, AsteroidBeltForm
from django import forms

@admin.register(Star)
class StarAdmin(admin.ModelAdmin):
    list_display = ('id', 'star_type')
    list_filter = ('star_type',)
    search_fields = ('star_type',)

class PlanetInline(admin.TabularInline):
    model = Planet
    form = PlanetForm
    extra = 0
    readonly_fields = ('mineral_production', 'organic_production', 
                      'radioactive_production', 'exotic_production',
                      'mineral_storage_capacity', 'organic_storage_capacity',
                      'radioactive_storage_capacity', 'exotic_storage_capacity',
                      'get_link')
    fields = ('get_link', 'orbit', 'empire', 'mineral_production', 'organic_production', 
              'radioactive_production', 'exotic_production',
              'mineral_storage_capacity', 'organic_storage_capacity',
              'radioactive_storage_capacity', 'exotic_storage_capacity')
    
    def get_formset(self, request, obj=None, **kwargs):
        if obj is None:
            return super().get_formset(request, obj, **kwargs)
        
        # Create the formset with the system parameter
        formset = super().get_formset(request, obj, **kwargs)
        formset.form = type('PlanetFormWithSystem', (self.form,), {
            '__init__': lambda self, *args, **kwargs: super(self.__class__, self).__init__(*args, system=obj, **kwargs)
        })
        
        return formset
    
    def get_link(self, obj):
        return mark_safe(f'<a href="/admin/celestial/planet/{obj.id}/change/">View Details</a>')
    get_link.short_description = "Actions"

class AsteroidBeltInline(admin.TabularInline):
    model = AsteroidBelt
    form = AsteroidBeltForm
    extra = 0
    readonly_fields = ('mineral_production', 'organic_production', 
                      'radioactive_production', 'exotic_production', 'get_link')
    fields = ('get_link', 'orbit', 'empire', 'mineral_production', 'organic_production', 
              'radioactive_production', 'exotic_production')
    
    def get_formset(self, request, obj=None, **kwargs):
        if obj is None:
            return super().get_formset(request, obj, **kwargs)
        
        # Create the formset with the system parameter
        formset = super().get_formset(request, obj, **kwargs)
        formset.form = type('AsteroidBeltFormWithSystem', (self.form,), {
            '__init__': lambda self, *args, **kwargs: super(self.__class__, self).__init__(*args, system=obj, **kwargs)
        })
        
        return formset
    
    def get_link(self, obj):
        return mark_safe(f'<a href="/admin/celestial/asteroidbelt/{obj.id}/change/">View Details</a>')
    get_link.short_description = "Actions"

@admin.register(System)
class SystemAdmin(admin.ModelAdmin):
    list_display = ('id', 'x', 'y', 'star', 'get_planets_count', 'get_asteroid_belts_count')
    list_filter = ('game',)
    search_fields = ('x', 'y', 'star__star_type')
    raw_id_fields = ('game',)
    inlines = [PlanetInline, AsteroidBeltInline]
    
    def get_planets_count(self, obj):
        return obj.planets.count()
    get_planets_count.short_description = "Planets"
    
    def get_asteroid_belts_count(self, obj):
        return obj.asteroid_belts.count()
    get_asteroid_belts_count.short_description = "Asteroid Belts"

@admin.register(Planet)
class PlanetAdmin(admin.ModelAdmin):
    form = PlanetForm
    list_display = ('id', 'system', 'orbit', 'empire', 'mineral_production', 'organic_production')
    list_filter = ('system', 'empire')
    search_fields = ('system__x', 'system__y', 'orbit', 'empire__name')
    raw_id_fields = ('system', 'empire')
    fieldsets = (
        ('Basic Information', {
            'fields': ('system', 'orbit', 'empire')
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

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if obj:
            form = type('PlanetFormWithSystem', (form,), {
                '__init__': lambda self, *args, **kwargs: super(self.__class__, self).__init__(*args, system=obj.system, **kwargs)
            })
        return form

@admin.register(AsteroidBelt)
class AsteroidBeltAdmin(admin.ModelAdmin):
    form = AsteroidBeltForm
    list_display = ('id', 'system', 'orbit', 'empire', 'mineral_production', 'organic_production')
    list_filter = ('system', 'empire')
    search_fields = ('system__x', 'system__y', 'orbit', 'empire__name')
    raw_id_fields = ('system', 'empire')
    fieldsets = (
        ('Basic Information', {
            'fields': ('system', 'orbit', 'empire')
        }),
        ('Resource Production', {
            'fields': (
                'mineral_production', 'organic_production',
                'radioactive_production', 'exotic_production'
            )
        }),
    )

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if obj:
            form = type('AsteroidBeltFormWithSystem', (form,), {
                '__init__': lambda self, *args, **kwargs: super(self.__class__, self).__init__(*args, system=obj.system, **kwargs)
            })
        return form

