# Generated by Django 5.1.2 on 2024-12-16 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0007_textdetailing"),
    ]

    operations = [
        migrations.AddField(
            model_name="audiosaving",
            name="is_extracted",
            field=models.BooleanField(default=False),
        ),
    ]