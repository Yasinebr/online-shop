from django.core.management import BaseCommand
from accounts.models import OtpCode
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Remove all expired otp'

    def handle(self, *args, **options):
        expired_time = datetime.now() - timedelta(minutes=2)
        OtpCode.objects.filter(created__lt=expired_time).delete()
        self.stdout.write('Removed all expired otp')