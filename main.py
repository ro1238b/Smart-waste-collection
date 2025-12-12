from db import fetch_data
from logic import detect_overflow_bins, sort_bins, prepare_route_points
from routeoptimize import get_optimized_route

def main():
    print("\n📥 Fetching data from MongoDB...")
    data = fetch_data()

    print("\n🚨 Detecting overflowing bins...")
    urgent = detect_overflow_bins(data, threshold=60)  # Set threshold as needed
    if not urgent:
        print("🎉 No bins need urgent cleaning!")
        return

    print("\n📌 Sorting bins by priority...")
    urgent = sort_bins(urgent)

    # Keep only top 50 bins for optimization
    urgent = urgent[:50]

    # Print urgent bins with fill %
    print("\n🔥 Urgent Bins (Highest Fill % First):")
    for b in urgent:
        print(f"{b['bin_id']} — {b['fill_level_percent']}%")

    print("\n📍 Preparing coordinates for route optimization...")
    points = prepare_route_points(urgent)

    print("\n⚙️ Computing optimized route (NN + 2-Opt)...")
    route, total_distance = get_optimized_route(points)

    # Print optimized route
    print("\n🗺 Optimized Cleaning Route:")
    for i, p in enumerate(route, 1):
        print(f"{i}. {p[0]} (Lat: {p[1]}, Lon: {p[2]})")

    # Print total distance only once
    print("\n📏 Total Distance:", round(total_distance, 2), "km")


if __name__ == "__main__":
    main()



