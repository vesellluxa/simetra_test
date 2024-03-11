from datetime import date, datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.utils import create_datetime_range_from_date
from app.api.validators import (validate_date_params,
                                validate_empty_tracks,
                                validate_vehicle_id_exists)
from app.core.db import get_async_session
from app.crud.track import track_crud
from app.schemas import TrackModel

router = APIRouter()


@router.get(
    "/",
    response_model=List[TrackModel]
)
async def get_vehicles_last_tracks(
        session: AsyncSession = Depends(get_async_session)
):
    """
    GET запрос для получения всех машин с последней геометрией.
    """
    return await track_crud.get_last_track_for_vehicles(
        session=session
    )


@router.get(
    "/{vehicle_id}",
    response_model=TrackModel
)
async def get_vehicle_last_track(
        vehicle_id: int,
        session: AsyncSession = Depends(get_async_session),

):
    """
    GET запрос для получения конкретной машины с последней геометрией.
    """
    await validate_vehicle_id_exists(
        vehicle_id=vehicle_id,
        session=session
    )
    last_track = await track_crud.get_last_location_for_vehicle(
        vehicle_id=vehicle_id,
        session=session
    )
    if last_track:
        return last_track
    raise HTTPException(
        status_code=404,
        detail="Объекта с указанным vehicle_id не существует"
    )


@router.get(
    "/{vehicle_id}/track",
    response_model=List[TrackModel]
)
async def get_tracks_for_vehicle(
        vehicle_id: int,
        for_date: Optional[date] = Query(
            None,
            title="Дата",
            description="Дата для фильтрации "
                        "в формате YYYY-MM-DD"
        ),
        start_time: Optional[datetime] = Query(
            None,
            title="Дата и время начала",
            description="Дата и время для "
                        "начала диапазона фильтрации"
                        " в формате YYYY-MM-DD HH:MM:SS"
        ),
        end_time: Optional[datetime] = Query(
            None,
            title="Дата и время окончания",
            description="Дата и время для "
                        "окончания диапазона фильтрации"
                        " в формате YYYY-MM-DD HH:MM:SS"
        ),
        session: AsyncSession = Depends(get_async_session)
):
    """
    GET запрос для построения трека по дате или временному диапазону для конкретной машины. \n
    В запросе должны присутствовать query_params for_date или (start_time И end_time). \n
    Если передан параметр start_time, он не должен превышать end_time. \n
    Диапазон фильтрации любой. \n
    """
    await validate_vehicle_id_exists(
        vehicle_id=vehicle_id,
        session=session
    )
    await validate_date_params(
        for_date=for_date,
        start_time=start_time,
        end_time=end_time
    )
    if for_date:
        start_time, end_time = create_datetime_range_from_date(for_date)
    tracks = await track_crud.get_vehicle_tracks_by_time(
        vehicle_id=vehicle_id,
        start_time=start_time,
        end_time=end_time,
        session=session
    )
    await validate_empty_tracks(
        objs=tracks,
        vehicle_id=vehicle_id,
        start_time=start_time,
        end_time=end_time
    )
    return tracks
