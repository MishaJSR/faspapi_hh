from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.models import UserRepository
from src.auth.schemas import ConstructUser
from src.database import get_async_session

router = APIRouter(
    prefix="/user",
    tags=["User"]
)


@router.post("/check_or_create")
async def get_last_messages(tg_user_id: int, user_tag: str, session: AsyncSession = Depends(get_async_session)):
    user_repo = UserRepository()
    field_filter = {
        "tg_user_id": tg_user_id
    }
    res = await user_repo.get_one_by_fields(session=session, data=["id", "tg_user_id"], field_filter=field_filter)
    if res:
        return res
    else:
        res = await user_repo.add_object(session=session, data=ConstructUser(tg_user_id=tg_user_id,
                                                                             user_tag=user_tag,
                                                                             is_block_bot=False).model_dump())
        return res

