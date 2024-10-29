import asyncio
import logging
from threading import Lock

from grpc_utils.utils import send_grpc_to_tg
from vacancy.models import vac_repository
from repository.utils import connection
from subscriber.models import sub_repository
from subscriber.utils import bot


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
        self.is_run = False
        self.background_tasks = set()

    def start_send(self) -> None:
        if not self.is_run:
            task = asyncio.create_task(self.check_updates())
            self.background_tasks.add(task)
            task.add_done_callback(self.background_tasks.discard)
            self.is_run = True

    @connection
    async def check_updates(self, session=None) -> None:
        sub_list = await sub_repository.get_all_by_fields(session=session,
                                                          data=["sub_tag", "is_no_exp", "is_remote", "user_tg_id"])
        if sub_list:
            for sub in sub_list:
                res = await self.find_post(session=session, target=sub.sub_tag,
                                           is_no_exp=sub.is_no_exp, is_remote=sub.is_remote)
                if res:
                    for el in res:
                       await send_grpc_to_tg(tg_user_id=sub.user_tg_id, text=f"{el.name}\n"
                                                                       f"{el.url}\n"
                                                                       f"{el.salary}\n"
                                                                       f"{el.employer}")
                    logging.info(f"Send {len(res)} message matching old")
                else:
                    logging.info("Send no message matching old")

    @staticmethod
    async def find_post(session, target: str, is_no_exp: bool, is_remote: bool):
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
