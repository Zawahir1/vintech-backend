# Generated by Django 5.0.7 on 2024-08-17 12:33

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("mainapp", "0004_alter_users_options_alter_users_managers_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="users",
            name="salary",
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="users",
            name="shift",
            field=models.CharField(default="Morning", max_length=50),
        ),
        migrations.AlterField(
            model_name="users",
            name="type",
            field=models.CharField(default="Agent", max_length=50),
        ),
    ]
