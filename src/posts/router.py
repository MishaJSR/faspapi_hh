import asyncio
import threading

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.posts.models import VacancyRepository
from src.posts.utils import push_to_db
from src.workers.ParserHH import ParserHH

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
    if key == "private":
        parser_hh = ParserHH()
        parser_hh.start_parsing()
        asyncio.create_task(push_to_db(session))
        return []