# Generated by Django 5.0.1 on 2024-04-07 14:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_product_discount_end_date'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ('-created_at',), 'verbose_name': 'Product', 'verbose_name_plural': 'Products'},
        ),
        migrations.AlterModelOptions(
            name='productimage',
            options={'ordering': ('created_at',), 'verbose_name': 'ProductImage', 'verbose_name_plural': 'ProductImages'},
        ),
    ]
