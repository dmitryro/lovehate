# Generated by Django 2.0.4 on 2018-05-09 02:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20180504_1555'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='password_recovery_key',
            field=models.CharField(blank=True, default='', max_length=250, null=True),
        ),
    ]