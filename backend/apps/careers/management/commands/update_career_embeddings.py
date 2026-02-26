from django.core.management.base import BaseCommand
from sentence_transformers import SentenceTransformer
from apps.careers.models import Career


class Command(BaseCommand):
    help = (
        "Compute or refresh semantic embeddings for all active careers. "
        "Embeddings are persisted in the ``Career.embedding`` VectorField so "
        "they can be used directly in SQL/ORM similarity queries."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--model",
            type=str,
            default="all-MiniLM-L6-v2",
            help="Name of the SentenceTransformer model to use (must be installed).",
        )
        parser.add_argument(
            "--force",
            action="store_true",
            help="Recompute embeddings even if the field is already populated.",
        )

    def handle(self, *args, **options):
        model_name = options["model"]
        force = options["force"]

        self.stdout.write(f"Loading embedding model: {model_name}")
        model = SentenceTransformer(model_name)

        qs = Career.objects.filter(is_active=True)
        if not force:
            qs = qs.filter(embedding__isnull=True)  # only those missing a vector

        total = qs.count()
        self.stdout.write(f"Computing embeddings for {total} careers...")

        for idx, career in enumerate(qs.iterator(), start=1):
            self.stdout.write(f"[{idx}/{total}] {career.name}")
            try:
                career.compute_embedding(model)
            except Exception as exc:
                self.stderr.write(f"failed for {career.name}: {exc}")

        self.stdout.write(self.style.SUCCESS("Embedding update complete."))
