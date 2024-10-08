import asyncio
import logging
from threading import Lock

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.posts.models import VacancyRepository
from src.subscriber.models import SubscriberRepository


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
        self.sub_repo = SubscriberRepository()
        self.vac_repo = VacancyRepository()
        self.is_run = False

    def start_send(self) -> None:
        if not self.is_run:
            asyncio.create_task(self.check_updates())

    async def check_updates(self) -> None:
        sub_list = []
        async for session in get_async_session():
            sub_list = await self.sub_repo.get_all_by_fields(session=session,
                                                             data=["sub_tag", "sub_addition", "user_tg_id"])
        for sub in sub_list:
            res = await self.find_post(target=sub.sub_tag, additions=sub.sub_addition)
            if res:
                logging.info(f"Send {len(res)} message matching old")
            else:
                logging.info("Send no message matching old")
        pass

    async def find_post(self, target: str, additions: str = ""):
        async for session in get_async_session():
            filed_filter = {
                "name": target.lower()
            }
            if additions:
                filed_filter["experience"] = additions.lower()
            res = await self.vac_repo.get_all_contain_fields(session=session,
                                                             data=["name", "url", "salary", "experience",
                                                                   "employer", "location"],
                                                             field_filter=filed_filter)
            return res
