# Generated by Django 4.2 on 2025-03-01 19:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userrole', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('admin', 'Admin'), ('user', 'User')], default='user', max_length=20),
        ),
    ]
