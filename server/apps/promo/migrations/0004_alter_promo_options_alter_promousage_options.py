# Generated by Django 5.0.4 on 2024-06-26 14:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('promo', '0003_alter_promo_created_at_alter_promo_updated_at_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='promo',
            options={'ordering': ('-created_at',), 'verbose_name': 'Promo', 'verbose_name_plural': 'Promos'},
        ),
        migrations.AlterModelOptions(
            name='promousage',
            options={'ordering': ('-created_at',), 'verbose_name': 'Promo Usage', 'verbose_name_plural': 'Promo Usages'},
        ),
    ]
