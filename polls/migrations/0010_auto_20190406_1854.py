# Generated by Django 2.1.7 on 2019-04-06 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0009_remove_shopcharacteristics_total_count_of_products'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shopcharacteristics',
            name='total_money',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=9),
        ),
        migrations.AlterField(
            model_name='shopcharacteristics',
            name='total_usage_of_coupons',
            field=models.PositiveIntegerField(blank=True, default=0),
        ),
    ]
