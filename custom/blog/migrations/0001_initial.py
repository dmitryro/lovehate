# Generated by Django 2.0.4 on 2018-05-03 17:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('forum', '0005_auto_20180502_2154'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(blank=True, max_length=250, null=True)),
                ('body', models.TextField(blank=True, null=True)),
                ('time_published', models.DateTimeField(auto_now_add=True)),
                ('rating', models.FloatField(blank=True, default=0, null=True)),
                ('attitude', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='forum.Attitude')),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Emotions',
                'verbose_name': 'Emotion',
            },
        ),
    ]
