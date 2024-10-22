import asyncio

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from subscriber.models import sub_repository
from subscriber.schemas import ConstructSubscriber
from subscriber.utils import send_first_matches_by_vac

router = APIRouter(
    prefix="/sub",
    tags=["Subscribers"]
)


@router.post("/subscribe_user")
async def subscribe_user(data=Depends(ConstructSubscriber), session: AsyncSession = Depends(get_async_session)):
    field_filter = {
        "user_tg_id": data.user_tg_id
    }
    res = await sub_repository.get_one_by_fields(session=session, data=["id", "user_tg_id"], field_filter=field_filter)
    if not res:
        sub_id = await sub_repository.add_object(session=session, data=data.model_dump())
    else:
        update_filter = {
            "user_tg_id": data.user_tg_id,
        }
        update_data = {
            "sub_tag": data.target,
            "is_no_exp": data.is_no_exp,
            "is_remote": data.is_remote,
            "user_tg_id": data.user_tg_id,
        }
        sub_id = await sub_repository.update_fields(session=session,
                                                    update_data=update_data,
                                                    update_filter=update_filter)
    if sub_id:
        asyncio.create_task(send_first_matches_by_vac(target=data.target,
                                                      is_no_exp=data.is_no_exp,
                                                      is_remote=data.is_remote))
        return sub_id
    else:
        raise HTTPException(status_code=400, detail="Данный пользователь отсутствует")
