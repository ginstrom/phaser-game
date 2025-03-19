from django import forms
from .models import Planet, AsteroidBelt, System

class PlanetForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        system = kwargs.pop('system', None)
        super().__init__(*args, **kwargs)
        
        # Get the system either from the instance or the passed system
        system = system or (self.instance.system if self.instance.pk else None)
        
        if system:
            # Set the system field
            self.fields['system'].initial = system
            self.fields['system'].widget = forms.HiddenInput()
            
            # Get all used orbits in the system
            used_orbits = set()
            used_orbits.update(system.planets.values_list('orbit', flat=True))
            used_orbits.update(system.asteroid_belts.values_list('orbit', flat=True))
            
            # If editing, exclude current planet's orbit
            if self.instance.pk:
                used_orbits.discard(self.instance.orbit)
            
            # Create choices for available orbits
            available_orbits = [(i, f"Orbit {i}") for i in range(1, System.MAX_ORBITS + 1) if i not in used_orbits]
            
            # Update orbit field choices
            self.fields['orbit'].widget = forms.Select(choices=available_orbits)
            if not available_orbits:
                self.fields['orbit'].widget.attrs['disabled'] = True
                self.fields['orbit'].help_text = "No orbits available in this system"

    def clean(self):
        cleaned_data = super().clean()
        system = cleaned_data.get('system')
        orbit = cleaned_data.get('orbit')
        
        if system and orbit:
            # Check if orbit is already taken
            if Planet.objects.filter(system=system, orbit=orbit).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError(f"Orbit {orbit} is already occupied in this system")
            if AsteroidBelt.objects.filter(system=system, orbit=orbit).exists():
                raise forms.ValidationError(f"Orbit {orbit} is already occupied in this system")
        
        return cleaned_data

    class Meta:
        model = Planet
        fields = '__all__'

class AsteroidBeltForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        system = kwargs.pop('system', None)
        super().__init__(*args, **kwargs)
        
        # Get the system either from the instance or the passed system
        system = system or (self.instance.system if self.instance.pk else None)
        
        if system:
            # Set the system field
            self.fields['system'].initial = system
            self.fields['system'].widget = forms.HiddenInput()
            
            # Get all used orbits in the system
            used_orbits = set()
            used_orbits.update(system.planets.values_list('orbit', flat=True))
            used_orbits.update(system.asteroid_belts.values_list('orbit', flat=True))
            
            # If editing, exclude current belt's orbit
            if self.instance.pk:
                used_orbits.discard(self.instance.orbit)
            
            # Create choices for available orbits
            available_orbits = [(i, f"Orbit {i}") for i in range(1, System.MAX_ORBITS + 1) if i not in used_orbits]
            
            # Update orbit field choices
            self.fields['orbit'].widget = forms.Select(choices=available_orbits)
            if not available_orbits:
                self.fields['orbit'].widget.attrs['disabled'] = True
                self.fields['orbit'].help_text = "No orbits available in this system"

    def clean(self):
        cleaned_data = super().clean()
        system = cleaned_data.get('system')
        orbit = cleaned_data.get('orbit')
        
        if system and orbit:
            # Check if orbit is already taken
            if Planet.objects.filter(system=system, orbit=orbit).exists():
                raise forms.ValidationError(f"Orbit {orbit} is already occupied in this system")
            if AsteroidBelt.objects.filter(system=system, orbit=orbit).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError(f"Orbit {orbit} is already occupied in this system")
        
        return cleaned_data

    class Meta:
        model = AsteroidBelt
        fields = '__all__' 