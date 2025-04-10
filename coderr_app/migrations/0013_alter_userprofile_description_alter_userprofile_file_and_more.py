# Generated by Django 5.1.7 on 2025-04-10 07:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coderr_app', '0012_alter_userprofile_description_alter_userprofile_file_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='description',
            field=models.CharField(default='add information', max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='file',
            field=models.ImageField(default='add information', null=True, upload_to='uploads/'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='first_name',
            field=models.CharField(default='add information', max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='last_name',
            field=models.CharField(default='add information', max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='location',
            field=models.CharField(default='add information', max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='tel',
            field=models.CharField(default='add information', max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='working_hours',
            field=models.CharField(default='add information', max_length=24, null=True),
        ),
    ]
