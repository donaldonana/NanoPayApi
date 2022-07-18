# Generated by Django 3.1 on 2022-07-17 11:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Comptes', '0002_auto_20220717_0922'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='WaitingTransactions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('Paiement', 'Paiement'), ('Transfert', 'Transfert'), ('Facture', 'Facture')], default='depense', max_length=25)),
                ('DateTransaction', models.DateTimeField(default=django.utils.timezone.now)),
                ('montant', models.IntegerField()),
                ('receiverPhone', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, to_field='phone')),
                ('senderNumCompte', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Comptes.compte')),
                ('senderPhone', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Waitsender', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('Paiement', 'Paiement'), ('Transfert', 'Transfert'), ('Facture', 'Facture')], default='depense', max_length=25)),
                ('DateTransaction', models.DateTimeField(default=django.utils.timezone.now)),
                ('montant', models.IntegerField()),
                ('receiverPhone', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, to_field='phone')),
                ('senderNumCompte', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Comptes.compte')),
                ('senderPhone', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sender', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]