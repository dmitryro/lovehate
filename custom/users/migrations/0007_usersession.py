# Generated by Django 2.0.4 on 2018-05-18 17:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0006_profile_password'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserSession',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(blank=True, max_length=200, null=True)),
                ('remote_ip', models.CharField(blank=True, max_length=20, null=True)),
                ('session_key', models.CharField(blank=True, max_length=200, null=True)),
                ('time_in', models.DateTimeField(auto_now_add=True)),
                ('time_out', models.DateTimeField(blank=True, null=True, verbose_name='Time Logged Out')),
                ('time_online_hours', models.IntegerField(blank=True, default=0, null=True)),
                ('time_online_minutes', models.IntegerField(blank=True, default=0, null=True)),
                ('time_online_seconds', models.IntegerField(blank=True, default=0, null=True)),
                ('time_online_total', models.CharField(blank=True, max_length=200, null=True)),
                ('time_online_delta', models.FloatField(blank=True, default=0, null=True)),
                ('date_visited', models.DateField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Session',
                'verbose_name_plural': 'Sessions',
            },
        ),
    ]
