# Generated by Django 5.0.7 on 2024-07-15 09:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('countries', '0003_alter_country_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='country',
            name='flag',
            field=models.CharField(blank=True, max_length=300),
        ),
    ]
