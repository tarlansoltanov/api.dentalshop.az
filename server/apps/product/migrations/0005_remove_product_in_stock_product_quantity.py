# Generated by Django 5.0.1 on 2024-04-08 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_alter_product_options_alter_productimage_options'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='in_stock',
        ),
        migrations.AddField(
            model_name='product',
            name='quantity',
            field=models.PositiveIntegerField(default=0),
        ),
    ]