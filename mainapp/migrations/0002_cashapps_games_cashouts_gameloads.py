# Generated by Django 5.0.7 on 2024-08-02 12:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("mainapp", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="CashApps",
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
                ("cash_tag", models.IntegerField()),
                ("ownership", models.CharField(max_length=20)),
                ("system", models.CharField(max_length=20)),
                ("status", models.CharField(max_length=20)),
                ("installation_date", models.DateField()),
                ("delivery_email", models.CharField(max_length=50)),
                ("delivery_password", models.CharField(max_length=50)),
                ("delivery_recovery", models.CharField(max_length=100)),
                ("vintech_email", models.CharField(max_length=50)),
                ("vintech_password", models.CharField(max_length=50)),
                ("vintech_recovery", models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="Games",
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
                ("name", models.CharField(max_length=100)),
                ("credentials", models.CharField(max_length=200)),
                ("login_link", models.CharField(max_length=250)),
                ("balance", models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="CashOuts",
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
                ("cashout_date", models.DateField()),
                ("amount", models.IntegerField()),
                ("status", models.CharField(max_length=100)),
                ("owner", models.CharField(max_length=100)),
                ("by", models.CharField(max_length=100)),
                ("comment", models.CharField(max_length=250, null=True)),
                (
                    "cashapp",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="mainapp.cashapps",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="GameLoads",
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
                ("amount", models.IntegerField()),
                (
                    "game",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="mainapp.games"
                    ),
                ),
            ],
        ),
    ]
