# Generated by Django 5.1.7 on 2025-03-15 07:41

import core.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("celestial", "0002_star"),
    ]

    operations = [
        migrations.CreateModel(
            name="AsteroidBelt",
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
                (
                    "mineral_production",
                    core.fields.FixedPointField(
                        default=50, help_text="Base mineral production per turn"
                    ),
                ),
                (
                    "organic_production",
                    core.fields.FixedPointField(
                        default=50, help_text="Base organic production per turn"
                    ),
                ),
                (
                    "radioactive_production",
                    core.fields.FixedPointField(
                        default=50, help_text="Base radioactive production per turn"
                    ),
                ),
                (
                    "exotic_production",
                    core.fields.FixedPointField(
                        default=50, help_text="Base exotic production per turn"
                    ),
                ),
            ],
        ),
    ]
