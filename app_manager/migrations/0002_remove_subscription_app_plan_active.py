# Generated by Django 4.2.9 on 2024-01-03 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app_manager", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="subscription",
            name="app",
        ),
        migrations.AddField(
            model_name="plan",
            name="active",
            field=models.BooleanField(default=True),
        ),
    ]
