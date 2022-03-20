# Generated by Django 3.1 on 2022-03-20 10:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='ParametreCarte',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('paiementVerouiller', models.BooleanField()),
                ('nbrPaiementQuotidientLimite', models.IntegerField()),
                ('MontantPaimentQuotidient', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=255, unique=True)),
                ('nom', models.CharField(max_length=255)),
                ('prenom', models.CharField(blank=True, max_length=255)),
                ('phone', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('dateDeNaissance', models.DateField(blank=True)),
                ('genre', models.CharField(choices=[('masculin', 'Masculin'), ('feminin', 'Feminin')], max_length=25)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dateHeure', models.DateTimeField(default=django.utils.timezone.now)),
                ('montant', models.IntegerField()),
                ('compteEmetteur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='emetteur', to=settings.AUTH_USER_MODEL)),
                ('compteRecepteur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recepteur', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Compte',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numCompte', models.IntegerField(unique=True)),
                ('nomCompte', models.CharField(blank=True, max_length=25)),
                ('principal', models.BooleanField()),
                ('solde', models.IntegerField()),
                ('type', models.CharField(choices=[('entrprise', 'Entreprise'), ('personel', 'Personel')], max_length=25)),
                ('dateCreation', models.DateTimeField(default=django.utils.timezone.now)),
                ('params', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='NanoPayApp.parametrecarte')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
