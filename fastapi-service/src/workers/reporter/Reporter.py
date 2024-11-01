import logging

from grpc_utils.utils import send_grpc_to_tg
from workers.utils import send_first_matches_by_sub
from vacancy.models import vac_repository
from repository.utils import connection
from subscriber.models import sub_repository
from vacancy.utils import hh_pusher_to_db
from workers.hh.Observer import Observer, Subject, SingletonMeta


class Reporter(Observer, metaclass=SingletonMeta):
    def __init__(self) -> None:
        self.is_run = False
        self.background_tasks = set()

    def __str__(self) -> str:
        return "Reporter"

    async def update(self, subject: Subject) -> None:
        logging.info(subject.new_links)
        logging.info(f"Reporter: Reacted to the event, get {len(subject.new_links)} items")
        for link in subject.new_links:
            is_new = await hh_pusher_to_db(new_vac=link)
            if is_new:
                await send_first_matches_by_sub(link=link)

    async def start_send(self) -> None:
        if not self.is_run:
            await self.check_updates()
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
