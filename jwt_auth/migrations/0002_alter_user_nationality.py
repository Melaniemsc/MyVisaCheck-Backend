# Generated by Django 5.0.6 on 2024-07-08 22:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('countries', '0001_initial'),
        ('jwt_auth', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='nationality',
            field=models.ManyToManyField(blank=True, related_name='users', to='countries.country'),
        ),
    ]
