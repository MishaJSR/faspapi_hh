import asyncio
import logging

from database import get_async_session
from posts.models import VacancyRepository
from posts.schemas import ConstructVacancy


async def hh_pusher_to_db(new_vac=None):
    async for session in get_async_session():
        if not new_vac:
            return None
        logging.info(f"Find new vacancy")
        vac = ConstructVacancy(url=new_vac[0], name=new_vac[1], salary=new_vac[2], is_no_exp=new_vac[3],
                               is_remote=new_vac[4], employer=new_vac[5], location=new_vac[6]).model_dump()
        vacancy_filter = {
            "url": new_vac[0],
            "name": new_vac[1],
        }
        res = await VacancyRepository().get_all_by_fields(session=session, data=["id"], field_filter=vacancy_filter)
        if not res:
            await VacancyRepository().add_object(session=session, data=vac)
            logging.info(f"Add new vacancy")
        else:
            logging.info(f"Vacancy was already add")
