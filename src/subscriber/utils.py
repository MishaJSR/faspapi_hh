import logging

from src.database import get_async_session
from src.posts.models import VacancyRepository
from src.subscriber.models import SubscriberRepository


async def send_first_matches_by_vac(target: str, is_no_exp: bool, is_remote: bool):
    async for session in get_async_session():
        filed_filter = {
            "name": target,
            "is_no_exp": is_no_exp,
            "is_remote": is_remote
        }
        res = await VacancyRepository().get_all_by_fields(session=session,
                                                          data=["name", "url", "salary", "is_no_exp",
                                                                "is_remote", "employer", "location"],
                                                          field_filter=filed_filter)
        if res:
            logging.info(f"send {len(res)} matches")
        else:
            logging.info(f"No matches")


async def send_first_matches_by_sub(target: str, is_no_exp: bool, is_remote: bool):
    async for session in get_async_session():
        filed_filter = {
            "sub_tag": target,
            "is_no_exp": is_no_exp,
            "is_remote": is_remote
        }
        res = await SubscriberRepository().get_all_by_fields(session=session, data=["user_tg_id"],
                                                             field_filter=filed_filter)
        if res:
            logging.info(f"send {len(res)} matches")
        else:
            logging.info(f"No matches")
