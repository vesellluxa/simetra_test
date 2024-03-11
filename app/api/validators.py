import logging

from datetime import date, datetime
from typing import Optional

from fastapi import HTTPException, Query
from sqlalchemy.ext.asyncio.session import AsyncSession

from app.crud.track import track_crud


async def validate_date_params(
        for_date: Optional[date] = Query(None),
        start_time: Optional[datetime] = Query(None),
        end_time: Optional[datetime] = Query(None)
) -> None:
    """
    Валидатор для параметров фильтрации
    """
    if for_date and (start_time or end_time):
        raise HTTPException(
            status_code=422,
            detail="Невозможно использовать аргумент 'for_date' И один "
                   "из аргументов 'start_time', 'end_time'"
        )
    if (start_time and not end_time) or (not start_time and end_time):
        raise HTTPException(
            status_code=422,
            detail="Невозможно использовать только один из аргументов "
                   "'start_time', 'end_time'"
        )
    if not for_date and not start_time and not end_time:
        raise HTTPException(
            status_code=422,
            detail="Должен быть передан или аргумент 'for_date'"
                   " или оба аргумента 'start_time' и 'end_time'"
        )
    if start_time and end_time:
        if start_time >= end_time:
            raise HTTPException(
                status_code=422,
                detail="Время начала диапазона фильтрации"
                       " не может быть равно или превышать"
                       " время окончания диапазона"
            )


async def validate_vehicle_id_exists(
        vehicle_id: int,
        session: AsyncSession
) -> None:
    """
    Валидатор для проверки наличия записей с указанным vehicle_id в БД
    """
    objects = await track_crud.get_objects_by_vehicle_id(
        vehicle_id=vehicle_id,
        session=session
    )
    logging.warning(objects)
    if not objects:
        raise HTTPException(
            status_code=404,
            detail=(f"Объекты с указанным"
                    f" vehicle_id {vehicle_id}"
                    f" не найдены.")
        )


async def validate_empty_tracks(
        objs: list,
        vehicle_id: int,
        start_time: datetime,
        end_time: datetime
) -> None:
    """
    Валидатор для проверки возвращаемых значений после фильтрации.
    Если ответ БД - пустой список вызывает исключение 404
    """
    if not objs:
        raise HTTPException(
            status_code=404,
            detail=(f"Объекты для указанного"
                    f" vehicle_id {vehicle_id}"
                    f" и диапазона {start_time}, "
                    f"{end_time} не найдены.")
        )
