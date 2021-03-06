# Generated by Django 2.0.4 on 2018-05-18 01:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('forum', '0007_emotion_time_last_edited'),
    ]

    operations = [
        migrations.CreateModel(
            name='MessageRule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rule', models.CharField(blank=True, max_length=250, null=True)),
                ('code', models.CharField(blank=True, max_length=15, null=True)),
            ],
            options={
                'verbose_name_plural': 'Message Rules',
                'verbose_name': 'Message Rule',
            },
        ),
        migrations.CreateModel(
            name='MessageSettings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('duplicate_to_email', models.NullBooleanField(default=False)),
                ('message_rule', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='message_rule', to='forum.MessageRule')),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='owner', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
