# Generated by Django 5.0.4 on 2024-06-26 16:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0007_alter_order_created_at_alter_order_updated_at_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ('-created_at',), 'verbose_name': 'Order', 'verbose_name_plural': 'Orders'},
        ),
        migrations.AlterModelOptions(
            name='orderitem',
            options={'ordering': ('-created_at',), 'verbose_name': 'Order Item', 'verbose_name_plural': 'Order Items'},
        ),
        migrations.AlterModelOptions(
            name='orderpayment',
            options={'ordering': ('-created_at',), 'verbose_name': 'Order Payment', 'verbose_name_plural': 'Order Payments'},
        ),
        migrations.RemoveField(
            model_name='order',
            name='date',
        ),
    ]
