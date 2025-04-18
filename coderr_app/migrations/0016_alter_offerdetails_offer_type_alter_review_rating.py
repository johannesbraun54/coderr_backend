# Generated by Django 5.1.7 on 2025-04-19 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coderr_app', '0015_alter_offerdetails_offer_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offerdetails',
            name='offer_type',
            field=models.CharField(choices=[('basic', 'Basic'), ('standard', 'Standard'), ('premium', 'Premium')], max_length=255),
        ),
        migrations.AlterField(
            model_name='review',
            name='rating',
            field=models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)]),
        ),
    ]
