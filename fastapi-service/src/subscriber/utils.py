import asyncio
import logging
from typing import Union

from grpc_utils.grpc_connection import send_grpc_to_tg
from vacancy.models import vac_repository


async def send_first_matches_by_vac(session=None, sub_tag: str = None, is_no_exp: bool = None,
                                    is_remote: bool = None, user_tg_id: str = None):
    filed_filter = {
        "is_no_exp": is_no_exp,
        "is_remote": is_remote
    }
    contain_field = {
        "name": sub_tag.lower(),
    }
    res = await vac_repository.get_all_by_one_contain_field(
        session=session,
        data=["name", "url", "salary", "is_no_exp", "is_remote", "employer", "location"],
        field_filter=filed_filter,
        contain_field=contain_field
    )
    if res:
        await asyncio.gather(*(send_grpc_to_tg(**el, user_tg_id=user_tg_id) for el in res))
        logging.info(f"send {len(res)} matches for {user_tg_id}")
    else:
        logging.info(f"No matches for {user_tg_id}")


async def add_or_update_sub(session=None, data: dict = None, repo=None, active_sub: list = None) -> Union[dict, list]:
    if not active_sub:
        sub = await repo.add_object(session=session, data=data)
        logging.info(f"Create sub with target {data.get("sub_tag")} for id: {sub.get("id")}")
    else:
        sub = await repo.update_fields(session=session,
                                                 update_data=data,
                                                 update_filter={
                                                     "user_tg_id": data.get("user_tg_id"),
                                                 },
                                                 is_one=True)
        logging.info(f"Update sub with target {data.get("sub_tag")} for id: {sub.get("id")}")
    await send_first_matches_by_vac(**data, session=session)
    return sub



