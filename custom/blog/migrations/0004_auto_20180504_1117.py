# Generated by Django 2.0.4 on 2018-05-04 16:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20180504_1041'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='link_five',
            field=models.CharField(blank=True, max_length=1850, null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='link_four',
            field=models.CharField(blank=True, max_length=1850, null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='link_three',
            field=models.CharField(blank=True, max_length=1850, null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='link_two',
            field=models.CharField(blank=True, max_length=1850, null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='link',
            field=models.CharField(blank=True, max_length=1850, null=True),
        ),
    ]