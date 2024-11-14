from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from subscriber.models import sub_repository
from subscriber.schemas import ConstructSubscriber, ResponseAllSubs, ResponseUpdateSubs, SubPaginationModel, \
    DeleteSubSchema, ResponseDeleteSubSchema
from subscriber.utils import send_first_matches_by_vac
from user.models import user_repository

router = APIRouter(
    prefix="/sub",
    tags=["Subscribers"]
)


@router.post("/subscribe_user", response_model=ResponseUpdateSubs)
async def subscribe_user(data=Depends(ConstructSubscriber), session: AsyncSession = Depends(get_async_session)):
    user = await user_repository.get_all_by_fields(session=session, data=["id", "tg_user_id"],
                                                   field_filter={
                                                       "tg_user_id": data.user_tg_id
                                                   },
                                                   is_one=True)
    if not user:
        raise HTTPException(status_code=400, detail="Невозможно открыть подписку, пользователь отсутствует")

    active_sub = await sub_repository.get_all_by_fields(session=session, data=["id", "user_tg_id"],
                                                        field_filter={
                                                            "user_tg_id": data.user_tg_id
                                                        },
                                                        is_one=True)
    if not active_sub:
        sub = await sub_repository.add_object(session=session, data=data.model_dump())
    else:
        sub = await sub_repository.update_fields(session=session,
                                                 update_data=data.model_dump(),
                                                 update_filter={
                                                     "user_tg_id": data.user_tg_id,
                                                 },
                                                 is_one=True)
    if sub:
        await send_first_matches_by_vac(**data.model_dump())
        return ResponseUpdateSubs(**sub)
    else:
        raise HTTPException(status_code=400, detail="Невозможно открыть подписку")


@router.get("", response_model=list[ResponseAllSubs])
async def get_all(data=Depends(SubPaginationModel), session: AsyncSession = Depends(get_async_session)) -> list[ResponseAllSubs]:
    data_load = ["id", "sub_tag", "is_no_exp", "is_remote", "user_tg_id"]
    res = await sub_repository.get_all_by_fields(session=session, data=data_load,
                                                 offset=data.offset, limit=data.limit)
    if res:
        return [ResponseAllSubs(**obj) for obj in res]
    else:
        return []


@router.post("/delete_sub", response_model=ResponseDeleteSubSchema)
async def delete_sub(data=Depends(DeleteSubSchema), session: AsyncSession = Depends(get_async_session)):
    delete_filter = {
        "user_tg_id": data.tg_user_id
    }
    res = await sub_repository.delete_fields(session=session, delete_filter=delete_filter, is_one=True)
    if res:
        return ResponseDeleteSubSchema(**res)
    else:
        raise HTTPException(status_code=400, detail="Данный пользователь не найден")
