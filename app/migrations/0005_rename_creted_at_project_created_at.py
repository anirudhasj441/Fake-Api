# Generated by Django 3.2.2 on 2021-07-23 02:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_project_creted_at'),
    ]

    operations = [
        migrations.RenameField(
            model_name='project',
            old_name='creted_at',
            new_name='created_at',
        ),
    ]
