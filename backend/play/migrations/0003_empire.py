# Generated by Django 5.1.7 on 2025-03-15 15:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "celestial",
            "0005_alter_asteroidbelt_orbit_alter_planet_orbit_system_and_more",
        ),
        ("play", "0002_race"),
    ]

    operations = [
        migrations.CreateModel(
            name="Empire",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("mineral_storage", models.IntegerField(default=0)),
                ("organic_storage", models.IntegerField(default=0)),
                ("radioactive_storage", models.IntegerField(default=0)),
                ("exotic_storage", models.IntegerField(default=0)),
                (
                    "asteroid_belts",
                    models.ManyToManyField(
                        blank=True, related_name="empire", to="celestial.asteroidbelt"
                    ),
                ),
                (
                    "planets",
                    models.ManyToManyField(
                        blank=True, related_name="empire", to="celestial.planet"
                    ),
                ),
                (
                    "player",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="empires",
                        to="play.player",
                    ),
                ),
                (
                    "race",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="empires",
                        to="play.race",
                    ),
                ),
            ],
        ),
    ]
