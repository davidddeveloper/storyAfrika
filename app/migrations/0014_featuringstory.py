# Generated by Django 5.1.3 on 2024-12-08 20:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_story_unique_views'),
    ]

    operations = [
        migrations.CreateModel(
            name='FeaturingStory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caption', models.CharField(max_length=50)),
                ('image', models.ImageField(upload_to='')),
                ('status', models.CharField(choices=[('a', 'Active'), ('i', 'Inactive')], default='a', max_length=1)),
                ('story', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='has_featured', to='app.story')),
            ],
        ),
    ]
