# Generated by Django 2.1.7 on 2019-04-06 15:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0008_shopcharacteristics'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shopcharacteristics',
            name='total_count_of_products',
        ),
    ]
