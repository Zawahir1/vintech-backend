# Generated by Django 5.0.7 on 2024-08-28 04:25

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("mainapp", "0013_redeems_agent_alter_redeems_cashtag_uuid"),
    ]

    operations = [
        migrations.AddField(
            model_name="cashapps",
            name="activity_status",
            field=models.CharField(default="Active", max_length=10),
            preserve_default=False,
        ),
    ]
