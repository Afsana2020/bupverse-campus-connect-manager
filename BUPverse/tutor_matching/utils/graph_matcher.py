# tutor_matching/utils/graphy_matcher_max_ai.py

from functools import lru_cache
from sentence_transformers import SentenceTransformer, util
from tutor_matching.models import nextDoorPost
from core.utils.geo_utils import get_real_distance_km

# Load AI model once
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# Cache embeddings for efficiency
@lru_cache(maxsize=2000)
def cached_encode(text: str):
    return embedding_model.encode(text, convert_to_tensor=True)

def post_to_text(post):
    """
    Convert a post to rich natural language text for AI embeddings.
    Handles 'any' values as neutral placeholders.
    """
    def clean(value, placeholder):
        if not value or str(value).strip().lower() == "any":
            return placeholder
        return str(value).strip()

    parts = []

    user_type = "tutor" if post.user_type == 'looking_tutor' else "student seeking tutor"
    parts.append(user_type)

    parts.append(f"subjects: {clean(post.subjects, 'any subject')}")
    if post.budget:
        parts.append(f"budget: {post.budget} BDT")
    parts.append(f"medium of instruction: {clean(post.medium, 'any medium')}")
    parts.append(f"class level: {clean(post.student_class, 'any class')}")
    parts.append(f"gender preference: {clean(post.gender, 'any gender')}")
    parts.append(f"location: {clean(post.location, 'any location')}")

    return ". ".join(parts)

def location_score(post1, post2):
    """
    Location score based on latitude/longitude.
    Exponential decay for distance similarity.
    """
    if not all([post1.latitude, post1.longitude, post2.latitude, post2.longitude]):
        return 0.5  # neutral if coordinates missing

    distance_km = get_real_distance_km(
        (post1.latitude, post1.longitude),
        (post2.latitude, post2.longitude)
    )

    # Exponential decay: closer -> score closer to 1
    score = max(0.0, min(1.0, 1.0 * (2 ** (-distance_km / 5))))
    return round(score, 3)

def ai_matching(user_post, top_n=10):
    """
    Return top-N AI + location matches using fast batch matrix operations.
    """
  
    if user_post.user_type == 'looking_tutor':
        target_type = 'looking_tutions'
    elif user_post.user_type == 'looking_tutions':
        target_type = 'looking_tutor'
    else:
        return []


    candidates = list(nextDoorPost.objects.filter(user_type=target_type).exclude(user_id=user_post.user_id))

    if not candidates:
        return []

  
    user_text = post_to_text(user_post)
    candidate_texts = [post_to_text(c) for c in candidates]

    
    user_emb = cached_encode(user_text)
    candidate_embs = embedding_model.encode(candidate_texts, convert_to_tensor=True)

   
    ai_scores = util.pytorch_cos_sim(user_emb, candidate_embs)[0].tolist()

    results = []
    for i, candidate in enumerate(candidates):
        ai_sim = round(ai_scores[i], 3)
        loc_sim = location_score(user_post, candidate)
        
      
        hybrid = round(0.7 * ai_sim + 0.3 * loc_sim, 3)
        results.append((hybrid, candidate))

    results.sort(key=lambda x: x[0], reverse=True)
    return results[:top_n]

def choose_method(user_post, top_n=10):
    return ai_matching(user_post, top_n=top_n)