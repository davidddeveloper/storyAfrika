"""
Django management command to clear demo data from StoryAfrika.
Run with: python manage.py clear_demo_data
"""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from stories.models import Story
from taxonomy.models import Country, Category, Theme, Era
from editorial.models import FeaturedStory, ContentGuideline

User = get_user_model()


class Command(BaseCommand):
    help = 'Clears all demo data from the database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--confirm',
            action='store_true',
            help='Confirm deletion without prompting',
        )

    def handle(self, *args, **options):
        if not options['confirm']:
            self.stdout.write(self.style.WARNING(
                'This will delete ALL demo data from the database.'
            ))
            confirmation = input('Are you sure you want to continue? (yes/no): ')

            if confirmation.lower() != 'yes':
                self.stdout.write(self.style.ERROR('Operation cancelled.'))
                return

        self.stdout.write(self.style.WARNING('Clearing demo data...'))

        # Delete in order (respecting foreign keys)
        deleted_counts = {}

        # Featured stories
        count = FeaturedStory.objects.all().delete()[0]
        deleted_counts['Featured Stories'] = count

        # Stories
        count = Story.objects.all().delete()[0]
        deleted_counts['Stories'] = count

        # Content Guidelines
        count = ContentGuideline.objects.all().delete()[0]
        deleted_counts['Content Guidelines'] = count

        # Taxonomy
        count = Country.objects.all().delete()[0]
        deleted_counts['Countries'] = count

        count = Category.objects.all().delete()[0]
        deleted_counts['Categories'] = count

        count = Theme.objects.all().delete()[0]
        deleted_counts['Themes'] = count

        count = Era.objects.all().delete()[0]
        deleted_counts['Eras'] = count

        # Demo users (keep superusers)
        demo_emails = [
            'kwame@storyafrika.com',
            'amara@storyafrika.com',
            'zola@storyafrika.com',
            'fatima@storyafrika.com',
        ]
        count = User.objects.filter(email__in=demo_emails).delete()[0]
        deleted_counts['Demo Users'] = count

        self.stdout.write(self.style.SUCCESS('\n✓ Demo data cleared successfully!\n'))

        for model, count in deleted_counts.items():
            if count > 0:
                self.stdout.write(f'  - Deleted {count} {model}')

        self.stdout.write(self.style.WARNING('\nYou can re-seed demo data with: python manage.py seed_demo_data'))
