# Generated by Django 5.1.7 on 2025-03-20 16:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('coderr_app', '0002_offer_max_delivery_time_offer_min_price'),
    ]

    operations = [
        migrations.RenameField(
            model_name='offer',
            old_name='user',
            new_name='creator_id',
        ),
    ]
