from datetime import datetime
from typing import Optional

import shapely.wkt

from geoalchemy2.elements import WKBElement
from geoalchemy2.shape import to_shape
from pydantic import BaseModel, Field, field_validator


class TrackModel(BaseModel):
    """
    Pydantic-модель GPS-трекера
    """
    id: Optional[int] = None
    longitude: float
    latitude: float
    speed: float
    gps_time: datetime
    vehicle_id: int
    geometry: str = Field(..., example="POINT(30 10)")

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "longitude": 30.0,
                "latitude": 10.0,
                "speed": 100.0,
                "gps_time": "2023-01-01T12:00:00",
                "vehicle_id": "vehicle123",
                "geometry": "POINT(30 10)"
            }
        }

    @field_validator('geometry', mode='before')
    def convert_geometry_to_wkt(cls, value):
        if isinstance(value, WKBElement):
            # Преобразование элемента WKB в объект Shapely
            shape = to_shape(value)
            # Преобразование объекта Shapely в строку WKT
            return shapely.wkt.dumps(shape)
        return value
