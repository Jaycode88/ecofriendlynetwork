# Generated by Django 4.2.9 on 2024-01-16 11:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_favorite_created'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='favorite',
            name='created',
        ),
    ]
