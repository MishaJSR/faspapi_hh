import asyncio
import logging
import threading

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.posts.models import VacancyRepository
from src.posts.utils import hh_pusher_to_db
from src.workers.ParserHH import ParserHH



router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


@router.get("/all_posts")
async def get_last_messages(session: AsyncSession = Depends(get_async_session)):
    res = await VacancyRepository().get_all_by_fields(session=session, data=["url", "is_active"])
    return res


@router.post("/find_post")
async def get_last_messages(target: str, additions: str = "", session: AsyncSession = Depends(get_async_session)):
    filed_filter = {
        "name": target.lower()
    }
    if additions:
        filed_filter["experience"] = additions.lower()
    res = await VacancyRepository().get_all_contain_fields(session=session,
                                                           data=["name", "url", "salary", "experience",
                                                                 "employer", "location"],
                                                           field_filter=filed_filter)
    return res


@router.post("/start_pooling")
async def start_pooling(key: str, session: AsyncSession = Depends(get_async_session)):
    if key == "private":
        parser_hh = ParserHH()
        is_already_start = parser_hh.start_parsing()
        if not is_already_start:
            asyncio.create_task(hh_pusher_to_db(session))
        return []
