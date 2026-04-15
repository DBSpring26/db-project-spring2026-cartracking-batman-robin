## Project Architecture

The project follows the required handler/DAO pattern:

backend/
│
├── dao/
│   ├── location_ping_dao.py
│   ├── parking_area_dao.py
│   ├── road_segment_dao.py
│   ├── trip_dao.py
│   └── vehicle_dao.py
├── db/
│   └── db.py
│
├── handlers/
│   ├── location_ping_handler.py
│   ├── parking_area_handler.py
│   ├── road_segment_handler.py
│   ├── trip_handler.py
│   └── vehicle_handler.py
│
├── routes/
│   ├── location_ping_routes.py
│   ├── parking_area_routes.py
│   ├── road_segment_routes.py
│   ├── trip_routes.py
│   └── vehicle_routes.py
│
├── schemas/
│   ├── location_ping_schema.py
│   ├── parking_area_schema.py
│   ├── road_segment_schema.py
│   ├── trip_schema.py
│   └── vehicle_schema.py
│
├── utils/
│   ├── bbox.py
│   └── pagination.py
│
│
├── main.py
└── requirements.txt


## Endpoints

### Vehicles
POST   /api/v1/vehicles
GET    /api/v1/vehicles
GET    /api/v1/vehicles/{vehicle_id}
PUT    /api/v1/vehicles/{vehicle_id}
DELETE /api/v1/vehicles/{vehicle_id}
GET    /api/v1/vehicles/{vehicle_id}/current-location

### Location Pings
POST   /api/v1/location-pings
GET    /api/v1/location-pings
GET    /api/v1/location-pings/{ping_id}
PUT    /api/v1/location-pings/{ping_id}
DELETE /api/v1/location-pings/{ping_id}

### Vehicle Pings
GET    /api/v1/vehicles/{vehicle_id}/pings

### Trips
POST   /api/v1/trips
GET    /api/v1/trips
GET    /api/v1/trips/{trip_id}
PUT    /api/v1/trips/{trip_id}
DELETE /api/v1/trips/{trip_id}

### Vehicle Trips
GET    /api/v1/vehicles/{vehicle_id}/trips

### Road Segments
POST   /api/v1/road-segments
GET    /api/v1/road-segments
GET    /api/v1/road-segments/{road_id}
PUT    /api/v1/road-segments/{road_id}
DELETE /api/v1/road-segments/{road_id}

### Parking Areas
POST   /api/v1/parking-areas
GET    /api/v1/parking-areas
GET    /api/v1/parking-areas/{parking_area_id}
PUT    /api/v1/parking-areas/{parking_area_id}
DELETE /api/v1/parking-areas/{parking_area_id}

### Root
GET    /


## Base URL:

https://cartracking-alexisandjesus.onrender.com

## Interactive API documentation (Swagger):

https://cartracking-alexisandjesus.onrender.com/docs

## Running Locally

Install dependencies:

`pip install -r requirements.txt`

Run server from the `backend` directory:

`uvicorn main:app --reload`

Open docs:

`http://127.0.0.1:8000/docs`

# Credentials

host="dpg-d6ovsu15pdvs739ofrn0-a.virginia-postgres.render.com"
port=5432
dbname="declass"
user="alexisagosto"
password="ehx0AjqfLrNdUErWtDRLgimnorzscTDd"

## Authors

Alexis Agosto Bracety  
Jesus

