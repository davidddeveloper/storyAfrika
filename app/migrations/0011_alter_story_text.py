# Generated by Django 5.1.3 on 2024-12-04 17:06

import tinymce.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_alter_story_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='story',
            name='text',
            field=tinymce.models.HTMLField(),
        ),
    ]
