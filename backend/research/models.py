from django.db import models

# Create your models here.

class Technology(models.Model):
    """
    Represents a technology that can be researched by an empire.
    Technologies can have prerequisites and belong to different categories.
    """

    class Category(models.TextChoices):
        """Categories of technology that affect different aspects of the empire."""
        RESOURCES = 'RESOURCES', 'Resources'
        INDUSTRY = 'INDUSTRY', 'Industry'
        SCIENCE = 'SCIENCE', 'Science'
        MILITARY = 'MILITARY', 'Military'

    name = models.CharField(
        max_length=100,
        unique=True,
        help_text="The unique name of the technology"
    )
    description = models.TextField(
        help_text="Detailed description of what the technology does"
    )
    category = models.CharField(
        max_length=20,
        choices=Category.choices,
        help_text="The category this technology belongs to"
    )
    prerequisites = models.ManyToManyField(
        'self',
        symmetrical=False,
        blank=True,
        help_text="Technologies that must be researched before this one"
    )

    class Meta:
        app_label = 'research'
        verbose_name_plural = 'Technologies'

    def __str__(self):
        """String representation of the Technology."""
        return f"{self.name} ({self.get_category_display()})"
