import asyncio

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from vacancy.models import vac_repository
from workers.hh.ParserHH import ParserHH
from workers.Reporter import Reporter

router = APIRouter(
    prefix="/vacancy",
    tags=["Posts"]
)


@router.post("/start_pooling")
async def start_pooling(key: str):
    if key == "private":
        reporter = Reporter()
        parser_hh = ParserHH(reporter=reporter)
        asyncio.create_task(parser_hh.start_pooling())
        await reporter.start_send()
        return []


@router.get("")
async def get_all(session: AsyncSession=Depends(get_async_session)):
    data = ["id", "name", "url", "salary", "is_no_exp", "is_remote", "employer", "is_active", "registered_at"]
    return await vac_repository.get_all_by_fields(session=session, data=data)



