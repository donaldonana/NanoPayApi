# Generated by Django 3.1 on 2022-06-30 18:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('NanoPayApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parametrecarte',
            name='MontantPaimentQuotidient',
            field=models.IntegerField(default=10000),
        ),
        migrations.AlterField(
            model_name='parametrecarte',
            name='PaiementQuotidientLimite',
            field=models.IntegerField(default=10),
        ),
    ]
