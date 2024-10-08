import asyncio
import logging

from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.posts.models import VacancyRepository
from src.posts.schemas import ConstructVacancy


async def hh_pusher_to_db(new_vac=None):
    async for session in get_async_session():
        if not new_vac:
            return None
        logging.info(f"Find new vacancy")
        vac = ConstructVacancy(url=new_vac[0], name=new_vac[1], salary=new_vac[2], experience=new_vac[3],
                               employer=new_vac[4], location=new_vac[5]).model_dump()
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


