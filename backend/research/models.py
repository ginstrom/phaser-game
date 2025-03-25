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
    cost = models.IntegerField(
        help_text="Research cost in research points",
        default=100
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


class EmpireTechnology(models.Model):
    """
    Represents an empire's progress in researching a specific technology.
    Tracks the research points invested and whether the technology is complete.
    """

    technology = models.ForeignKey(
        Technology,
        on_delete=models.CASCADE,
        related_name='empire_research',
        help_text="The technology being researched"
    )
    empire = models.ForeignKey(
        'play.Empire',
        on_delete=models.CASCADE,
        related_name='technology_research',
        help_text="The empire researching the technology"
    )
    research_points = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        help_text="Number of research points invested in this technology"
    )

    class Meta:
        app_label = 'research'
        verbose_name_plural = 'Empire Technologies'
        unique_together = ['technology', 'empire']

    def __str__(self):
        """String representation of the EmpireTechnology."""
        return f"{self.empire.name} - {self.technology.name}"

    @property
    def is_complete(self) -> bool:
        """Returns whether the technology has been fully researched."""
        return self.research_points >= self.technology.cost
