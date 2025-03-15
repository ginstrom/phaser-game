from django.db import models

# Create your models here.

class Player(models.Model):
    class PlayerType(models.TextChoices):
        HUMAN = 'human', 'Human'
        COMPUTER = 'computer', 'Computer'

    player_type = models.CharField(
        max_length=10,
        choices=PlayerType.choices,
        default=PlayerType.HUMAN,
    )

    def __str__(self):
        return f"{self.player_type} player ({self.id})"

    class Meta:
        app_label = 'play'
