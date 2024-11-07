from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse

from user.models import user_repository
from user.schemas import ConstructUser, ResponseAllUsers
from database import get_async_session

router = APIRouter(
    prefix="/user",
    tags=["User"]
)


@router.post("/check_or_create")
async def get_last_messages(data = Depends(ConstructUser),
                            session = Depends(get_async_session)) -> int | HTTPException:
    field_filter = {
        "tg_user_id": data.tg_user_id
    }
    res = await user_repository.get_one_by_fields(session=session, data=["id", "tg_user_id"], field_filter=field_filter)
    if res:
        raise HTTPException(status_code=400, detail="Данный пользователь уже зарегистрирован")
    else:
        try:
            result = await user_repository.add_object(session=session, data=data.model_dump())
            return result
        except:
            raise HTTPException(status_code=400, detail="Данный пользователь уже зарегистрирован")


@router.post("/remove_user")
async def get_last_messages(tg_user_id: int,
                            session: AsyncSession = Depends(get_async_session)) -> JSONResponse | HTTPException:
    delete_filter = {
        "tg_user_id": tg_user_id
    }
    res = await user_repository.delete_fields(session=session, delete_filter=delete_filter)
    if res:
        return JSONResponse(content={"message": "Пользователь удален"}, status_code=200)
    else:
        raise HTTPException(status_code=400, detail="Данный пользователь не найден")


@router.get("/")
async def get_all_users(session: AsyncSession = Depends(get_async_session)) -> list[ResponseAllUsers]:
    res = await user_repository.get_all_by_fields(session=session, data=["id", "tg_user_id", "is_block_bot", "is_auth"])
    if res:
        return [ResponseAllUsers(user_id=obj.id, tg_user_id=obj.tg_user_id, is_block_bot=obj.is_block_bot)
                    for obj in res]
    else:
        return []


