# Generated by Django 3.2.6 on 2021-11-22 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0020_alter_user_role'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='webinfo',
            name='password',
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('Staff', 'Staff'), ('Admin', 'Admin'), ('Manager', 'Manager')], default='Staff', max_length=15),
        ),
        migrations.AlterField(
            model_name='webinfo',
            name='email',
            field=models.EmailField(default='nzafloris@gmail.com', max_length=254, verbose_name='Enter a business email'),
        ),
    ]
