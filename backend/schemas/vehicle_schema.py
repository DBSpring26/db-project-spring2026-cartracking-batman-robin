from typing import Optional
from pydantic import BaseModel, field_validator


class VehicleCreate(BaseModel):
    vehicle_type_id: int
    vehicle_status_id: int
    plate_number: str
    make: Optional[str] = None
    model: Optional[str] = None
    year: Optional[int] = None

    @field_validator("plate_number")
    @classmethod
    def validate_plate_number(cls, value: str):
        value = value.strip()
        if not value:
            raise ValueError("plate_number is required and must be non-empty.")
        return value

    @field_validator("make", "model")
    @classmethod
    def trim_optional_text(cls, value):
        if value is None:
            return value
        return value.strip()

    @field_validator("year")
    @classmethod
    def validate_year(cls, value):
        if value is None:
            return value
        if value < 1950 or value > 2100:
            raise ValueError("year must be between 1950 and 2100.")
        return value


class VehicleUpdate(BaseModel):
    vehicle_type_id: Optional[int] = None
    vehicle_status_id: Optional[int] = None
    plate_number: Optional[str] = None
    make: Optional[str] = None
    model: Optional[str] = None
    year: Optional[int] = None

    @field_validator("plate_number")
    @classmethod
    def validate_plate_number(cls, value):
        if value is None:
            return value
        value = value.strip()
        if not value:
            raise ValueError("plate_number must be non-empty.")
        return value

    @field_validator("make", "model")
    @classmethod
    def trim_optional_text(cls, value):
        if value is None:
            return value
        return value.strip()

    @field_validator("year")
    @classmethod
    def validate_year(cls, value):
        if value is None:
            return value
        if value < 1950 or value > 2100:
            raise ValueError("year must be between 1950 and 2100.")
        return value