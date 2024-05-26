# Generated by Django 5.0.4 on 2024-05-26 20:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_remove_order_products_alter_order_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='payment_method',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Qapıda ödəniş'), (2, 'Kartla ödəniş'), (3, 'Borclu ödəniş')]),
        ),
    ]
