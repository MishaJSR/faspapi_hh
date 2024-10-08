import asyncio

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.subscriber.models import SubscriberRepository
from src.subscriber.schemas import ConstructSubscriber
from src.subscriber.utils import send_first_matches_by_vac

router = APIRouter(
    prefix="/sub",
    tags=["Subscribers"]
)


@router.post("/subscribe_user")
async def subscribe_user(user_tg_id: int, target: str, is_no_exp: bool, is_remote: bool,
                         session: AsyncSession = Depends(get_async_session)):
    sub_repo = SubscriberRepository()
    field_filter = {
        "user_tg_id": user_tg_id
    }
    res = await sub_repo.get_one_by_fields(session=session, data=["id", "user_tg_id"], field_filter=field_filter)
    if not res:
        sub_id = await sub_repo.add_object(session=session,
                                           data=ConstructSubscriber(user_tg_id=user_tg_id,
                                                                    sub_tag=target,
                                                                    is_no_exp=is_no_exp,
                                                                    is_remote=is_remote).model_dump())
    else:
        update_filter = {
            "user_tg_id": user_tg_id,
        }
        update_data = {
            "sub_tag": target,
            "is_no_exp": is_no_exp,
            "is_remote": is_remote,
            "user_tg_id": user_tg_id,
        }
        sub_id = await sub_repo.update_fields(session=session, update_data=update_data, update_filter=update_filter)
    asyncio.create_task(send_first_matches_by_vac(target=target, is_no_exp=is_no_exp, is_remote=is_remote))
    return sub_id

