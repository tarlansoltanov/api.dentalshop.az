# Generated by Django 5.0.1 on 2024-03-01 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='message_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
