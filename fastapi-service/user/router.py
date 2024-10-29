import grpc
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from grpc_service import message_pb2_grpc, message_pb2
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
        raise HTTPException(status_code=400, detail="Данный пользователь уже зарегистрирован")
    else:
        return await user_repository.add_object(session=session, data=data.model_dump())



@router.post("/send_grpc_message")
async def get_last_messages(text: str):
    async with grpc.aio.insecure_channel('localhost:50051') as channel:
        stub = message_pb2_grpc.MessageServiceStub(channel)
        for el in range(10):
            response = await stub.SendMessage(message_pb2.Message(text=f"elem {str(el)}"))
    return response.text

