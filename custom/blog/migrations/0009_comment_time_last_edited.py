# Generated by Django 2.0.4 on 2018-05-09 20:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_auto_20180507_0741'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='time_last_edited',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
