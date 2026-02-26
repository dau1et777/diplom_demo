"""Hybrid career recommendation using pretrained embeddings + ability vectors.

This module illustrates a production-ready architecture that satisfies the
requirements listed by the user:

* 80+ career profiles stored in the database with cached text embeddings.
* Use a SentenceTransformer/OpenAI model to obtain semantic vectors for career
  descriptions and user quiz responses (no training from scratch).
* Store career embeddings in a PostgreSQL `vector` column (via `pgvector`) to
  allow fast nearest‑neighbour queries.
* Compute a hybrid score combining embedding similarity and ability score
  matching.
* Enforce a diversity constraint so the final top‑N list does not contain more
  than one item from any single cluster.

SQL/ORM snippets demonstrating usage are included below.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional

try:
    import numpy as np
    from sklearn.metrics.pairwise import cosine_similarity
except ImportError:
    np = None
    cosine_similarity = None

try:
    from sentence_transformers import SentenceTransformer
except ImportError:
    SentenceTransformer = None

from django.db import models
from django.db.models import F

from apps.careers.models import Career

# backward compat: if ml.recommendation_engine or inference are available, use them
try:
    from ml.recommendation_engine import UserFeatureExtractor
except ImportError:
    UserFeatureExtractor = None


@dataclass
class HybridRecommendation:
    career: Career
    score: float  # hybrid score between 0 and 1
    emb_similarity: float
    ability_similarity: float

    def to_dict(self) -> Dict:
        return {
            "career_id": str(self.career.id),
            "career_name": self.career.name,
            "score": round(self.score * 100, 1),
            "embedding_similarity": round(self.emb_similarity * 100, 1),
            "ability_similarity": round(self.ability_similarity * 100, 1),
            "cluster": self.career.cluster,
        }


class HybridRecommendationService:
    """Service object encapsulating the recommendation logic.

    ``alpha`` controls the relative weight of the semantic embedding similarity
    vs. the numeric ability match.  A value of 0.7 means 70% embedding and 30%
    ability.  You can tune this after collecting user feedback.

    ``diversity`` toggles the cluster‑based diversity constraint.  When True the
    method will return at most one career per distinct ``cluster`` value.
    """

    def __init__(self, embedding_model_name: str = "all-MiniLM-L6-v2", alpha: float = 0.7):
        if SentenceTransformer is None:
            raise ImportError(
                "SentenceTransformer not found. Please install: "
                "pip install sentence-transformers. "
                "Falling back to old recommendation system."
            )
        self.alpha = alpha
        self._model = SentenceTransformer(embedding_model_name)
        # calling ``encode`` once, later we cache career vectors in the DB

    # ------------------------------------------------------------------
    # embedding helpers
    # ------------------------------------------------------------------
    def text_to_embedding(self, text: str) -> np.ndarray:
        """Return a *normalized* vector for arbitrary text."""
        vec = self._model.encode(text, convert_to_numpy=True)
        # SentenceTransformer models can optionally return normalized vectors;
        # ensure normalization for cosine computations regardless.
        return vec / np.linalg.norm(vec, axis=-1, keepdims=True)

    def career_embedding(self, career: Career) -> np.ndarray:
        """Fetch the career's cached embedding from the model or raise ValueError."""
        if career.embedding is None:
            raise ValueError(f"Career {career.name} has no embedding cached")
        return np.array(career.embedding, dtype=np.float32)

    def user_embedding(self, quiz_answers: Dict[int, int]) -> np.ndarray:
        """Convert quiz answers to a text summary and then to an embedding.

        We simply serialize the numerical feature vector into a short string;
        the SentenceTransformer model will still pick up the semantic pattern.
        Keeping everything in text means we don't have to retrain any numeric
        encoder when the quiz schema changes.
        """
        features = UserFeatureExtractor.extract_features(quiz_answers)
        # example: "logical_thinking:8.5 creativity:3.0 ..."
        text = " ".join(f"{k}:{v:.1f}" for k, v in features.items())
        return self.text_to_embedding(text)

    # ------------------------------------------------------------------
    # similarity / scoring
    # ------------------------------------------------------------------
    def _ability_similarity(self, user_feat: np.ndarray, career_feat: np.ndarray) -> float:
        # if either vector is empty, fall back to zero similarity
        if user_feat.size == 0 or career_feat.size == 0:
            return 0.0
        return float(cosine_similarity([user_feat], [career_feat])[0][0])

    def _hybrid_score(
        self, emb_sim: float, ability_sim: float
    ) -> float:
        return self.alpha * emb_sim + (1.0 - self.alpha) * ability_sim

    # ------------------------------------------------------------------
    # public API
    # ------------------------------------------------------------------
    def recommend(
        self,
        quiz_answers: Dict[int, int],
        top_n: int = 5,
        diversity: bool = True,
    ) -> List[HybridRecommendation]:
        """Return a ranked list of ``HybridRecommendation`` objects.

        The pipeline is:

        1. compute user embedding and ability vector
        2. fetch all active careers (could be restricted by a prefilter)
        3. score each career via hybrid formula
        4. optionally enforce diversity by cluster
        5. return the top-n items
        """
        user_emb = self.user_embedding(quiz_answers)
        user_feat = np.array(
            list(UserFeatureExtractor.extract_features(quiz_answers).values()),
            dtype=np.float32,
        )

        careers = Career.objects.filter(is_active=True)
        scored: List[HybridRecommendation] = []

        # fetch all embeddings once (avoid N+1)
        for career in careers:
            try:
                emb = self.career_embedding(career)
            except ValueError:
                # skip careers that haven't been embedded yet; a management
                # command should be run periodically to fill them.
                continue
            emb_sim = float(cosine_similarity([user_emb], [emb])[0][0])

            ability_sim = self._ability_similarity(user_feat, np.array(career.ability_vector or [], dtype=np.float32))
            score = self._hybrid_score(emb_sim, ability_sim)
            scored.append(HybridRecommendation(career, score, emb_sim, ability_sim))

        # rank
        scored.sort(key=lambda rec: rec.score, reverse=True)

        if diversity:
            selected: List[HybridRecommendation] = []
            seen_clusters: set = set()
            for rec in scored:
                clu = rec.career.cluster
                if clu and clu in seen_clusters:
                    continue
                selected.append(rec)
                seen_clusters.add(clu)
                if len(selected) >= top_n:
                    break
            return selected

        return scored[:top_n]

    # ------------------------------------------------------------------
    # database/ORM helpers
    # ------------------------------------------------------------------
    def careers_by_embedding(self, user_emb: List[float], limit: int = 100) -> models.QuerySet:
        """Demonstrate how to push the cosine calculation into SQL using pgvector.

        ``user_emb`` must be a Python list/tuple of floats; Postgres/pgvector will
        compute the distance in the query and we sort by it.

        Example usage::

            user_vec = service.user_embedding(answers).tolist()
            qs = service.careers_by_embedding(user_vec, limit=20)
            for career in qs:
                print(career.name, career.embedding_similarity)

        The returned queryset has an extra attribute ``embedding_similarity``
        containing the raw cosine score (higher is more similar).
        """
        # ``CosineDistance`` or ``CosineSimilarity`` expressions are provided by
        # django-pgvector; if you prefer raw SQL you can call
        # ``.extra(select={...})`` instead.
        from pgvector.expressions import CosineSimilarity

        return (
            Career.objects
            .filter(is_active=True)
            .annotate(embedding_similarity=CosineSimilarity("embedding", user_emb))
            .order_by("-embedding_similarity")
            .all()[:limit]
        )


# ---------------------------------------------------------------------------
# simple CLI demonstration (can be removed in production)
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import django

    django.setup()

    service = HybridRecommendationService()
    demo_answers = {i: 8 for i in range(1, 20)}  # pretend high scores
    recs = service.recommend(demo_answers, top_n=5)
    for r in recs:
        print(r.to_dict())
