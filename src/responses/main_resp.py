from fastapi.responses import JSONResponse

from src.database.main_db import Database
from src.elastic.main_es import Elastic


class Response:
    async def search(query, db):
        arr = await Elastic.search(query)
        if len(arr) == 0:
            return JSONResponse(
                content={
                    "detail": "no matches found",
                },
                status_code=404,
            )
        else:
            arr = await Database.search(db, arr)
            resp = [
                {
                    "id": i.id,
                    "text": i.text,
                    "created_date": i.created_date,
                    "rubrics": i.rubrics,
                }
                for i in arr
            ]
            return resp

    async def delete(id, db):
        await Elastic.delete(id)
        if await Database.delete(db, id):
            return JSONResponse(
                content={
                    "success": "the record was successfully deleted"
                },
                status_code=200,
            )
        else:
            return JSONResponse(
                content={"detail": "there is no record with this id"},
                status_code=404,
            )
