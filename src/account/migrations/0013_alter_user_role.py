# Generated by Django 3.2.6 on 2021-10-31 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0012_alter_user_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('Staff', 'Staff'), ('Manager', 'Manager'), ('Admin', 'Admin')], default='Staff', max_length=15),
        ),
    ]
