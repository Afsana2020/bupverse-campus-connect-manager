from django.conf import settings
from core.utils.geo_utils import get_real_distance_km
import heapq
from roommate_finder.models import roomPost


def calculate_weight(user, candidate, distance_km):
    if distance_km == float('inf'):
        return float('inf')

    #location(high)
    location_weight = (distance_km ** 2) * 1000

    #rent(mid)
    rent_penalty = abs(user.rent - candidate.rent) * 2  

    #food preference(low)
    food_penalty = 0
    if user.food != 'Any' and candidate.food != 'Any':
        if user.food != candidate.food:
            food_penalty = 50

    #gender(mid)
    gender_penalty = 0
    if user.gender and candidate.gender:
        if user.gender != candidate.gender:
            gender_penalty = 200

    total_weight = location_weight + rent_penalty + food_penalty + gender_penalty
    return total_weight



def dijkstra_roommate_matching(user_post, top_n=10):
    if user_post.user_type not in ['looking_house', 'looking_roommate']:
        return []

    target_type = 'looking_roommate' if user_post.user_type == 'looking_house' else 'looking_house'
    candidates = roomPost.objects.filter(
        user_type=target_type,
        gender=user_post.gender)


    graph = {user_post.id: []}
    post_lookup = {user_post.id: user_post}

    for candidate in candidates:
        if not all([user_post.latitude, user_post.longitude, candidate.latitude, candidate.longitude]):
            continue

        distance = get_real_distance_km(
            (user_post.latitude, user_post.longitude),
            (candidate.latitude, candidate.longitude)
        )

        weight = calculate_weight(user_post, candidate, distance)
        if weight == float('inf'):
            continue

        graph[user_post.id].append((candidate.id, weight))
        post_lookup[candidate.id] = candidate
        
    distance_map = {user_post.id: 0}
    heap = [(0, user_post.id)]
    visited = set()

    while heap:
        current_dist, current_node = heapq.heappop(heap)

        if current_node in visited:
            continue
        visited.add(current_node)

        for neighbor_id, edge_weight in graph.get(current_node, []):
            total_dist = current_dist + edge_weight
            if neighbor_id not in distance_map or total_dist < distance_map[neighbor_id]:
                distance_map[neighbor_id] = total_dist
                heapq.heappush(heap, (total_dist, neighbor_id))

    # store distance as similarity score
    results = []
    for post_id, dist in distance_map.items():
        if post_id == user_post.id:
            continue
        similarity = 1 / (1 + dist)
        results.append((similarity, post_lookup[post_id]))

    results.sort(key=lambda x: x[0], reverse=True)
    return results[:top_n]
