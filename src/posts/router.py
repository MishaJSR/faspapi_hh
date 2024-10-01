from typing import List

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from pydantic import BaseModel
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.posts.models import VacancyRepository

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

@router.get("/all_posts")
async def get_last_messages(session: AsyncSession = Depends(get_async_session)):
    res = await VacancyRepository().get_all_by_fields(session=session, data=["url", "is_active"])
    return res


@router.post("/start_pooling")
async def start_pooling(key: str, session: AsyncSession = Depends(get_async_session)):
    return []