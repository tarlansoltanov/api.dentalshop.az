# Generated by Django 5.0.4 on 2024-06-22 11:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0006_alter_orderitem_options_alter_orderpayment_options_and_more'),
        ('promo', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='promousage',
            options={'verbose_name': 'Promo Usage', 'verbose_name_plural': 'Promo Usages'},
        ),
        migrations.AlterField(
            model_name='promo',
            name='code',
            field=models.CharField(max_length=255, unique=True, verbose_name='Code'),
        ),
        migrations.AlterField(
            model_name='promo',
            name='discount',
            field=models.PositiveIntegerField(default=0, verbose_name='Discount'),
        ),
        migrations.AlterField(
            model_name='promo',
            name='end',
            field=models.DateField(verbose_name='End Date'),
        ),
        migrations.AlterField(
            model_name='promo',
            name='start',
            field=models.DateField(verbose_name='Start Date'),
        ),
        migrations.AlterField(
            model_name='promousage',
            name='order',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='promo', to='order.order', verbose_name='Order'),
        ),
        migrations.AlterField(
            model_name='promousage',
            name='promo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='usages', to='promo.promo', verbose_name='Promo'),
        ),
    ]
