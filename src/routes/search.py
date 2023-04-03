import http

from fastapi import APIRouter, Depends

from src.database.main_db import Database
from src.responses.main_resp import Response
from src.responses.models import RespModelSearch

router = APIRouter()


@router.get(
    "/search/{query}",
    summary="Поиск",
    status_code=http.HTTPStatus.OK,
    response_model=list[RespModelSearch],
    tags=["Поиск"],
)
async def search_req(query, db=Depends(Database.get_db)):
    return await Response.search(query, db)
