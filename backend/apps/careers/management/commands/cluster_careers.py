"""
Management command to perform k-means clustering on careers
Uses either embeddings (if available) or ability_vectors for clustering

Usage: python manage.py cluster_careers [--n_clusters 8] [--use_embeddings] [--force_recompute]
"""
import json
import numpy as np
from django.core.management.base import BaseCommand
from django.db import transaction
from sklearn.cluster import KMeans
from apps.careers.models import Career


class Command(BaseCommand):
    help = "Run k-means clustering on careers using embeddings or ability vectors"

    def add_arguments(self, parser):
        parser.add_argument(
            "--n_clusters",
            type=int,
            default=8,
            help="Number of clusters (default: 8)",
        )
        parser.add_argument(
            "--use_embeddings",
            action="store_true",
            help="Use embeddings if available, fall back to ability_vectors",
        )
        parser.add_argument(
            "--force_recompute",
            action="store_true",
            help="Force recompute even if clusters already exist",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        n_clusters = options["n_clusters"]
        use_embeddings = options["use_embeddings"]
        force_recompute = options["force_recompute"]

        # Get all careers
        careers = Career.objects.all()
        if not careers.exists():
            self.stdout.write(
                self.style.ERROR("✗ No careers found. Run 'python manage.py import_careers' first.")
            )
            return

        self.stdout.write(f"Loading {careers.count()} careers for clustering...")

        # Prepare feature vectors
        feature_vectors = []
        career_list = []
        
        for career in careers:
            if use_embeddings and career.embedding:
                try:
                    # Use embeddings if requested and available
                    vec = np.array(career.embedding)
                    feature_vectors.append(vec)
                    career_list.append(career)
                except (TypeError, ValueError):
                    pass
            elif career.ability_vector:
                try:
                    # Fall back to ability vectors
                    vec = np.array(career.ability_vector)
                    feature_vectors.append(vec)
                    career_list.append(career)
                except (TypeError, ValueError):
                    pass

        if not feature_vectors:
            self.stdout.write(
                self.style.ERROR(
                    f"✗ No valid vectors found. Please ensure careers have ability_vectors or embeddings."
                )
            )
            return

        feature_vectors = np.array(feature_vectors)
        self.stdout.write(
            f"✓ Loaded {len(feature_vectors)} feature vectors (dimension: {feature_vectors.shape[1]})"
        )

        # Perform k-means clustering
        self.stdout.write(f"\nRunning k-means with {n_clusters} clusters...")
        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        labels = kmeans.fit_predict(feature_vectors)

        self.stdout.write("✓ K-means clustering complete")

        # Map cluster labels to career names
        cluster_mapping = {}
        default_clusters = [
            "Technology",
            "Business",
            "Creative",
            "Healthcare",
            "Education",
            "Finance",
            "Engineering",
            "Administrative",
            "Marketing",
            "Operations",
        ]

        for idx, career in enumerate(career_list):
            cluster_label = labels[idx]
            
            # Use predefined cluster names or create generic ones
            if cluster_label < len(default_clusters):
                cluster_name = default_clusters[cluster_label]
            else:
                cluster_name = f"Cluster_{cluster_label}"
            
            career.cluster = cluster_name
            career.save()
            
            if cluster_name not in cluster_mapping:
                cluster_mapping[cluster_name] = []
            cluster_mapping[cluster_name].append(career.name)

        # Display results
        self.stdout.write(self.style.SUCCESS("\n✓ Clustering complete! Results:"))
        for cluster_name in sorted(cluster_mapping.keys()):
            careers_in_cluster = cluster_mapping[cluster_name]
            self.stdout.write(f"\n{cluster_name} ({len(careers_in_cluster)} careers):")
            for career_name in sorted(careers_in_cluster):
                self.stdout.write(f"  • {career_name}")

        self.stdout.write(
            self.style.SUCCESS(
                f"\n✓ Updated {len(career_list)} careers with cluster assignments"
            )
        )
