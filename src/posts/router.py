from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from workers.ParserHH import ParserHH
from workers.Reporter import Reporter

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


@router.post("/start_pooling")
async def start_pooling(key: str):
    if key == "private":
        parser_hh = ParserHH()
        parser_hh.start_parsing()
        reporter = Reporter()
        reporter.start_send()
        return []
