import os

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import desc, or_, select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from src.database.model import Base, Table

load_dotenv()

database_path = os.getenv("DATABASE_URL_P")
engine = create_async_engine(database_path)


class Database:
    async def init_db():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def get_db() -> AsyncSession:
        async_session = sessionmaker(
            engine, class_=AsyncSession, expire_on_commit=False
        )
        async with async_session() as db:
            try:
                yield db
            finally:
                await db.close()

    async def import_csv():
        df = pd.read_csv("posts.csv")
        df["created_date"] = pd.to_datetime(df["created_date"])
        documents = df.to_dict(orient="records")
        db = AsyncSession(engine)
        for row in documents:
            record = Table(
                text=row["text"],
                created_date=row["created_date"],
                rubrics=[i for i in eval(row["rubrics"])],
            )
            db.add(record)
        await db.commit()
        await db.close()

    async def search(db, arr):
        result = await db.execute(
            select(Table)
            .filter(or_(Table.id.in_(arr)))
            .order_by(desc("created_date"))
        )
        arr = result.scalars().all()
        return arr

    async def delete(db, id):
        try:
            result = await db.execute(
                select(Table).filter(Table.id == int(id))
            )
            doc = result.scalars().one()
            await db.delete(doc)
            await db.commit()
            return True
        except:
            return False
