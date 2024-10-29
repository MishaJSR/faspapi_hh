import asyncio

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from database import get_async_session
from subscriber.models import sub_repository
from subscriber.schemas import ConstructSubscriber, ResponseAllSubs
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
            "sub_tag": data.sub_tag,
            "is_no_exp": data.is_no_exp,
            "is_remote": data.is_remote,
            "user_tg_id": data.user_tg_id,
        }
        sub_id = await sub_repository.update_fields(session=session,
                                                    update_data=update_data,
                                                    update_filter=update_filter)
    if sub_id:
        await send_first_matches_by_vac(target=data.sub_tag,
                                        is_no_exp=data.is_no_exp,
                                        is_remote=data.is_remote,
                                        sub_id=sub_id)
        return sub_id
    else:
        raise HTTPException(status_code=400, detail="Невозможно открыть подписку")


@router.get("")
async def get_all(session: AsyncSession = Depends(get_async_session)) -> list[ResponseAllSubs]:
    data = ["id", "sub_tag", "is_no_exp", "is_remote", "user_tg_id"]
    res = await sub_repository.get_all_by_fields(session=session, data=data)
    if res:
        response = [ResponseAllSubs(sub_id=obj.id, sub_tag=obj.sub_tag,
                                    is_no_exp=obj.is_no_exp,
                                    is_remote=obj.is_remote,
                                    user_tg_id=obj.user_tg_id, )
                    for obj in res]
        return response
    else:
        return []


@router.post("/delete_sub")
async def delete_sub(tg_user_id: int, session: AsyncSession = Depends(get_async_session)) -> list[ResponseAllSubs]:
    delete_filter = {
        "user_tg_id": tg_user_id
    }
    res = await sub_repository.delete_fields(session=session, delete_filter=delete_filter)
    if res:
        return JSONResponse(content={"message": "Пользователь удален"}, status_code=200)
    else:
        raise HTTPException(status_code=400, detail="Данный пользователь не найден")
