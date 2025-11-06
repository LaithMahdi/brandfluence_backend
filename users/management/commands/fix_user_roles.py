from django.core.management.base import BaseCommand
from users.models import User


class Command(BaseCommand):
    help = 'Fix EnumMeta.ROLE values in user roles (e.g., EnumMeta.COMPANY → COMPANY)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be fixed without making changes',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        
        if dry_run:
            self.stdout.write(self.style.WARNING('DRY RUN MODE - No changes will be made'))
        
        users_to_fix = User.objects.filter(role__contains='EnumMeta.')
        total_users = users_to_fix.count()
        
        if total_users == 0:
            self.stdout.write(self.style.SUCCESS('No users need fixing. All roles are correct!'))
            return
        
        self.stdout.write(f'Found {total_users} users with EnumMeta roles\n')
        
        fixed_count = 0
        for user in users_to_fix:
            old_role = user.role
            # Extract the role value after 'EnumMeta.'
            role_value = str(user.role).split('.')[-1]
            
            if dry_run:
                self.stdout.write(
                    f'Would fix: {user.email} ({user.id}): {old_role} → {role_value}'
                )
            else:
                user.role = role_value
                user.save(update_fields=['role'])
                self.stdout.write(
                    self.style.SUCCESS(
                        f'✓ Fixed: {user.email} ({user.id}): {old_role} → {role_value}'
                    )
                )
            fixed_count += 1
        
        if dry_run:
            self.stdout.write(
                self.style.WARNING(
                    f'\nDRY RUN: Would fix {fixed_count} users'
                )
            )
            self.stdout.write('Run without --dry-run to apply changes')
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    f'\n✅ Successfully fixed {fixed_count} users'
                )
            )
