from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_title: str = 'Simetra Test'
    app_description: str = 'API для отслеживания машин + загрузка файла'
    database_url: str = 'postgresql+asyncpg://simetra:simetra@db:5432/simetra'
    secret: str = 'секрет'

    class Config:
        env_file = '/app/app/.env'


settings = Settings()
