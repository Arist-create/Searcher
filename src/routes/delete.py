import http

from fastapi import Depends

from src.database.main_db import Database
from src.responses.main_resp import Response
from src.routes.search import router


@router.delete(
    "/delete/{id}",
    summary="Удаление по id",
    status_code=http.HTTPStatus.OK,
    tags=["Удаление"],
)
async def delete_req(id, db=Depends(Database.get_db)):
    return await Response.delete(id, db)
