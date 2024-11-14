from datetime import datetime
from math import trunc

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from vacancy.models import vac_repository
from vacancy.schemas import VacPaginationModel, ResponseAllVac

router = APIRouter(
    prefix="/vacancy",
    tags=["Posts"]
)



@router.get("/", response_model=list[ResponseAllVac])
async def get_all(data=Depends(VacPaginationModel), session: AsyncSession=Depends(get_async_session)):
    load_fields = ["id", "name", "url", "salary", "is_no_exp", "is_remote", "employer", "location",
                   "is_active", "registered_at"]
    res = await vac_repository.get_all_by_fields(session=session, data=load_fields,
                                                  offset=data.offset, limit=data.limit)
    return [ResponseAllVac(**obj) for obj in res]
