from django.core.management.base import BaseCommand
from django.utils import timezone
from users.models import VerifyToken, PasswordResetToken


class Command(BaseCommand):
    help = 'Delete expired verification tokens and password reset tokens'

    def add_arguments(self, parser):
        parser.add_argument(
            '--days',
            type=int,
            default=0,
            help='Also delete tokens older than X days (even if not expired). Default: 0 (only delete expired)',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be deleted without actually deleting',
        )

    def handle(self, *args, **options):
        now = timezone.now()
        days = options['days']
        dry_run = options['dry_run']

        # Query for expired verification tokens
        verify_tokens_query = VerifyToken.objects.filter(expires_at__lt=now)
        
        # Query for expired password reset tokens
        reset_tokens_query = PasswordResetToken.objects.filter(expires_at__lt=now)

        # If days parameter is provided, also include old tokens
        if days > 0:
            cutoff_date = now - timezone.timedelta(days=days)
            verify_tokens_query = verify_tokens_query | VerifyToken.objects.filter(created_at__lt=cutoff_date)
            reset_tokens_query = reset_tokens_query | PasswordResetToken.objects.filter(created_at__lt=cutoff_date)

        # Count tokens to be deleted
        verify_count = verify_tokens_query.count()
        reset_count = reset_tokens_query.count()

        if dry_run:
            self.stdout.write(
                self.style.WARNING(f'[DRY RUN] Would delete:')
            )
            self.stdout.write(f'  - {verify_count} expired verification tokens')
            self.stdout.write(f'  - {reset_count} expired password reset tokens')
            self.stdout.write(f'  - Total: {verify_count + reset_count} tokens')
            return

        # Delete expired tokens
        verify_deleted = verify_tokens_query.delete()[0]
        reset_deleted = reset_tokens_query.delete()[0]

        # Display results
        self.stdout.write(
            self.style.SUCCESS(f'Successfully deleted expired tokens:')
        )
        self.stdout.write(f'  > {verify_deleted} verification tokens')
        self.stdout.write(f'  > {reset_deleted} password reset tokens')
        self.stdout.write(f'  > Total: {verify_deleted + reset_deleted} tokens')

        # Show statistics
        remaining_verify = VerifyToken.objects.count()
        remaining_reset = PasswordResetToken.objects.count()
        
        self.stdout.write('\nRemaining tokens:')
        self.stdout.write(f'  - {remaining_verify} verification tokens')
        self.stdout.write(f'  - {remaining_reset} password reset tokens')
