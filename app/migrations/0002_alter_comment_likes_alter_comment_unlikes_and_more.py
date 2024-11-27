# Generated by Django 5.0 on 2024-11-27 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='likes',
            field=models.ManyToManyField(blank=True, null=True, related_name='comment_likes', to='app.profile'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='unlikes',
            field=models.ManyToManyField(blank=True, null=True, related_name='comment_unlikes', to='app.profile'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='bookmarks',
            field=models.ManyToManyField(blank=True, null=True, related_name='bookmarkers', to='app.story'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='followers',
            field=models.ManyToManyField(blank=True, null=True, related_name='following', to='app.profile'),
        ),
        migrations.AlterField(
            model_name='story',
            name='contributors',
            field=models.ManyToManyField(blank=True, null=True, related_name='stories_contributed_to', to='app.profile'),
        ),
        migrations.AlterField(
            model_name='story',
            name='likes',
            field=models.ManyToManyField(blank=True, null=True, related_name='likers', to='app.profile'),
        ),
        migrations.AlterField(
            model_name='story',
            name='topics',
            field=models.ManyToManyField(blank=True, null=True, related_name='stories', to='app.topic'),
        ),
        migrations.AlterField(
            model_name='topic',
            name='contributors',
            field=models.ManyToManyField(blank=True, null=True, related_name='topics_contributed_to', to='app.profile'),
        ),
        migrations.AlterField(
            model_name='topic',
            name='followers',
            field=models.ManyToManyField(blank=True, null=True, related_name='topics_following', to='app.profile'),
        ),
    ]
