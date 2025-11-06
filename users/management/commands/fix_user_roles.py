from django.core.management.base import BaseCommand
from users.models import User
from users.influencer_models import Influencer, ReseauSocial, OffreCollaboration


class Command(BaseCommand):
    help = 'Fix ALL EnumMeta values in database (User roles, Influencer disponibilite, ReseauSocial plateforme/frequence, OffreCollaboration type)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be fixed without making changes',
        )

    def fix_enum_value(self, value):
        """Extract clean enum value from EnumMeta.VALUE"""
        if value and 'EnumMeta.' in str(value):
            return str(value).split('.')[-1]
        return value

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        
        if dry_run:
            self.stdout.write(self.style.WARNING('🔍 DRY RUN MODE - No changes will be made\n'))
        else:
            self.stdout.write(self.style.SUCCESS('🔧 FIXING MODE - Changes will be saved\n'))
        
        total_fixed = 0
        
        # ========== FIX USER ROLES ==========
        self.stdout.write(self.style.WARNING('📌 Checking Users...'))
        users_to_fix = User.objects.filter(role__contains='EnumMeta.')
        user_count = 0
        
        for user in users_to_fix:
            old_role = user.role
            new_role = self.fix_enum_value(old_role)
            
            if dry_run:
                self.stdout.write(f'  Would fix User {user.email}: {old_role} → {new_role}')
            else:
                user.role = new_role
                user.save(update_fields=['role'])
                self.stdout.write(self.style.SUCCESS(f'  ✓ Fixed User {user.email}: {old_role} → {new_role}'))
            user_count += 1
        
        if user_count > 0:
            self.stdout.write(self.style.SUCCESS(f'✅ Users: {user_count} fixed\n'))
            total_fixed += user_count
        else:
            self.stdout.write('✓ Users: All clean!\n')
        
        # ========== FIX INFLUENCER DISPONIBILITE ==========
        self.stdout.write(self.style.WARNING('📌 Checking Influencers...'))
        influencers_to_fix = Influencer.objects.filter(disponibilite_collaboration__contains='EnumMeta.')
        influencer_count = 0
        
        for influencer in influencers_to_fix:
            old_dispo = influencer.disponibilite_collaboration
            new_dispo = self.fix_enum_value(old_dispo)
            
            if dry_run:
                self.stdout.write(f'  Would fix Influencer {influencer.user.email}: {old_dispo} → {new_dispo}')
            else:
                influencer.disponibilite_collaboration = new_dispo
                influencer.save(update_fields=['disponibilite_collaboration'])
                self.stdout.write(self.style.SUCCESS(f'  ✓ Fixed Influencer {influencer.user.email}: {old_dispo} → {new_dispo}'))
            influencer_count += 1
        
        if influencer_count > 0:
            self.stdout.write(self.style.SUCCESS(f'✅ Influencers: {influencer_count} fixed\n'))
            total_fixed += influencer_count
        else:
            self.stdout.write('✓ Influencers: All clean!\n')
        
        # ========== FIX RESEAU SOCIAL ==========
        self.stdout.write(self.style.WARNING('📌 Checking Réseaux Sociaux...'))
        reseaux_to_fix = ReseauSocial.objects.filter(
            plateforme__contains='EnumMeta.'
        ) | ReseauSocial.objects.filter(
            frequence_publication__contains='EnumMeta.'
        )
        reseau_count = 0
        
        for reseau in reseaux_to_fix.distinct():
            changes = []
            
            if 'EnumMeta.' in str(reseau.plateforme):
                old_plateforme = reseau.plateforme
                new_plateforme = self.fix_enum_value(old_plateforme)
                changes.append(f'plateforme: {old_plateforme} → {new_plateforme}')
                if not dry_run:
                    reseau.plateforme = new_plateforme
            
            if 'EnumMeta.' in str(reseau.frequence_publication):
                old_freq = reseau.frequence_publication
                new_freq = self.fix_enum_value(old_freq)
                changes.append(f'frequence: {old_freq} → {new_freq}')
                if not dry_run:
                    reseau.frequence_publication = new_freq
            
            if changes:
                if dry_run:
                    self.stdout.write(f'  Would fix ReseauSocial {reseau.id}: {", ".join(changes)}')
                else:
                    reseau.save()
                    self.stdout.write(self.style.SUCCESS(f'  ✓ Fixed ReseauSocial {reseau.id}: {", ".join(changes)}'))
                reseau_count += 1
        
        if reseau_count > 0:
            self.stdout.write(self.style.SUCCESS(f'✅ Réseaux Sociaux: {reseau_count} fixed\n'))
            total_fixed += reseau_count
        else:
            self.stdout.write('✓ Réseaux Sociaux: All clean!\n')
        
        # ========== FIX OFFRE COLLABORATION ==========
        self.stdout.write(self.style.WARNING('📌 Checking Offres Collaboration...'))
        offres_to_fix = OffreCollaboration.objects.filter(type_collaboration__contains='EnumMeta.')
        offre_count = 0
        
        for offre in offres_to_fix:
            old_type = offre.type_collaboration
            new_type = self.fix_enum_value(old_type)
            
            if dry_run:
                self.stdout.write(f'  Would fix OffreCollaboration {offre.id}: {old_type} → {new_type}')
            else:
                offre.type_collaboration = new_type
                offre.save(update_fields=['type_collaboration'])
                self.stdout.write(self.style.SUCCESS(f'  ✓ Fixed OffreCollaboration {offre.id}: {old_type} → {new_type}'))
            offre_count += 1
        
        if offre_count > 0:
            self.stdout.write(self.style.SUCCESS(f'✅ Offres Collaboration: {offre_count} fixed\n'))
            total_fixed += offre_count
        else:
            self.stdout.write('✓ Offres Collaboration: All clean!\n')
        
        # ========== SUMMARY ==========
        self.stdout.write('=' * 60)
        if total_fixed == 0:
            self.stdout.write(self.style.SUCCESS('🎉 No issues found! All enum values are clean!'))
        elif dry_run:
            self.stdout.write(self.style.WARNING(f'🔍 DRY RUN COMPLETE: Would fix {total_fixed} total records'))
            self.stdout.write('\n💡 Run without --dry-run to apply these changes:')
            self.stdout.write('   python manage.py fix_user_roles')
        else:
            self.stdout.write(self.style.SUCCESS(f'✅ SUCCESS: Fixed {total_fixed} total records!'))
            self.stdout.write('\n💡 You may need to restart your Django server for changes to take effect')
        self.stdout.write('=' * 60)
