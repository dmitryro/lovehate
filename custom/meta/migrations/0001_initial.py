# Generated by Django 2.0.4 on 2018-04-28 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ContactMetaProp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('address1', models.CharField(max_length=150)),
                ('address2', models.CharField(blank=True, max_length=150, null=True)),
                ('city', models.CharField(max_length=150)),
                ('zip', models.CharField(max_length=20)),
                ('state', models.CharField(max_length=20)),
                ('phone', models.CharField(max_length=20)),
                ('fax', models.CharField(max_length=20)),
                ('hours', models.CharField(max_length=200)),
                ('days', models.CharField(max_length=200)),
                ('note', models.CharField(blank=True, max_length=1500, null=True)),
            ],
            options={
                'verbose_name': 'contact meta property',
                'verbose_name_plural': 'contact meta properties',
            },
        ),
        migrations.CreateModel(
            name='MetaProp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=140)),
                ('keywords', models.CharField(max_length=1600)),
                ('description', models.TextField(max_length=1500)),
                ('author', models.CharField(max_length=140)),
                ('analytics', models.CharField(max_length=60)),
                ('h1header', models.CharField(blank=True, max_length=140, null=True)),
                ('content', models.TextField(blank=True, max_length=1600, null=True)),
            ],
            options={
                'verbose_name': 'seo meta property',
                'verbose_name_plural': 'seo meta properties',
            },
        ),
        migrations.CreateModel(
            name='ProfileMetaProp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=150, null=True)),
                ('email', models.EmailField(max_length=254)),
                ('from_email', models.EmailField(max_length=254)),
                ('to_email', models.EmailField(max_length=254)),
                ('to_email_secondary', models.EmailField(max_length=254)),
                ('to_email_third', models.EmailField(max_length=254)),
                ('smtp_server', models.CharField(max_length=150)),
                ('smtp_port', models.CharField(max_length=10)),
                ('user_name', models.CharField(max_length=200)),
                ('password', models.CharField(max_length=200)),
                ('message', models.CharField(blank=True, max_length=2500, null=True)),
            ],
            options={
                'verbose_name': 'profile meta property',
                'verbose_name_plural': 'profile meta properties',
            },
        ),
    ]
