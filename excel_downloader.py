import asyncio
import datetime

import argparse
import pandas
from sqlalchemy.ext.asyncio.session import AsyncSession

from app.core.db import get_async_session
from app.models import TrackModel


def make_naive(dt: datetime):
    """
    Делает переданный объект наивным
    """
    return dt.replace(tzinfo=None)


def read_excel(file_path: str) -> pandas.DataFrame:
    """
    Считывает excel-файл
    """
    return pandas.read_excel(file_path, engine='openpyxl')


async def load_data(
        df: pandas.DataFrame,
        session: AsyncSession
):
    """
    Создаёт объекты и загружает их в БД
    """
    data_to_insert = [
        {
            "id": row["id"],
            "longitude": row["longitude"],
            "latitude": row["latitude"],
            "speed": row["speed"],
            "gps_time": make_naive(
                datetime.datetime.fromisoformat(row["gps_time"])
            ) if isinstance(row["gps_time"], str) else row["gps_time"],
            "vehicle_id": row["vehicle_id"],
            "geometry": f"SRID=4326;POINT({row['longitude']} {row['latitude']})"
        }
        for index, row in df.iterrows()
    ]

    # Вставка данных пачками
    async with session.begin():
        await session.run_sync(
            lambda session: session.bulk_insert_mappings(
                TrackModel, data_to_insert
            )
        )


async def main(file_path: str):
    df = read_excel(file_path)
    session = await get_async_session()
    await load_data(df, session)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Load data from an Excel file into the database.'
    )
    parser.add_argument(
        'file_path',
        type=str,
        help='Path to the Excel file'
    )
    args = parser.parse_args()

    asyncio.run(main(args.file_path))
