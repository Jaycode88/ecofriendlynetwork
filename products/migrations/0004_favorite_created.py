# Generated by Django 4.2.9 on 2024-01-08 17:48

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_favorite'),
    ]

    operations = [
        migrations.AddField(
            model_name='favorite',
            name='created',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
