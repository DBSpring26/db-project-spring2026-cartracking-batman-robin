import streamlit as st
import pandas as pd
import folium
import plotly.express as px
from streamlit_folium import st_folium
from api_client import *

st.set_page_config(
    page_title="Car Tracking Dashboard",
    layout="wide"
)

MAYAGUEZ_CENTER = [18.2013, -67.1452]


# ================= HELPERS =================

def bbox_string(min_lon, min_lat, max_lon, max_lat):
    return f"{min_lon},{min_lat},{max_lon},{max_lat}"


def get_coords_from_geom(geom):
    if not geom:
        return None

    return geom.get("coordinates")


# ================= LOGIN =================

def require_login():

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if st.session_state.logged_in:
        return True

    st.title("🚗 Car Tracking System")

    tab1, tab2 = st.tabs(["Login", "Sign Up"])

    # ---------- LOGIN ----------

    with tab1:

        username = st.text_input(
            "Username",
            key="login_user"
        )

        password = st.text_input(
            "Password",
            type="password",
            key="login_pass"
        )

        if st.button("Login"):

            response = login(username, password)

            if response.status_code == 200:

                st.session_state.logged_in = True
                st.session_state.username = username

                st.rerun()

            else:
                st.error(
                    response.json().get(
                        "detail",
                        "Login failed"
                    )
                )

    # ---------- SIGNUP ----------

    with tab2:

        username = st.text_input(
            "New Username",
            key="signup_user"
        )

        password = st.text_input(
            "New Password",
            type="password",
            key="signup_pass"
        )

        if st.button("Create Account"):

            response = signup(username, password)

            if response.status_code in [200, 201]:

                st.success(
                    "User created successfully. You can now log in."
                )

            else:
                st.error(
                    response.json().get(
                        "detail",
                        "Signup failed"
                    )
                )

    return False


if not require_login():
    st.stop()


# ================= SIDEBAR =================

st.sidebar.success(
    f"Logged in as {st.session_state.username}"
)

if st.sidebar.button("Logout"):

    st.session_state.logged_in = False
    st.rerun()


# ================= MAIN TITLE =================

st.title("🚗 Car Tracking Dashboard")


menu = st.sidebar.selectbox(
    "Select Feature",
    [
        "Vehicles",
        "Parking Areas Map",
        "Road Segments Map",
        "Latest Vehicle Pings",
        "Breadcrumb",
        "Pings Per Day Chart"
    ]
)



# ===================== VEHICLES ==========================


if menu == "Vehicles":

    st.subheader("Vehicles")

    data = get_vehicles(limit=100)

    df = pd.DataFrame(
        data.get("items", [])
    )

    st.dataframe(
        df,
        width="stretch"
    )



# ================= PARKING AREAS MAP =====================


elif menu == "Parking Areas Map":

    st.subheader("Parking Areas Map")

    with st.sidebar:

        st.markdown("### Filters")

        name = st.text_input("Name")

        capacity_input = st.text_input("Capacity")

        use_bbox = st.checkbox(
            "Use bbox filter"
        )

        bbox = None

        if use_bbox:

            min_lon = st.number_input(
                "minLon",
                value=-67.1700,
                format="%.6f"
            )

            min_lat = st.number_input(
                "minLat",
                value=18.1900,
                format="%.6f"
            )

            max_lon = st.number_input(
                "maxLon",
                value=-67.1200,
                format="%.6f"
            )

            max_lat = st.number_input(
                "maxLat",
                value=18.2300,
                format="%.6f"
            )

            bbox = bbox_string(
                min_lon,
                min_lat,
                max_lon,
                max_lat
            )

    capacity = (
        int(capacity_input)
        if capacity_input.strip().isdigit()
        else None
    )

    data = get_parking_areas(
        limit=500,
        name=name if name else None,
        capacity=capacity,
        bbox=bbox
    )

    items = data.get("items", [])

    m = folium.Map(
        location=MAYAGUEZ_CENTER,
        zoom_start=14
    )

    for item in items:

        geom = item.get("geom")

        coords = get_coords_from_geom(geom)

        if coords:

            popup = (
                f"ID: {item.get('parking_area_id')}<br>"
                f"Capacity: {item.get('capacity')}"
            )

            folium.GeoJson(
                geom,
                tooltip=item.get("name"),
                popup=popup,
                style_function=lambda x: {
                    "color": "blue",
                    "weight": 3,
                    "opacity": 0.8,
                    "fillOpacity": 0.3
                }
            ).add_to(m)

    st_folium(
        m,
        width=1100,
        height=600
    )

    st.subheader(
        "Displayed Parking Areas"
    )

    st.dataframe(
        pd.DataFrame(items),
        width="stretch"
    )



