# Generated by Django 3.2 on 2023-06-23 15:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_alter_user_username'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='user',
            name='unique_registry',
        ),
    ]
