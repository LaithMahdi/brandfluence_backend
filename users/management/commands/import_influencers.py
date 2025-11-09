import json
from django.core.management.base import BaseCommand
from django.db import transaction
from users.models import User
from users.influencer_models import Influencer, ReseauSocial, InfluencerWork, OffreCollaboration
from category.models import Category
from decimal import Decimal


class Command(BaseCommand):
    help = 'Import influencer accounts from JSON file into the database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--file',
            type=str,
            default='influencer_accounts.json',
            help='Path to the JSON file containing influencer data (default: influencer_accounts.json)',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be imported without making changes',
        )
        parser.add_argument(
            '--update',
            action='store_true',
            help='Update existing users if email already exists',
        )

    def handle(self, *args, **options):
        file_path = options['file']
        dry_run = options['dry_run']
        update_existing = options['update']

        if dry_run:
            self.stdout.write(self.style.WARNING('🔍 DRY RUN MODE - No changes will be made\n'))
        else:
            self.stdout.write(self.style.SUCCESS('📥 IMPORT MODE - Importing influencers...\n'))

        try:
            # Load JSON file
            with open(file_path, 'r', encoding='utf-8') as f:
                influencers_data = json.load(f)
            
            self.stdout.write(self.style.SUCCESS(f'✓ Loaded {len(influencers_data)} influencer(s) from {file_path}\n'))

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'❌ Error: File "{file_path}" not found'))
            return
        except json.JSONDecodeError as e:
            self.stdout.write(self.style.ERROR(f'❌ Error: Invalid JSON format - {str(e)}'))
            return

        # Process each influencer
        success_count = 0
        error_count = 0
        updated_count = 0

        for idx, data in enumerate(influencers_data, 1):
            try:
                self.stdout.write(f'\n{"="*60}')
                self.stdout.write(f'Processing influencer {idx}/{len(influencers_data)}: {data.get("name")}')
                self.stdout.write(f'{"="*60}')
                
                if dry_run:
                    self.stdout.write(self.style.WARNING('  [DRY RUN] Would create/update:'))
                    self.stdout.write(f'    Email: {data.get("email")}')
                    self.stdout.write(f'    Name: {data.get("name")}')
                    self.stdout.write(f'    Role: {data.get("role")}')
                    if 'influencer_profile' in data:
                        profile = data['influencer_profile']
                        self.stdout.write(f'    Instagram: @{profile.get("instagram_username")}')
                        self.stdout.write(f'    Social Networks: {len(profile.get("reseaux_sociaux", []))}')
                        self.stdout.write(f'    Previous Works: {len(profile.get("previous_works", []))}')
                        self.stdout.write(f'    Collaboration Offers: {len(profile.get("offres_collaboration", []))}')
                    success_count += 1
                else:
                    result = self._import_influencer(data, update_existing)
                    if result['updated']:
                        updated_count += 1
                        self.stdout.write(self.style.WARNING(f'  ⚠️  Updated existing user: {data.get("email")}'))
                    else:
                        success_count += 1
                        self.stdout.write(self.style.SUCCESS(f'  ✓ Created new user: {data.get("email")}'))

            except Exception as e:
                error_count += 1
                self.stdout.write(self.style.ERROR(f'  ❌ Error processing {data.get("email", "unknown")}: {str(e)}'))

        # Summary
        self.stdout.write(f'\n{"="*60}')
        self.stdout.write('SUMMARY')
        self.stdout.write(f'{"="*60}')
        
        if dry_run:
            self.stdout.write(self.style.WARNING(f'🔍 DRY RUN COMPLETE'))
            self.stdout.write(f'  Would create: {success_count} influencer(s)')
            self.stdout.write(f'  Errors encountered: {error_count}')
            self.stdout.write('\n💡 Run without --dry-run to apply these changes:')
            self.stdout.write(f'   python manage.py import_influencers --file={file_path}')
        else:
            self.stdout.write(self.style.SUCCESS(f'✅ IMPORT COMPLETE'))
            self.stdout.write(f'  Created: {success_count} influencer(s)')
            self.stdout.write(f'  Updated: {updated_count} influencer(s)')
            self.stdout.write(f'  Errors: {error_count}')
        
        self.stdout.write(f'{"="*60}')

    @transaction.atomic
    def _import_influencer(self, data, update_existing):
        """Import a single influencer with all related data"""
        
        email = data.get('email')
        updated = False

        # Check if user exists
        user_exists = User.objects.filter(email=email).exists()
        
        if user_exists:
            if not update_existing:
                raise ValueError(f'User with email {email} already exists. Use --update to update existing users.')
            user = User.objects.get(email=email)
            updated = True
        else:
            # Create user
            user = User.objects.create_user(
                email=email,
                password=data.get('password', 'DefaultPassword123!'),
                name=data.get('name'),
                phone_number=data.get('phone_number'),
                role=data.get('role', 'INFLUENCER'),
                email_verified=data.get('email_verified', False),
                is_verify_by_admin=data.get('is_verify_by_admin', False),
            )
            self.stdout.write(f'    ✓ Created user: {user.email}')

        # Create or update influencer profile
        if 'influencer_profile' in data:
            profile_data = data['influencer_profile']
            
            influencer, created = Influencer.objects.get_or_create(
                user=user,
                defaults={
                    'instagram_username': profile_data.get('instagram_username'),
                    'pseudo': profile_data.get('pseudo'),
                    'biography': profile_data.get('biography'),
                    'site_web': profile_data.get('site_web'),
                    'localisation': profile_data.get('localisation'),
                    'langues': profile_data.get('langues', []),
                    'centres_interet': profile_data.get('centres_interet', []),
                    'type_contenu': profile_data.get('type_contenu', []),
                    'disponibilite_collaboration': profile_data.get('disponibilite_collaboration', 'disponible'),
                }
            )

            if not created:
                # Update existing influencer
                influencer.instagram_username = profile_data.get('instagram_username')
                influencer.pseudo = profile_data.get('pseudo')
                influencer.biography = profile_data.get('biography')
                influencer.site_web = profile_data.get('site_web')
                influencer.localisation = profile_data.get('localisation')
                influencer.langues = profile_data.get('langues', [])
                influencer.centres_interet = profile_data.get('centres_interet', [])
                influencer.type_contenu = profile_data.get('type_contenu', [])
                influencer.disponibilite_collaboration = profile_data.get('disponibilite_collaboration', 'disponible')
                influencer.save()

            action = 'Updated' if not created else 'Created'
            self.stdout.write(f'    ✓ {action} influencer profile')

            # Add categories
            if 'selected_categories' in profile_data:
                category_names = profile_data['selected_categories']
                categories = []
                for cat_name in category_names:
                    category, _ = Category.objects.get_or_create(
                        name=cat_name,
                        defaults={'description': f'Category: {cat_name}'}
                    )
                    categories.append(category)
                
                influencer.selected_categories.set(categories)
                self.stdout.write(f'    ✓ Added {len(categories)} categories')

            # Create social networks
            if 'reseaux_sociaux' in profile_data:
                # Clear existing if updating
                if not created:
                    ReseauSocial.objects.filter(influencer=influencer).delete()
                
                for reseau_data in profile_data['reseaux_sociaux']:
                    ReseauSocial.objects.create(
                        influencer=influencer,
                        plateforme=reseau_data.get('plateforme'),
                        url_profil=reseau_data.get('url_profil'),
                        nombre_abonnes=reseau_data.get('nombre_abonnes', 0),
                        taux_engagement=reseau_data.get('taux_engagement', 0.0),
                        moyenne_vues=reseau_data.get('moyenne_vues', 0),
                        moyenne_likes=reseau_data.get('moyenne_likes', 0),
                        moyenne_commentaires=reseau_data.get('moyenne_commentaires', 0),
                        frequence_publication=reseau_data.get('frequence_publication', 'hebdomadaire'),
                    )
                self.stdout.write(f'    ✓ Created {len(profile_data["reseaux_sociaux"])} social network(s)')

            # Create previous works
            if 'previous_works' in profile_data:
                # Clear existing if updating
                if not created:
                    InfluencerWork.objects.filter(influencer=influencer).delete()
                
                for work_data in profile_data['previous_works']:
                    InfluencerWork.objects.create(
                        influencer=influencer,
                        brand_name=work_data.get('brand_name'),
                        campaign=work_data.get('campaign'),
                        period=work_data.get('period'),
                        results=work_data.get('results'),
                        publication_link=work_data.get('publication_link'),
                    )
                self.stdout.write(f'    ✓ Created {len(profile_data["previous_works"])} previous work(s)')

            # Create collaboration offers
            if 'offres_collaboration' in profile_data:
                # Clear existing if updating
                if not created:
                    OffreCollaboration.objects.filter(influencer=influencer).delete()
                
                for offre_data in profile_data['offres_collaboration']:
                    OffreCollaboration.objects.create(
                        influencer=influencer,
                        type_collaboration=offre_data.get('type_collaboration'),
                        tarif_minimum=Decimal(str(offre_data.get('tarif_minimum', 0))),
                        tarif_maximum=Decimal(str(offre_data.get('tarif_maximum', 0))),
                        conditions=offre_data.get('conditions'),
                    )
                self.stdout.write(f'    ✓ Created {len(profile_data["offres_collaboration"])} collaboration offer(s)')

        return {'updated': updated}
