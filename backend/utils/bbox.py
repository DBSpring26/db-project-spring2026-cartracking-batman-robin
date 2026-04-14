def parse_bbox(bbox: str):
    parts = bbox.split(",")

    if len(parts) != 4:
        raise ValueError("bbox must have 4 values: minLon,minLat,maxLon,maxLat")

    min_lon, min_lat, max_lon, max_lat = map(float, parts)

    if not (-180 <= min_lon <= 180 and -180 <= max_lon <= 180):
        raise ValueError("Longitude must be between -180 and 180")

    if not (-90 <= min_lat <= 90 and -90 <= max_lat <= 90):
        raise ValueError("Latitude must be between -90 and 90")

    if min_lon >= max_lon:
        raise ValueError("minLon must be smaller than maxLon")

    if min_lat >= max_lat:
        raise ValueError("minLat must be smaller than maxLat")

    return min_lon, min_lat, max_lon, max_lat