# Generated by Django 5.1 on 2024-09-12 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0017_redeems_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='deposit',
            name='cashtag_uuid',
            field=models.CharField(default=123, max_length=50),
            preserve_default=False,
        ),
    ]
