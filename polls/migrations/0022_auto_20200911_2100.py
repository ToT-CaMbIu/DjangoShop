# Generated by Django 3.0.5 on 2020-09-11 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0021_product_count_in_stock'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='count_in_stock',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
