import asyncio
import logging

from grpc_utils_parser.grpc_connection import send_grpc_to_tg
from models.schemas import ConstructVacancy
from repo_parser.utils import connection
from models.models import sub_repository, vac_repository


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
            if el.get("sub_tag").lower() in vacancy_name.lower():
                await asyncio.gather(*(send_grpc_to_tg(**el) for el in res), )
                count += 1
        logging.info(f"send {count} matches")
    else:
        logging.info(f"No matches")


@connection
async def hh_pusher_to_db(new_vac=None, session=None):
    vac = ConstructVacancy(url=new_vac[0], name=new_vac[1], salary=new_vac[2], is_no_exp=new_vac[3],
                           is_remote=new_vac[4], employer=new_vac[5], location=new_vac[6])
    vacancy_filter = {
        "url": new_vac[0],
        "name": new_vac[1],
    }
    res = await vac_repository.get_all_by_fields(session=session, data=["id"], field_filter=vacancy_filter)
    if not res:
        await vac_repository.add_object(session=session, data=vac.model_dump())
        logging.info(f"Add new vacancy")
        return True
    else:
        logging.info(f"Vacancy was already add")
        return False

