# Generated by Django 4.2.11 on 2024-03-26 02:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campgrounds', '0002_rename_name_campground_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='campground',
            name='image',
            field=models.JSONField(blank=True, null=True),
        ),
    ]