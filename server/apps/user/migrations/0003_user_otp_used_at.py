# Generated by Django 5.0.4 on 2024-04-26 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_user_is_verified_user_otp_code_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='otp_used_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
