from datetime import datetime
from typing import List, Optional

from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import TrackModel


class CRUDTrack:
    """
    Объект для CRUD-операций
    """
    def __init__(self):
        self.model = TrackModel

    async def get_objects_by_vehicle_id(self, vehicle_id: int, session: AsyncSession) -> Optional[list]:
        """
        Получение всех объектов модели для валидации запросов
        """
        stmt = select(
            self.model
        ).where(
            self.model.vehicle_id == vehicle_id
        )
        result = await session.execute(stmt)
        objects = result.scalars().first()
        return objects if objects else None

    async def get_last_track_for_vehicles(self, session: AsyncSession):
        """
        Получение последнего трека для каждого vehicle_id
        """
        subquery = select(
            self.model.vehicle_id,
            func.max(
                self.model.gps_time
            ).label(
                "max_gps_time"
            )
        ).group_by(
            self.model.vehicle_id
        ).subquery()
        query = select(
            self.model.id,
            self.model.longitude,
            self.model.latitude,
            self.model.speed,
            self.model.gps_time,
            self.model.vehicle_id,
            self.model.geometry
        ).join(
            subquery,
            and_(
                self.model.vehicle_id == subquery.c.vehicle_id,
                self.model.gps_time == subquery.c.max_gps_time
            )
        )
        res = await session.execute(query)
        return res.all()

    async def get_last_location_for_vehicle(
            self,
            vehicle_id: int,
            session: AsyncSession
    ) -> TrackModel:
        """
        Получение последнего трека для конкретного vehicle_id
        """
        subquery = select(
            self.model.vehicle_id,
            func.max(
                self.model.gps_time
            ).label(
                "max_gps_time"
            )
        ).where(
            self.model.vehicle_id == vehicle_id
        ).group_by(
            self.model.vehicle_id
        ).subquery(
            "latest"
        )

        query = select(
            self.model.id,
            self.model.longitude,
            self.model.latitude,
            self.model.speed,
            self.model.gps_time,
            self.model.vehicle_id,
            self.model.geometry
        ).join(
            subquery,
            and_(
                self.model.vehicle_id == subquery.c.vehicle_id,
                self.model.gps_time == subquery.c.max_gps_time
            )
        ).where(
            self.model.vehicle_id == vehicle_id
        )
        res = await session.execute(query)
        return res.first()

    async def get_vehicle_tracks_by_time(
            self,
            vehicle_id: int,
            start_time: datetime,
            end_time: datetime,
            session: AsyncSession
    ) -> List[TrackModel]:
        """
        Получение всех треков для vehicle_id в диапазоне start_time - end_time
        """
        stmt = select(
            self.model.id,
            self.model.longitude,
            self.model.latitude,
            self.model.speed,
            self.model.gps_time,
            self.model.vehicle_id,
            self.model.geometry
        ).filter(
            self.model.vehicle_id == vehicle_id
        ).filter(
            self.model.gps_time >= start_time
        ).filter(
            self.model.gps_time <= end_time
        ).order_by(
            self.model.gps_time
        )

        result = await session.execute(stmt)
        return result.all()


track_crud = CRUDTrack()
