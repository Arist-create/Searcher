from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.database.main_db import Database
from src.elastic.main_es import Elastic
from src.routes import delete, search

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def on_startup():
    await Database.init_db()
    await Database.import_csv()
    await Elastic.fill()


app.include_router(search.router)
app.include_router(delete.router)
