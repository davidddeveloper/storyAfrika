# Generated by Django 5.1.3 on 2024-12-08 21:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_featuringstory'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='featuringstory',
            name='image',
        ),
        migrations.AddField(
            model_name='featuringstory',
            name='banner',
            field=models.ImageField(default='something', upload_to='media/'),
        ),
    ]
