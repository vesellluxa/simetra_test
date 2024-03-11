from geoalchemy2 import Geometry
from sqlalchemy import Column, DateTime, Float, Integer

from app.core.db import Base


class TrackModel(Base):
    """
    Модель GPS-трека
    """
    __tablename__ = 'track'
    longitude = Column(Float)
    latitude = Column(Float)
    speed = Column(Float)
    gps_time = Column(DateTime)
    vehicle_id = Column(Integer)
    geometry = Column(Geometry('POINT'))
