from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse

from user.models import user_repository
from user.schemas import ConstructUser, ResponseAllUsers, UserCreateModel, ResponseDeleteUsers, UserPaginationModel
from database import get_async_session

router = APIRouter(
    prefix="/user",
    tags=["User"]
)


@router.post("/check_or_create", response_model=UserCreateModel)
async def get_last_messages(data=Depends(ConstructUser),
                            session=Depends(get_async_session)):
    field_filter = {
        "tg_user_id": data.tg_user_id
    }
    res = await user_repository.get_all_by_fields(session=session, data=["id", "tg_user_id"], field_filter=field_filter,
                                                  is_one=True)
    if res:
        raise HTTPException(status_code=400, detail="Данный пользователь уже зарегистрирован")
    try:
        result = await user_repository.add_object(session=session, data=data.model_dump())
        return UserCreateModel(id=result, tg_user_id=data.tg_user_id)
    except:
        raise HTTPException(status_code=505, detail="Ошибка в работе сервиса")



@router.post("/remove_user", response_model=list[ResponseDeleteUsers])
async def get_last_messages(data=Depends(ResponseDeleteUsers),
                            session: AsyncSession = Depends(get_async_session)):
    delete_filter = {
        "tg_user_id": data.tg_user_id
    }
    res = await user_repository.delete_fields(session=session, delete_filter=delete_filter)
    if res:
        return [ResponseDeleteUsers(**obj) for obj in res]
    else:
        raise HTTPException(status_code=400, detail="Данный пользователь не найден")


@router.get("/", response_model=list[ResponseAllUsers])
async def get_all_users(data=Depends(UserPaginationModel), session: AsyncSession = Depends(get_async_session)):
    res = await user_repository.get_all_by_fields(session=session, data=["id", "tg_user_id", "is_block_bot", "is_auth"],
                                                  offset=data.offset, limit=data.limit)
    return [ResponseAllUsers(**obj) for obj in res]
