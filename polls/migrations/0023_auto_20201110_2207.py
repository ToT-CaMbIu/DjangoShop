# Generated by Django 3.0.5 on 2020-11-10 19:07

from django.db import migrations
import phone_field.models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0022_auto_20200911_2100'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='phone',
            field=phone_field.models.PhoneField(blank=True, max_length=31),
        ),
    ]