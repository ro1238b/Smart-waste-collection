from db import get_bins
from routeoptimize import nearest_neighbour, two_opt, total_distance

def compute_route():
    bins = get_bins()

    if not bins:
        raise Exception("No bins found in MongoDB!")

    # Step 1 — Nearest neighbour
    nn_route = nearest_neighbour(bins)

    # Step 2 — 2-opt optimization
    final_route = two_opt(nn_route)

    # Step 3 — Total optimized distance
    distance = total_distance(final_route)

    return final_route, distance

