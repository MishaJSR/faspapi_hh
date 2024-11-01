import asyncio
import logging

from grpc_utils.utils import send_grpc_to_tg
from workers.utils import send_first_matches_by_sub
from models.models import vac_repository
from repository.utils import connection
from models.models import sub_repository
from workers.utils import hh_pusher_to_db
from workers.hh.Observer import Observer, Subject, SingletonMeta


class Reporter(Observer, metaclass=SingletonMeta):
    def __init__(self) -> None:
        pass

    def __str__(self) -> str:
        return "Reporter"

    @staticmethod
    async def update(subject: Subject) -> None:
        logging.info(f"Reporter: Reacted to the event, get {len(subject.new_links)} items")
        for link in subject.new_links:
            is_new = await hh_pusher_to_db(new_vac=link)
            if is_new:
                await send_first_matches_by_sub(link=link)

    @classmethod
    @connection
    async def check_updates(cls, session=None) -> None:
        logging.info("Start Reporter notify")
        sub_list = await sub_repository.get_all_by_fields(session=session,
                                                          data=["sub_tag", "is_no_exp", "is_remote", "user_tg_id"])
        if sub_list:
            for sub in sub_list:
                res = await cls.find_post(session=session, target=sub.sub_tag,
                                          is_no_exp=sub.is_no_exp, is_remote=sub.is_remote)
                if res:
                    logging.info(f"Start GRPC sending...")
                    await asyncio.gather(*(send_grpc_to_tg(name=el.name,
                                                           url=el.url,
                                                           salary=el.salary,
                                                           employer=el.employer,
                                                           tg_user_id=sub.user_tg_id, ) for el in res), )
                    logging.info(f"Send {len(res)} old matcher by GRPC for user {sub.user_tg_id}")
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
