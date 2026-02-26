"""
Management command to populate the database with 80+ careers from careers_db.py
Usage: python manage.py import_careers [--clear]

If --clear is passed, it will delete existing careers before importing.
"""
from django.core.management.base import BaseCommand
from django.db import transaction
from apps.careers.models import Career
from ml.careers_db import get_all_careers, get_all_clusters


class Command(BaseCommand):
    help = "Import 80+ careers from the careers database with ability vectors and clusters"

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Delete existing careers before importing",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        if options["clear"]:
            count = Career.objects.count()
            Career.objects.all().delete()
            self.stdout.write(
                self.style.SUCCESS(f"✓ Deleted {count} existing careers")
            )

        careers_data = get_all_careers()
        created = 0
        updated = 0

        for career_data in careers_data:
            career, is_created = Career.objects.update_or_create(
                name=career_data["name"],
                defaults={
                    "description": career_data["description"],
                    "required_skills": career_data["required_skills"],
                    "ability_vector": career_data["ability_vector"],
                    "cluster": career_data["cluster"],
                    "average_salary_range": career_data.get("average_salary_range", ""),
                    "job_growth": career_data.get("job_growth", ""),
                    "required_education": career_data.get("required_education", ""),
                },
            )

            if is_created:
                created += 1
            else:
                updated += 1

            self.stdout.write(
                f"{'✓ Created' if is_created else '✓ Updated'}: {career.name} ({career.cluster})"
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"\n✓ Import complete: {created} created, {updated} updated"
            )
        )

        # Display cluster statistics
        clusters = get_all_clusters()
        self.stdout.write(self.style.SUCCESS("\nCluster Distribution:"))
        for cluster in clusters:
            count = Career.objects.filter(cluster=cluster).count()
            self.stdout.write(f"  • {cluster}: {count} careers")
