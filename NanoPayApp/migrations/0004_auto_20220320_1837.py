# Generated by Django 3.1 on 2022-03-20 18:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('NanoPayApp', '0003_auto_20220320_1836'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='dateDeNaissance',
            field=models.DateField(blank=True, null=True),
        ),
    ]