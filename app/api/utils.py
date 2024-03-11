from datetime import date, datetime, time


def create_datetime_range_from_date(
        input_date: date
) -> tuple:
    """
    Создаёт объекты для фильтрации по дате
    """
    return (datetime.combine(input_date, time.min),
            datetime.combine(input_date, time.max))
