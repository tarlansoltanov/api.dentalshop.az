# Generated by Django 5.0.4 on 2024-05-11 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AppVersionConfiguration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ios', models.CharField(blank=True, max_length=255, verbose_name='IOS Version')),
                ('ios_url', models.URLField(blank=True, verbose_name='IOS App Store URL')),
                ('android', models.CharField(blank=True, max_length=255, verbose_name='Android Version')),
                ('android_url', models.URLField(blank=True, verbose_name='Android Play Store URL')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
