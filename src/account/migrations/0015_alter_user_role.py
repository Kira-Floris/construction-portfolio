# Generated by Django 3.2.6 on 2021-10-31 17:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0014_alter_user_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('Staff', 'Staff'), ('Admin', 'Admin'), ('Manager', 'Manager')], default='Staff', max_length=15),
        ),
    ]