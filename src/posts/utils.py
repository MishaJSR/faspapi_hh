import asyncio
import logging

from sqlalchemy.ext.asyncio import AsyncSession

from src.posts.models import VacancyRepository
from src.posts.schemas import ConstructVacancy
from src.workers.ParserHH import ParserHH


async def hh_pusher_to_db(session: AsyncSession):
    lst_of_vacancies = []
    while True:
        counter = 0
        logging.info("Search new vacancies")
        lst_vacancies_parser = ParserHH().lst_of_vacancies
        new_vac = [item for item in lst_vacancies_parser if item not in lst_of_vacancies]
        if new_vac:
            lst_of_vacancies = lst_vacancies_parser
        logging.info(f"Find {len(new_vac)} new vacancies")
        for val in new_vac:
            new_vac = ConstructVacancy(url=val[0], name=val[1], salary=val[2], experience=val[3],
                                       employer=val[4], location=val[5]).model_dump()
            vacancy_filter = {
                "url": val[0],
                "name": val[1],
            }
            res = await VacancyRepository().get_all_by_fields(session=session, data=["id"], field_filter=vacancy_filter)
            if not len(res):
                counter += 1
                await VacancyRepository().add_object(session=session, data=new_vac)
        logging.info(f"Add {counter} new vacancies")
        await asyncio.sleep(30)