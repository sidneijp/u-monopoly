# Generated by Django 3.0.6 on 2020-05-18 10:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_remove_property_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='player',
            name='account_balance',
        ),
    ]
