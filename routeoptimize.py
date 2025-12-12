import math

# ----------------------------
# Haversine Distance
# ----------------------------
def distance(lat1, lon1, lat2, lon2):
    R = 6371  # km
    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)

    a = (math.sin(d_lat / 2) ** 2 +
         math.cos(math.radians(lat1)) *
         math.cos(math.radians(lat2)) *
         math.sin(d_lon / 2) ** 2)

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


# ----------------------------
# Nearest Neighbor TSP
# ----------------------------
def nearest_neighbor(points):
    unvisited = points.copy()
    route = []

    current = unvisited.pop(0)
    route.append(current)

    while unvisited:
        next_point = min(
            unvisited,
            key=lambda p: distance(current[1], current[2], p[1], p[2])
        )
        route.append(next_point)
        unvisited.remove(next_point)
        current = next_point

    return route


# ----------------------------
# Route Distance
# ----------------------------
def route_distance(route):
    total = 0
    for i in range(len(route) - 1):
        a = route[i]
        b = route[i + 1]
        total += distance(a[1], a[2], b[1], b[2])
    return total


# ----------------------------
# 2-Opt Optimization
# ----------------------------
def two_opt(route):
    best = route
    improved = True

    while improved:
        improved = False
        for i in range(1, len(best) - 2):
            for j in range(i + 1, len(best) - 1):
                new_route = best[:]
                new_route[i:j] = reversed(best[i:j])

                if route_distance(new_route) < route_distance(best):
                    best = new_route
                    improved = True

    return best


# ----------------------------
# Main Optimization Function
# ----------------------------
def get_optimized_route(points):
    initial_route = nearest_neighbor(points)
    optimized_route = two_opt(initial_route)
    return optimized_route, route_distance(optimized_route)
