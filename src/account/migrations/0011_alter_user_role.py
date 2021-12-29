# Generated by Django 3.2.6 on 2021-10-31 17:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0010_alter_user_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('Manager', 'Manager'), ('Admin', 'Admin'), ('Staff', 'Staff')], default='Staff', max_length=15),
        ),
    ]
