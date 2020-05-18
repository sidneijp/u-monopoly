# Generated by Django 3.0.6 on 2020-05-18 18:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20200518_1154'),
    ]

    operations = [
        migrations.AlterField(
            model_name='simulationoutcome',
            name='conservative_behavior',
            field=models.DecimalField(decimal_places=2, max_digits=5, verbose_name='% conservative behavior wins'),
        ),
        migrations.AlterField(
            model_name='simulationoutcome',
            name='impulsive_behavior',
            field=models.DecimalField(decimal_places=2, max_digits=5, verbose_name='% impulsive behavior wins'),
        ),
        migrations.AlterField(
            model_name='simulationoutcome',
            name='picky_behavior',
            field=models.DecimalField(decimal_places=2, max_digits=5, verbose_name='% picky behavior wins'),
        ),
        migrations.AlterField(
            model_name='simulationoutcome',
            name='random_behavior',
            field=models.DecimalField(decimal_places=2, max_digits=5, verbose_name='% random behavior wins'),
        ),
    ]
