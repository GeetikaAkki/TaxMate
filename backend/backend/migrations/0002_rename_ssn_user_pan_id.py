# Generated by Django 5.1.2 on 2025-02-08 06:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0001_create_user_model'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='ssn',
            new_name='pan_id',
        ),
    ]
