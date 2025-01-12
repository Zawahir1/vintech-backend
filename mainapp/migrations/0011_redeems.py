# Generated by Django 5.0.7 on 2024-08-22 21:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("mainapp", "0010_rename_redeem_deposit"),
    ]

    operations = [
        migrations.CreateModel(
            name="Redeems",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("datetime", models.DateTimeField(auto_now_add=True)),
                ("player_name", models.CharField(max_length=100)),
                ("game_user_id", models.CharField(max_length=100)),
                ("page_name", models.CharField(max_length=200)),
                ("amount", models.IntegerField()),
                ("tip", models.IntegerField(default=0)),
                ("added_back", models.IntegerField(default=0)),
                ("paid", models.IntegerField(default=0)),
                ("remaining", models.IntegerField(default=0)),
                ("cashtag_uuid", models.UUIDField()),
                ("comments", models.TextField(blank=True, null=True)),
                (
                    "game",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="mainapp.games"
                    ),
                ),
            ],
        ),
    ]
