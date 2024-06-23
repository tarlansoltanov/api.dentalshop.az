# Generated by Django 5.0.4 on 2024-06-24 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('freezone', '0003_alter_freezoneitem_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='freezoneitem',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Created at'),
        ),
        migrations.AlterField(
            model_name='freezoneitem',
            name='slug',
            field=models.SlugField(max_length=255, unique=True, verbose_name='Slug'),
        ),
        migrations.AlterField(
            model_name='freezoneitem',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Updated at'),
        ),
        migrations.AlterField(
            model_name='freezoneitemimage',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Created at'),
        ),
        migrations.AlterField(
            model_name='freezoneitemimage',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Updated at'),
        ),
    ]
