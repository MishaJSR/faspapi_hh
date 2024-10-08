import asyncio
import logging
import threading
from concurrent.futures import ThreadPoolExecutor

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.posts.models import VacancyRepository
from src.workers.ParserHH import ParserHH
from src.workers.Reporter import Reporter

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


@router.get("/all_posts")
async def get_last_messages(session: AsyncSession = Depends(get_async_session)):
    res = await VacancyRepository().get_all_by_fields(session=session, data=["url", "is_active"])
    return res


# @router.post("/find_post")
# async def find_post(target: str, additions: str = "", session: AsyncSession = Depends(get_async_session)):
#     filed_filter = {
#         "name": target.lower()
#     }
#     if additions:
#         filed_filter["experience"] = additions.lower()
#     res = await VacancyRepository().get_all_contain_fields(session=session,
#                                                            data=["name", "url", "salary", "experience",
#                                                                  "employer", "location"],
#                                                            field_filter=filed_filter)
#     return res


@router.post("/start_pooling")
async def start_pooling(key: str):
    if key == "private":
        parser_hh = ParserHH()
        parser_hh.start_parsing()
        reporter = Reporter()
        reporter.start_send()
        return []
