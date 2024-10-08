import logging

from src.database import get_async_session
from src.posts.models import VacancyRepository
from src.subscriber.models import SubscriberRepository


async def send_first_matches_by_vac(target: str, additions: str = ""):
    async for session in get_async_session():
        filed_filter = {
            "name": target.lower()
        }
        if additions:
            filed_filter["experience"] = additions.lower()
        res = await VacancyRepository().get_all_contain_fields(session=session,
                                                               data=["name", "url", "salary", "experience",
                                                                     "employer", "location"],
                                                               field_filter=filed_filter)
        if res:
            logging.info(f"send {len(res)} matches")
        else:
            logging.info(f"No matches")


async def send_first_matches_by_sub(target: str, additions: str = ""):
    async for session in get_async_session():
        filed_filter = {
            "sub_tag": target.lower(),
        }
        if additions:
            filed_filter["sub_addition"] = additions.lower()
        res = await SubscriberRepository().get_all_contain_fields(session=session, data=["user_tg_id"],
                                                                  field_filter=filed_filter)
        if res:
            logging.info(f"send {len(res)} matches")
        else:
            logging.info(f"No matches")
