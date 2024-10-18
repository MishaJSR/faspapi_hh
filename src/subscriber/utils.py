import logging
import re

from bot.bot import bot
from database import get_async_session
from posts.models import VacancyRepository
from repository.utils import connection
from subscriber.models import SubscriberRepository


@connection
async def send_first_matches_by_vac(session=None, target: str = None, is_no_exp: bool = None, is_remote: bool = None):
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


@connection
async def send_first_matches_by_sub(session=None, link: list = None):
    url, vacancy_name, salary, is_no_exp, is_remote, employer, location = link
    filed_filter = {
        "is_no_exp": is_no_exp,
        "is_remote": is_remote
    }
    res = await SubscriberRepository().get_all_by_fields(
        session=session,
        data=["user_tg_id", "sub_tag"],
        filed_filter=filed_filter)
    if res:
        count = 0
        for el in res:
            if el.sub_tag.lower() in vacancy_name.lower():
                await bot.send_message(chat_id=el.user_tg_id, text=f"{vacancy_name}\n"
                                                                   f"{url}\n"
                                                                   f"{salary}\n"
                                                                   f"{employer}")
                count += 1
        logging.info(f"send {count} matches")
    else:
        logging.info(f"No matches")
