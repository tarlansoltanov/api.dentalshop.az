# Generated by Django 5.0.4 on 2024-04-22 19:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': (models.OrderBy(models.F('position'), nulls_last=True), '-created_at'), 'verbose_name': 'Category', 'verbose_name_plural': 'Categories'},
        ),
        migrations.AddField(
            model_name='category',
            name='position',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]