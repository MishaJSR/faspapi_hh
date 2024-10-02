import asyncio

from sqlalchemy.ext.asyncio import AsyncSession

from src.posts.models import VacancyRepository
from src.posts.schemas import ConstructVacancy
from src.workers.ParserHH import ParserHH


async def push_to_db(session: AsyncSession):
    while True:
        print("work")
        lst_vacancies = ParserHH().lst_of_vacancies
        for val in lst_vacancies:
            new_vac = ConstructVacancy(url=val[0], name=val[1], salary=val[2], experience=val[3],
                                       employer=val[4], location=val[5]).model_dump()
            vacancy_filter = {
                "url": val[0],
                "name": val[1],
            }
            res = await VacancyRepository().get_all_by_fields(session=session, data=["id"], field_filter=vacancy_filter)
            if not len(res):
                await VacancyRepository().add_object(session=session, data=new_vac)
        await asyncio.sleep(30)