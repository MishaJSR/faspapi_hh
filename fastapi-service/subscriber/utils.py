import logging

from grpc_utils.utils import send_grpc_to_tg
from vacancy.models import vac_repository
from repository.utils import connection
from subscriber.models import sub_repository

from base_settings import base_settings
from telegram import Bot

bot = Bot(token=base_settings.get_api_token())


@connection
async def send_first_matches_by_vac(session=None, target: str = None, is_no_exp: bool = None,
                                    is_remote: bool = None, sub_id: int = None):
    filed_filter = {
        "is_no_exp": is_no_exp,
        "is_remote": is_remote
    }
    contain_field = {
        "name": target.lower(),
    }
    res = await vac_repository.get_all_by_one_contain_field(
        session=session,
        data=["name", "url", "salary", "is_no_exp", "is_remote", "employer", "location"],
        field_filter=filed_filter,
        contain_field=contain_field
    )
    if res:
        for vac in res:
            await send_grpc_to_tg(tg_user_id=sub_id, text=f"{vac.name}\n"
                                                          f"{vac.url}\n"
                                                          f"{vac.salary}\n"
                                                          f"{vac.employer}")
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
    res = await sub_repository.get_all_by_fields(
        session=session,
        data=["user_tg_id", "sub_tag"],
        filed_filter=filed_filter)
    if res:
        count = 0
        for el in res:
            if el.sub_tag.lower() in vacancy_name.lower():
                await send_grpc_to_tg(tg_user_id=el.user_tg_id, text=f"{el.name}\n"
                                                                     f"{el.url}\n"
                                                                     f"{el.salary}\n"
                                                                     f"{el.employer}")
                count += 1
        logging.info(f"send {count} matches")
    else:
        logging.info(f"No matches")
