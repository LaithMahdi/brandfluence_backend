import json
import os
from django.core.management.base import BaseCommand
from category.models import Category


class Command(BaseCommand):
    help = 'Populate category table with initial data if table is empty'

    def handle(self, *args, **options):
        # Check if category table is empty
        if Category.objects.exists():
            self.stdout.write(
                self.style.WARNING('Category table already has data. Skipping initialization.')
            )
            return

        # Get the path to the JSON file
        json_file_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))),
            'category_niches.json'
        )

        # Check if JSON file exists
        if not os.path.exists(json_file_path):
            self.stdout.write(
                self.style.ERROR(f'JSON file not found at: {json_file_path}')
            )
            return

        # Read and parse JSON file
        try:
            with open(json_file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
        except json.JSONDecodeError as e:
            self.stdout.write(
                self.style.ERROR(f'Error parsing JSON file: {str(e)}')
            )
            return
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error reading JSON file: {str(e)}')
            )
            return

        # Create categories
        categories_created = 0
        categories = data.get('categories', [])

        for category_data in categories:
            try:
                Category.objects.create(
                    name=category_data['name'],
                    description=category_data.get('description', ''),
                    is_active=True
                )
                categories_created += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created category: {category_data["name"]}')
                )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'Error creating category {category_data["name"]}: {str(e)}')
                )

        self.stdout.write(
            self.style.SUCCESS(f'\nSuccessfully created {categories_created} categories!')
        )
