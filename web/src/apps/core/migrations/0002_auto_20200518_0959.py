# Generated by Django 3.0.6 on 2020-05-18 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='turnaccountmovement',
            name='turn',
        ),
        migrations.RenameField(
            model_name='turn',
            old_name='dice_result',
            new_name='dice',
        ),
        migrations.RemoveField(
            model_name='player',
            name='is_winner',
        ),
        migrations.RemoveField(
            model_name='property',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='turn',
            name='match',
        ),
        migrations.RemoveField(
            model_name='turn',
            name='property',
        ),
        migrations.AddField(
            model_name='simulation',
            name='bonus',
            field=models.DecimalField(decimal_places=2, default=100.0, max_digits=8, verbose_name='bonus'),
        ),
        migrations.AddField(
            model_name='turn',
            name='account_movement',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8, verbose_name='account movement'),
        ),
        migrations.AlterField(
            model_name='simulation',
            name='dice',
            field=models.PositiveSmallIntegerField(default=6, verbose_name='times to run'),
        ),
        migrations.DeleteModel(
            name='Dice',
        ),
        migrations.DeleteModel(
            name='TurnAccountMovement',
        ),
    ]