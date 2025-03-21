# Generated by Django 5.1.7 on 2025-03-19 23:44

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Offer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('image', models.ImageField(null=True, upload_to='uploads/')),
                ('description', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OfferDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('revisions', models.IntegerField()),
                ('delivery_time_in_days', models.IntegerField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('features', models.JSONField()),
                ('offer_type', models.CharField(max_length=255)),
                ('offer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='details', to='coderr_app.offer')),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=10)),
                ('username', models.CharField(max_length=64)),
                ('email', models.EmailField(max_length=254)),
                ('first_name', models.CharField(max_length=64, null=True)),
                ('last_name', models.CharField(max_length=64, null=True)),
                ('file', models.ImageField(null=True, upload_to='uploads/')),
                ('location', models.CharField(max_length=64, null=True)),
                ('tel', models.CharField(max_length=64, null=True)),
                ('description', models.CharField(max_length=256, null=True)),
                ('working_hours', models.CharField(max_length=24, null=True)),
                ('created_at', models.DateTimeField(auto_now=True, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
