from django.db import models
from .base_model import Base
from ckeditor_uploader.fields import RichTextUploadingField
from tinymce.models import HTMLField

STATUS_CHOICES = {
    "d": "Draft",
    "p": "Published",
    "w": "Withdrawn",
}

class Story(Base):
    """ Represents a story
    """
    
    title = models.CharField(max_length=200, null=False)
    #text = RichTextUploadingField()
    #text = models.TextField(max_length=5000, null=False)
    text = HTMLField()
    writer = models.ForeignKey(to='Profile', on_delete=models.CASCADE, null=False, related_name='stories')
    topics = models.ManyToManyField(to='Topic', blank=True, related_name='stories')

    contributors = models.ManyToManyField(to='Profile', blank=True, related_name='stories_contributed_to')

    likes = models.ManyToManyField(to='Profile', blank=True, related_name='likers')

    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default="d")

    def get_related_stories(self, max_results=10):
        """Retrieve related stories with unique writers."""

        # Stories sharing topics
        topic_related = Story.objects.filter(
            topics__in=self.topics.all()
        ).exclude(id=self.id)

        # Stories with shared contributors
        contributor_related = Story.objects.filter(
            contributors__in=self.contributors.all()
        ).exclude(id=self.id)

        # Combine the results
        combined_stories = topic_related.union(contributor_related)

        # Filter unique writers
        unique_stories = {}
        for story in combined_stories[:max_results]:
            if story.writer_id not in unique_stories:
                unique_stories[story.writer_id] = story

        # Return the unique stories limited by max_results
        return list(unique_stories.values())[:max_results]

    def get_other_stories_by_writer(self, max_results=10):
        """Retrieve other stories written by the same writer, excluding the current story."""
        return Story.objects.filter(
            writer=self.writer
        ).exclude(id=self.id).order_by('-id')[:max_results]
    
    def get_similar_writers(self, max_results=10):
        """Retrieve similar writers based on shared topics or contributors."""
        # Writers sharing topics
        from . import Topic, Profile
        topic_ids = Topic.objects.filter(
            stories__writer=self.writer
        ).values_list('id', flat=True)

        similar_writers_by_topics = Profile.objects.filter(
            stories__topics__id__in=topic_ids
        ).exclude(id=self.writer.id).distinct()

        # Writers sharing contributors
        contributor_ids = Profile.objects.filter(
            stories_contributed_to__writer=self.writer
        ).values_list('id', flat=True)

        similar_writers_by_contributors = Profile.objects.filter(
            stories_contributed_to__id__in=contributor_ids
        ).exclude(id=self.writer.id).distinct()

        # Combine and ensure uniqueness
        similar_writers = (
            similar_writers_by_topics | similar_writers_by_contributors
        ).distinct()[:max_results]

        return similar_writers

    def __str__(self):
        return self.title


class StoryImage(models.Model):
    """ Represents an image for a story """
    story = models.ForeignKey(
        Story, on_delete=models.CASCADE, related_name='images'
    )
    image = models.ImageField(upload_to='media/')

    def __str__(self):
        return f"Image for {self.story.title}"