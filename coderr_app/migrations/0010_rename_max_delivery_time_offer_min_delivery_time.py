# Generated by Django 5.1.7 on 2025-04-09 09:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('coderr_app', '0009_alter_offer_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='offer',
            old_name='max_delivery_time',
            new_name='min_delivery_time',
        ),
    ]
