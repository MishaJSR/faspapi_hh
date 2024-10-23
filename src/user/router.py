from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from user.models import user_repository
from user.schemas import ConstructUser
from database import get_async_session

router = APIRouter(
    prefix="/user",
    tags=["User"]
)


@router.post("/check_or_create")
async def get_last_messages(data=Depends(ConstructUser), session: AsyncSession = Depends(get_async_session)) -> int:
    field_filter = {
        "tg_user_id": data.tg_user_id
    }
    res = await user_repository.get_one_by_fields(session=session, data=["id", "tg_user_id"], field_filter=field_filter)
    if res:
        return res
    else:
        return await user_repository.add_object(session=session, data=data.model_dump())
