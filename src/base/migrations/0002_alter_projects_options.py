# Generated by Django 3.2.6 on 2021-10-11 19:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='projects',
            options={'ordering': ['-date_created'], 'verbose_name_plural': 'Projects'},
        ),
    ]
