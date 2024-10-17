import logging
import re

from bot.bot import bot
from database import get_async_session
from posts.models import VacancyRepository
from subscriber.models import SubscriberRepository


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
            "is_no_exp": is_no_exp,
            "is_remote": is_remote
        }
        contain_value = {
            "sub_tag": target
        }
        res = await SubscriberRepository().get_all_by_one_contain_value(
            session=session,
            data=["user_tg_id"],
            field_filter=filed_filter,
            contain_value=contain_value)
        if res:
            for el in res:
                await bot.send_message(chat_id=el.user_tg_id, text=target)
            logging.info(f"send {len(res)} matches")
        else:
            logging.info(f"No matches")
