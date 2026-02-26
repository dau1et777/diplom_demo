from django.db import models
import uuid

# optional: use pgvector for fast vector similarity queries when using Postgres
# install with `pip install django-pgvector` and add 'pgvector' to INSTALLED_APPS
# ``pgvector`` provides a native vector type with cosine operators.
# if the package isn't installed yet we fallback to JSONField, but that
# field doesn't accept the ``dimensions`` keyword which our earlier version
# erroneously passed.
try:
    from pgvector.models import VectorField
    _VECTOR_FIELD_IS_PGVECTOR = True
except ImportError:  # fallback if extension not installed yet
    VectorField = models.JSONField  # store as plain list until pgvector is available
    _VECTOR_FIELD_IS_PGVECTOR = False

from django.contrib.postgres.fields import ArrayField


class Career(models.Model):
    """
    Stores career information and metadata.
    Used for displaying career details in recommendations.
    """
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True, db_index=True)
    description = models.TextField()
    required_skills = models.JSONField(default=list, help_text="List of required skills")
    suitable_for = models.TextField(help_text="Description of suitable candidates")
    average_salary_range = models.CharField(max_length=100, blank=True, help_text="e.g., '$80k - $150k'")
    job_growth = models.CharField(max_length=50, blank=True, help_text="e.g., '12% annual growth'")
    typical_companies = models.JSONField(default=list, help_text="List of typical employers")
    required_education = models.CharField(max_length=255, blank=True, help_text="e.g., 'Bachelor in Computer Science'")
    related_careers = models.JSONField(default=list, help_text="List of related career names")

    # ------------------------------------------------------------------
    # fields for the embedding-based recommender system
    # ------------------------------------------------------------------
    # semantic vector representing the career description+skills; used for
    # fast nearest-neighbor lookup.  Stored in the database so we don't have
    # to recompute it on every API call.  The dimensionality should match the
    # pretrained model that generates it (768 for many SentenceTransformer
    # models).  Using JSONField for broad compatibility;
    # pgvector offers a native vector type with built-in cosine operators.
    embedding = models.JSONField(null=True, blank=True,
                                 help_text="Cached embedding for semantic search (list)")

    # numeric ability vector corresponding to the 15 quiz features used by the
    # hybrid scorer.  Stored as JSON by default (will work with all databases).
    ability_vector = models.JSONField(default=list,
                                help_text="Pre-computed ability scores (15 dims)")

    # cluster label (e.g. 'Tech', 'Business', 'Creative', 'Education') that
    # will be used to enforce diversity in the final ranked list.  Populate
    # manually or derive by offline clustering of the embedding space.
    cluster = models.CharField(max_length=100, blank=True,
                               help_text="High-level category used for diversity")

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Career'
        verbose_name_plural = 'Careers'
    
    def __str__(self):
        return self.name

    # ------------------------------------------------------------------
    # convenience helpers used by the recommendation pipeline
    # ------------------------------------------------------------------
    def compute_embedding(self, model) -> None:
        """Generate a semantic vector for this career using ``model``.

        ``model`` should be a SentenceTransformer (or any object exposing
        ``encode(text, ...)`` returning a numpy array).  We concatenate the
        name, description and required_skills into a single string so changes
        to any of those fields cause a different embedding.

        The result is normalized and written back to ``self.embedding``.
        This method does **not** run on save automatically; it is usually
        called from a management command or signal handler.
        """
        from sentence_transformers import SentenceTransformer
        # build the source text; list concatenation keeps order consistent
        text = " ".join(
            [self.name or "", self.description or ""] +
            (self.required_skills or [])
        )
        vec = model.encode(text, convert_to_numpy=True, normalize_embeddings=True)
        # pgvector wants a list of floats; JSONField can also store the list.
        self.embedding = vec.tolist()
        self.save(update_fields=["embedding"])


class Course(models.Model):
    """
    Stores recommended courses for each career.
    Links courses to careers for career path recommendations.
    """
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    career = models.ForeignKey(Career, on_delete=models.CASCADE, related_name='courses')
    name = models.CharField(max_length=255)
    provider = models.CharField(max_length=255, help_text="e.g., 'Coursera', 'Udemy', 'University Name'")
    url = models.URLField(blank=True)
    description = models.TextField(blank=True)
    duration = models.CharField(max_length=100, blank=True, help_text="e.g., '3 months', '1 year'")
    difficulty_level = models.CharField(
        max_length=20,
        choices=[('beginner', 'Beginner'), ('intermediate', 'Intermediate'), ('advanced', 'Advanced')],
        default='intermediate'
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['career', 'name']
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'
    
    def __str__(self):
        return f"{self.name} ({self.career.name})"


class University(models.Model):
    """
    Stores recommended universities for each career.
    Provides location and program information.
    """
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    career = models.ForeignKey(Career, on_delete=models.CASCADE, related_name='universities')
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    program_name = models.CharField(max_length=255, help_text="e.g., 'Bachelor of Computer Science'")
    url = models.URLField(blank=True)
    ranking = models.IntegerField(blank=True, null=True, help_text="University ranking in this field")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['career', 'ranking']
        verbose_name = 'University'
        verbose_name_plural = 'Universities'
    
    def __str__(self):
        return f"{self.name} - {self.program_name}"
