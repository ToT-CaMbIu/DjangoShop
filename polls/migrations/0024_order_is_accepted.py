# Generated by Django 3.0.5 on 2020-11-12 19:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0023_auto_20201110_2207'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='is_accepted',
            field=models.BooleanField(default=False),
        ),
    ]
