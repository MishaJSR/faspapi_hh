from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from vacancy.models import vac_repository

router = APIRouter(
    prefix="/vacancy",
    tags=["Posts"]
)



@router.get("")
async def get_all(session: AsyncSession=Depends(get_async_session)):
    data = ["id", "name", "url", "salary", "is_no_exp", "is_remote", "employer", "is_active", "registered_at"]
    return await vac_repository.get_all_by_fields(session=session, data=data)



