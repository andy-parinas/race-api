from fastapi import APIRouter

from app.api.v1 import meetings
from app.api.v1 import races
from app.api.v1 import analysis

api_router = APIRouter()

api_router.include_router(meetings.router, prefix="/meetings", tags=["Meetings"])
api_router.include_router(races.router, prefix="/races", tags=["Races"])
api_router.include_router(analysis.router, prefix="/analysis", tags=["Analysis"])