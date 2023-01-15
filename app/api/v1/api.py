from fastapi import APIRouter

from app.api.v1 import meetings


api_router = APIRouter()

api_router.include_router(meetings.router, prefix="/meetings", tags=["Meetings"])