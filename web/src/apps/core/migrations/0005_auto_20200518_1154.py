# Generated by Django 3.0.6 on 2020-05-18 11:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_remove_player_account_balance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='simulation',
            name='dice',
            field=models.PositiveSmallIntegerField(default=6, verbose_name='dice'),
        ),
        migrations.CreateModel(
            name='SimulationOutcome',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timed_out_matches', models.PositiveSmallIntegerField(verbose_name='time out matches')),
                ('average_turns', models.PositiveSmallIntegerField(verbose_name='average match turns')),
                ('random_behavior', models.PositiveSmallIntegerField(verbose_name='% random behavior wins')),
                ('conservative_behavior', models.PositiveSmallIntegerField(verbose_name='% conservative behavior wins')),
                ('picky_behavior', models.PositiveSmallIntegerField(verbose_name='% picky behavior wins')),
                ('impulsive_behavior', models.PositiveSmallIntegerField(verbose_name='% impulsive behavior wins')),
                ('simulation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Simulation')),
            ],
            options={
                'verbose_name': 'Simulation outcome',
                'verbose_name_plural': 'Simulations outcomes',
            },
        ),
    ]