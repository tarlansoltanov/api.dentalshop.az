# Generated by Django 5.0.4 on 2024-06-24 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('banner', '0002_alter_banner_photo_alter_banner_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='banner',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Created at'),
        ),
        migrations.AlterField(
            model_name='banner',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Updated at'),
        ),
    ]
