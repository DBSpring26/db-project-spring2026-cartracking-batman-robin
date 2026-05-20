import requests

BASE_URL = "http://127.0.0.1:8000/api/v1"


def api_get(path, params=None):
    response = requests.get(f"{BASE_URL}{path}", params=params)
    response.raise_for_status()
    return response.json()


def api_post(path, payload):
    response = requests.post(f"{BASE_URL}{path}", json=payload)
    return response


def signup(username, password):
    return api_post("/auth/signup", {"username": username, "password": password})


def login(username, password):
    return api_post("/auth/login", {"username": username, "password": password})


def get_vehicles(limit=100, offset=0):
    return api_get("/vehicles", {"limit": limit, "offset": offset})


def get_parking_areas(limit=100, offset=0, name=None, capacity=None, bbox=None):
    params = {"limit": limit, "offset": offset}

    if name:
        params["name"] = name

    if capacity is not None:
        params["capacity"] = capacity

    if bbox:
        params["bbox"] = bbox

    return api_get("/parking-areas", params)


def get_road_segments(
    limit=100,
    offset=0,
    direction=None,
    is_oneway=None,
    name=None,
    speed_limit_kph=None,
    bbox=None
):
    params = {"limit": limit, "offset": offset}

    if direction:
        params["direction"] = direction

    if is_oneway is not None:
        params["is_oneway"] = is_oneway

    if name:
        params["name"] = name

    if speed_limit_kph is not None:
        params["speed_limit_kph"] = speed_limit_kph

    if bbox:
        params["bbox"] = bbox

    return api_get("/road-segments", params)


def get_latest_pings(limit=100, offset=0, bbox=None):
    params = {"limit": limit, "offset": offset}

    if bbox:
        params["bbox"] = bbox

    return api_get("/location-pings/latest", params)


def get_breadcrumb(vehicle_id, start_ts, end_ts):
    response = requests.get(
        f"{BASE_URL}/location-pings/breadcrumb",
        params={
            "vehicle_id": vehicle_id,
            "start_ts": start_ts,
            "end_ts": end_ts
        }
    )

    if response.status_code != 200:
        return {
            "items": [],
            "trip_ids": [],
            "count": 0,
            "error": response.text
        }

    return response.json()


def get_pings_per_day():
    return api_get("/location-pings/pings-per-day")