# ================= ROAD SEGMENTS MAP =====================


elif menu == "Road Segments Map":

    st.subheader("Road Segments Map")

    with st.sidebar:

        st.markdown("### Filters")

        direction = st.selectbox(
            "Direction",
            ["", "forward", "backward", "both"]
        )

        oneway = st.selectbox(
            "One Way",
            ["", "true", "false"]
        )

        name = st.text_input(
            "Road Name"
        )

        speed_input = st.text_input(
            "Speed Limit"
        )

        use_bbox = st.checkbox(
            "Use bbox filter"
        )

        bbox = None

        if use_bbox:

            min_lon = st.number_input(
                "minLon",
                value=-67.1700,
                format="%.6f"
            )

            min_lat = st.number_input(
                "minLat",
                value=18.1900,
                format="%.6f"
            )

            max_lon = st.number_input(
                "maxLon",
                value=-67.1200,
                format="%.6f"
            )

            max_lat = st.number_input(
                "maxLat",
                value=18.2300,
                format="%.6f"
            )

            bbox = bbox_string(
                min_lon,
                min_lat,
                max_lon,
                max_lat
            )

    is_oneway = None

    if oneway == "true":
        is_oneway = True

    elif oneway == "false":
        is_oneway = False

    speed_limit_kph = (
        int(speed_input)
        if speed_input.strip().isdigit()
        else None
    )

    data = get_road_segments(
        limit=500,
        direction=direction if direction else None,
        is_oneway=is_oneway,
        name=name if name else None,
        speed_limit_kph=speed_limit_kph,
        bbox=bbox
    )

    items = data.get("items", [])

    m = folium.Map(
        location=MAYAGUEZ_CENTER,
        zoom_start=14
    )

    for item in items:

        geom = item.get("geom")

        if geom:

            popup = (
                f"Street: {item.get('name')}<br>"
                f"Speed limit: {item.get('speed_limit_kph')} kph"
            )

            folium.GeoJson(
                geom,
                tooltip=item.get("name"),
                popup=popup,
                style_function=lambda x: {
                    "color": "red",
                    "weight": 5,
                    "opacity": 1.0
                }
            ).add_to(m)

    st_folium(
        m,
        width=1100,
        height=600
    )

    st.subheader(
        "Displayed Road Segments"
    )

    st.dataframe(
        pd.DataFrame(items),
        width="stretch"
    )



# ================= LATEST VEHICLE PINGS ==================


elif menu == "Latest Vehicle Pings":

    st.subheader("Latest Vehicle Pings")

    with st.sidebar:

        st.markdown("### Filters")

        use_bbox = st.checkbox(
            "Use bbox filter"
        )

        bbox = None

        if use_bbox:

            min_lon = st.number_input(
                "minLon",
                value=-67.1800,
                format="%.6f"
            )

            min_lat = st.number_input(
                "minLat",
                value=18.1700,
                format="%.6f"
            )

            max_lon = st.number_input(
                "maxLon",
                value=-67.1000,
                format="%.6f"
            )

            max_lat = st.number_input(
                "maxLat",
                value=18.2600,
                format="%.6f"
            )

            bbox = bbox_string(
                min_lon,
                min_lat,
                max_lon,
                max_lat
            )

    data = get_latest_pings(
        limit=500,
        bbox=bbox
    )

    items = data.get("items", [])

    m = folium.Map(
        location=MAYAGUEZ_CENTER,
        zoom_start=12
    )

    for item in items:

        geom = item.get("geom")

        coords = get_coords_from_geom(geom)

        if coords:

            lon, lat = coords

            popup = (
                f"Vehicle ID: {item.get('vehicle_id')}<br>"
                f"Timestamp: {item.get('ts')}<br>"
                f"Speed: {item.get('speed_kph')} kph"
            )

            folium.Marker(
                location=[lat, lon],
                popup=popup,
                tooltip=f"Vehicle {item.get('vehicle_id')}"
            ).add_to(m)

    st_folium(
        m,
        width=1100,
        height=600
    )

    st.subheader(
        "Displayed Location Pings"
    )

    st.dataframe(
        pd.DataFrame(items),
        width="stretch"
    )



