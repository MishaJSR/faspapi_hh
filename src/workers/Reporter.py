import asyncio
import logging
from threading import Lock

from database import get_async_session
from posts.models import vac_repository
from subscriber.models import sub_repository
from bot.bot import bot


class ReporterMeta(type):
    _instances = {}
    _lock: Lock = Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]


class Reporter(metaclass=ReporterMeta):
    def __init__(self) -> None:
        self.is_run = True

    def start_send(self) -> None:
        if not self.is_run:
            asyncio.create_task(self.check_updates())

    async def check_updates(self) -> None:
        async for session in get_async_session():
            sub_list = await sub_repository.get_all_by_fields(session=session,
                                                             data=["sub_tag", "is_no_exp", "is_remote", "user_tg_id"])
            for sub in sub_list:
                res = await self.find_post(session=session, target=sub.sub_tag,
                                           is_no_exp=sub.is_no_exp, is_remote=sub.is_remote)
                if res:
                    for el in res:
                        await bot.send_message(chat_id=548349299, text=el.name)
                    logging.info(f"Send {len(res)} message matching old")
                else:
                    logging.info("Send no message matching old")

    async def find_post(self, session, target: str, is_no_exp: bool, is_remote: bool):
        filed_filter = {
            "is_no_exp": is_no_exp,
            "is_remote": is_remote
        }
        contain_field = {
            "name": target,
        }
        res = await vac_repository.get_all_by_one_contain_field(
            session=session,
            data=["name", "url", "salary", "is_no_exp", "is_remote", "employer", "location"],
            field_filter=filed_filter,
            contain_field=contain_field)
        return res
