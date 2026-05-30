# Car Tracking System

## Overview

The system provides an interactive dashboard where users can explore vehicles, trips, parking areas, road segments, and location pings through maps, tables and analytics.

# Team Members

- Alexis Agosto Bracety
- Jesus Rodriguez

# Technologies Used

## Backend

- Python
- FastAPI
- PostgreSQL
- PostGIS
- Uvicorn

## Frontend

- Streamlit
- Folium
- Plotly
- Pandas

## ETL

- Pandas
- PyArrow

# Database

The project uses PostgreSQL with the PostGIS extension to support geospatial operations.

Main tables:

- vehicle
- trip
- location_ping
- road_segment
- parking_area
- fuel_type
- vehicle_type
- vehicle_status

# Features

## Authentication

- User Registration
- User Login
- User Logout

## Vehicles

- Vehicle listing
- Vehicle information visualization

## Parking Areas Map

- Interactive parking area visualization
- Capacity filtering
- Bounding box filtering
- Parking area information popups

## Road Segments Map

- Interactive road segment visualization
- Direction filtering
- One-way filtering
- Speed limit filtering
- Bounding box filtering
- Road information popups

## Latest Vehicle Pings

- Displays the latest location of every vehicle
- Interactive map visualization
- Bounding box filtering
- Vehicle location details

## Breadcrumb Visualization

- Vehicle route visualization
- Trip identification
- Time range filtering
- Route reconstruction using location pings

## Analytics

### Pings Per Day

Displays the number of recorded pings per day using an interactive Plotly chart.

---

# Dataset Statistics

Current database contents:

| Vehicles | 31 |
| Location Pings | 28,044 |
| Trips | 301 |


# API Documentation

## Production API

https://cartracking-alexisandjesus.onrender.com

## Swagger Documentation

https://cartracking-alexisandjesus.onrender.com/docs

---

# Running the Project Locally

The application requires two terminals.

---

## Terminal 1 - Backend

Navigate to the backend directory:

```bash
cd backend
```

Activate the virtual environment:

```bash
source ../venv/bin/activate
```

Start FastAPI:

```bash
uvicorn main:app --reload
```

Backend URL:

```text
http://127.0.0.1:8000
```

Swagger:

```text
http://127.0.0.1:8000/docs
```

Leave this terminal running.

---

## Terminal 2 - Frontend

Open a second terminal.

Navigate to the frontend directory:

```bash
cd web_application
```

Activate the virtual environment:

```bash
source ../venv/bin/activate
```

Run Streamlit:

```bash
streamlit run app.py
```

Dashboard URL:

```text
http://localhost:8501
```

Leave this terminal running.

---

# ETL Process

The ETL pipeline is responsible for:

- Loading parquet datasets
- Cleaning and validating records
- Transforming geometry fields
- Creating PostGIS geometries
- Loading data into PostgreSQL
- Preserving relationships between tables

---

# Spatial Features

PostGIS is used to support advanced geospatial functionality:

- Bounding Box Queries
- Geometry Storage
- ST_Intersects Operations
- Spatial Filtering
- Parking Area Visualization
- Road Segment Visualization
- Vehicle Route Visualization
