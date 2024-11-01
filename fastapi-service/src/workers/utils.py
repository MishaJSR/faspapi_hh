import logging

from grpc_utils.utils import send_grpc_to_tg
from repository.utils import connection
from subscriber.models import sub_repository
from vacancy.models import vac_repository
from vacancy.schemas import ConstructVacancy


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


@connection
async def hh_pusher_to_db(new_vac=None, session=None):
    logging.info(f"Find new vacancy")
    vac = ConstructVacancy(url=new_vac[0], name=new_vac[1], salary=new_vac[2], is_no_exp=new_vac[3],
                           is_remote=new_vac[4], employer=new_vac[5], location=new_vac[6]).model_dump()
    vacancy_filter = {
        "url": new_vac[0],
        "name": new_vac[1],
    }
    res = await vac_repository.get_all_by_fields(session=session, data=["id"], field_filter=vacancy_filter)
    if not res:
        await vac_repository.add_object(session=session, data=vac)
        logging.info(f"Add new vacancy")
        return True
    else:
        logging.info(f"Vacancy was already add")
        return False





@connection
async def send_sub_matches_by_vac(new_vac=None, session=None):
    logging.info(f"Find new vacancy")
    vac = ConstructVacancy(url=new_vac[0], name=new_vac[1], salary=new_vac[2], is_no_exp=new_vac[3],
                           is_remote=new_vac[4], employer=new_vac[5], location=new_vac[6]).model_dump()
    vacancy_filter = {
        "url": new_vac[0],
        "name": new_vac[1],
    }
    res = await vac_repository.get_all_by_fields(session=session, data=["id"], field_filter=vacancy_filter)
    if not res:
        await vac_repository.add_object(session=session, data=vac)
        logging.info(f"Add new vacancy")
    else:
        logging.info(f"Vacancy was already add")