# Generated by Django 5.0.7 on 2024-08-28 09:13

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("mainapp", "0016_remove_redeems_player_name"),
    ]

    operations = [
        migrations.AddField(
            model_name="redeems",
            name="status",
            field=models.CharField(default="Approved", max_length=100),
            preserve_default=False,
        ),
    ]