# ===================== BREADCRUMB ========================


elif menu == "Breadcrumb":

    st.subheader("Vehicle Breadcrumb")

    vehicles_data = get_vehicles(limit=500)

    vehicles = vehicles_data.get("items", [])

    vehicle_ids = [
        v["vehicle_id"]
        for v in vehicles
    ]

    col1, col2, col3 = st.columns(3)

    with col1:

        vehicle_id = st.selectbox(
            "Vehicle",
            vehicle_ids
        )

    with col2:

        start_ts = st.text_input(
            "Start Timestamp",
            "2025-11-10T06:00:00"
        )

    with col3:

        end_ts = st.text_input(
            "End Timestamp",
            "2025-11-10T06:02:00"
        )

    if st.button("Show Breadcrumb"):

        st.session_state.breadcrumb_data = get_breadcrumb(
            vehicle_id,
            start_ts,
            end_ts
        )

    if "breadcrumb_data" in st.session_state:

        data = st.session_state.breadcrumb_data

        items = data.get("items", [])

        st.write(
            f"Trips found: {len(data.get('trip_ids', []))}"
        )

        st.write(
            "Count:",
            data.get("count", len(items))
        )

        m = folium.Map(
            location=MAYAGUEZ_CENTER,
            zoom_start=13
        )

        trip_points = {}

        for item in items:

            geom = item.get("geom")

            coords = get_coords_from_geom(geom)

            trip_id = item.get("trip_id")

            if coords:

                lon, lat = coords

                if trip_id not in trip_points:
                    trip_points[trip_id] = []

                trip_points[trip_id].append(
                    [lat, lon]
                )

                folium.CircleMarker(
                    location=[lat, lon],
                    radius=3,
                    popup=f"""
                        Trip: {trip_id}<br>
                        Ping: {item.get('ping_id')}<br>
                        Time: {item.get('ts')}
                    """
                ).add_to(m)

        for trip_id, points in trip_points.items():

            if len(points) >= 2:

                folium.PolyLine(
                    points,
                    weight=5,
                    color="blue"
                ).add_to(m)

                folium.Marker(
                    points[0],
                    popup=f"Trip {trip_id} Start"
                ).add_to(m)

                folium.Marker(
                    points[-1],
                    popup=f"Trip {trip_id} End"
                ).add_to(m)

        st_folium(
            m,
            width=1100,
            height=600,
            key="breadcrumb_map"
        )

        st.subheader(
            "Breadcrumb Records"
        )

        st.dataframe(
            pd.DataFrame(items),
            width="stretch"
        )



# ================= PINGS PER DAY CHART ===================

elif menu == "Pings Per Day Chart":

    st.subheader(
        "Number of Pings Registered Per Day"
    )

    data = get_pings_per_day()

    items = data.get("items", [])

    # FIX nested items
    if isinstance(items, dict):
        items = items.get("items", [])

    df = pd.DataFrame(items)

    if not df.empty:

        fig = px.bar(
            df,
            x="day",
            y="total_pings",
            title="Pings Per Day"
        )

        st.plotly_chart(
            fig,
            config={
                "displaylogo": False
            }
        )

        st.subheader("Ping Statistics")

        st.dataframe(
            df,
            width="stretch"
        )

    else:
        st.info(
            "No ping data available."
        )