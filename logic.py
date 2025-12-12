from db import fetch_bin


from db import recordings_collection, fetch_bin
def detect_overflow_bins(data, threshold=60):
    """Find bins with fill_level > threshold."""
    urgent = []

    for d in data:
        if "location_lat" not in d:
            # Fetch location from bins collection
            bin_doc = fetch_bin(d["bin_id"])
            if not bin_doc:
                continue
            d["location_lat"] = bin_doc["location_lat"]
            d["location_lon"] = bin_doc["location_lon"]

        if d["fill_level_percent"] > threshold:
            urgent.append(d)

    return urgent





def sort_bins(urgent_bins):
    """Sort bins by fill level descending."""
    return sorted(urgent_bins, key=lambda x: x["fill_level_percent"], reverse=True)


def prepare_route_points(urgent_bins):
    """Convert urgent bin list into (bin_id, lat, lon) format."""
    return [(b["bin_id"], b["location_lat"], b["location_lon"]) for b in urgent_bins]
