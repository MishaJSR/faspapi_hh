import logging

from vacancy.models import vac_repository
from vacancy.schemas import ConstructVacancy
from repository.utils import connection


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
