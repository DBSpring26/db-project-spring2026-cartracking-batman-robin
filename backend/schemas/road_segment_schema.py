from typing import Optional, List
from pydantic import BaseModel, field_validator


class LineStringGeometry(BaseModel):
    type: str
    coordinates: List[List[float]]

    @field_validator("type")
    @classmethod
    def validate_type(cls, value: str):
        if value != "LineString":
            raise ValueError("geom.type must be 'LineString'.")
        return value

    @field_validator("coordinates")
    @classmethod
    def validate_coordinates(cls, value: List[List[float]]):
        if len(value) < 2:
            raise ValueError("LineString must have at least 2 coordinate pairs.")

        for pair in value:
            if len(pair) != 2:
                raise ValueError("Each coordinate pair must have exactly 2 values.")
            lon, lat = pair
            if lon < -180 or lon > 180:
                raise ValueError("Longitude must be between -180 and 180.")
            if lat < -90 or lat > 90:
                raise ValueError("Latitude must be between -90 and 90.")

        return value


class RoadSegmentCreate(BaseModel):
    name: str
    speed_limit_kph: int
    geom: LineStringGeometry
    is_oneway: bool
    direction: str

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str):
        value = value.strip()
        if not value:
            raise ValueError("name must be non-empty.")
        return value

    @field_validator("speed_limit_kph")
    @classmethod
    def validate_speed_limit(cls, value: int):
        if value <= 0:
            raise ValueError("speed_limit_kph must be > 0.")
        return value

    @field_validator("direction")
    @classmethod
    def validate_direction(cls, value: str):
        value = value.strip()
        if not value:
            raise ValueError("direction must be non-empty.")
        return value


class RoadSegmentUpdate(BaseModel):
    name: Optional[str] = None
    speed_limit_kph: Optional[int] = None
    geom: Optional[LineStringGeometry] = None
    is_oneway: Optional[bool] = None
    direction: Optional[str] = None

    @field_validator("name")
    @classmethod
    def validate_name(cls, value):
        if value is None:
            return value
        value = value.strip()
        if not value:
            raise ValueError("name must be non-empty.")
        return value

    @field_validator("speed_limit_kph")
    @classmethod
    def validate_speed_limit(cls, value):
        if value is None:
            return value
        if value <= 0:
            raise ValueError("speed_limit_kph must be > 0.")
        return value

    @field_validator("direction")
    @classmethod
    def validate_direction(cls, value):
        if value is None:
            return value
        value = value.strip()
        if not value:
            raise ValueError("direction must be non-empty.")
        return value