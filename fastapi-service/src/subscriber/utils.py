import asyncio
import logging

from grpc_utils.grpc_connection import send_grpc_to_tg
from vacancy.models import vac_repository
from repository.utils import connection



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
        await asyncio.gather(*(send_grpc_to_tg(name=el.name,
                                               url=el.url,
                                               salary=el.salary,
                                               employer=el.employer,
                                               tg_user_id=sub_id, ) for el in res), )
        logging.info(f"send {len(res)} matches")
    else:
        logging.info(f"No matches")



