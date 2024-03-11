from fastapi import APIRouter

from app.api.endpoints import vehicle_router

main_router = APIRouter()

main_router.include_router(
    vehicle_router,
    prefix='/api/v1/vehicles',
    tags=['vehicle']
)
