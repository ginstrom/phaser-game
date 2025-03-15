from django.db import migrations, models
import core.fields


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='TestModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', core.fields.FixedPointField()),
                ('custom_scale', core.fields.FixedPointField(scale=10000)),
            ],
        ),
    ] 