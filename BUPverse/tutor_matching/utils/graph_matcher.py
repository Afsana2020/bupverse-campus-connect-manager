from django.conf import settings
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from core.utils.geo_utils import get_real_distance_km
import heapq


def subject_similarity(subj1, subj2):
        subjects1 = set(map(str.strip, subj1.lower().split(',')))
        subjects2 = set(map(str.strip, subj2.lower().split(',')))

        if not subjects1 & subjects2:
            return 0.0  

        vectorizer = TfidfVectorizer().fit_transform([subj1.lower(), subj2.lower()])
        vectors = vectorizer.toarray()
        sim = cosine_similarity([vectors[0]], [vectors[1]])[0][0]
        return sim
#student
def compute_edge_weight(p1, p2):
    similarity = 0

    subject_sim = subject_similarity(p1.subjects, p2.subjects)
    similarity += subject_sim * 30

    if p1.medium == p2.medium:
        similarity += 10

    if abs(p1.budget - p2.budget) <= 1000:
        similarity += 15

    if p1.student_class == p2.student_class:
        similarity += 5

    if p1.gender == p2.gender:
        similarity += 5

    if p1.latitude and p1.longitude and p2.latitude and p2.longitude:
        distance = get_real_distance_km(
            (p1.latitude, p1.longitude),  
            (p2.latitude, p2.longitude)
        )
        if distance < 2:
            similarity += 25
        elif distance < 5:
            similarity += 15
        elif distance < 10:
            similarity += 10
        elif distance < 15:
            similarity += 5
        else:
            similarity += 0
        

    return 100 - similarity  

def budget_bonus(user_budget, student_budget):
    if student_budget is None or user_budget is None:
        return 0
    
    diff = student_budget - user_budget
    
    if diff >= 0:
        # more or equal: full
        return student_budget
    else:
        # less: reduce 
        ratio = max(0, 1 + (diff / user_budget))  
        return student_budget * ratio
    
#tutor
def compute_edge_weight_dijkstra(user_post, candidate_post):

    distance = get_real_distance_km(
        (user_post.latitude, user_post.longitude),
        (candidate_post.latitude, candidate_post.longitude)
    )
    
    bonus = budget_bonus(user_post.budget, candidate_post.budget)
    weight = (distance ** 2) * 100 - bonus
    
    return weight


def dijkstra_matching(user_post, weight_func, top_n=10):
    from tutor_matching.models import nextDoorPost

    if user_post.user_type == 'looking_tutor':
        candidates = list(nextDoorPost.objects.filter(user_type='looking_tutions'))
    elif user_post.user_type == 'looking_tutions':
        candidates = list(nextDoorPost.objects.filter(user_type='looking_tutor'))
    else:
        return []

    graph = {user_post.id: []}
    post_lookup = {user_post.id: user_post}

    for candidate in candidates:
        if not all([user_post.latitude, user_post.longitude, candidate.latitude, candidate.longitude]):
            continue

        weight = weight_func(user_post, candidate)

        graph[user_post.id].append((candidate.id, weight))
        post_lookup[candidate.id] = candidate

    distance_map = {user_post.id: 0}
    heap = [(0, user_post.id)]  # (distance, node_id)
    visited = set()

    while heap:
        current_dist, current_id = heapq.heappop(heap)

        if current_id in visited:
            continue
        visited.add(current_id)

        for neighbor_id, edge_weight in graph.get(current_id, []):
            new_dist = current_dist + edge_weight
            if neighbor_id not in distance_map or new_dist < distance_map[neighbor_id]:
                distance_map[neighbor_id] = new_dist
                heapq.heappush(heap, (new_dist, neighbor_id))

    results = []
    for node_id, dist in distance_map.items():
        if node_id == user_post.id:
            continue
        similarity = 1 / (1 + dist)
        results.append((similarity, post_lookup[node_id]))

    results.sort(key=lambda x: x[0], reverse=True)

    return results[:top_n]


def choose_method(user_post, top_n=10):
    if user_post.user_type == 'looking_tutor':
        weight_func = compute_edge_weight
    elif user_post.user_type == 'looking_tutions':
        weight_func = compute_edge_weight_dijkstra
    else:
        return []

    return dijkstra_matching(user_post, weight_func, top_n=top_n)
