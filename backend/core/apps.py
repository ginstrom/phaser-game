"""Core app configuration for the game.

This module configures the core Django app which provides shared functionality:

**Features:**
- Custom model fields
- Base classes
- Common utilities

**Configuration:**
- Uses :field:`django.db.models.BigAutoField` for primary keys
"""

from django.apps import AppConfig


class CoreConfig(AppConfig):
    """Configuration for the core app.
    
    **Settings:**
    - default_auto_field: Uses BigAutoField for primary keys
    - name: "core"
    """
    default_auto_field = "django.db.models.BigAutoField"
    name = "core"
