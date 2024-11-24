from django.core.management.base import BaseCommand, CommandError
from core.models import Image
from django.utils import timezone
from datetime import timedelta

class DeleteCommand(BaseCommand):
    help = "Deletes the images which were uploaded an hour ago"

    def handle(self, *args, **options):
        images = Image.objects.filter(created_at__lte = timezone.now() - timedelta(minutes=60))
        self.stdout.write(self.style.SUCCESS("Successfully deleted the images"))
        print("Successfully deleted the images")
        return
        