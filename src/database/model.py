from datetime import datetime
from sqlalchemy import ARRAY, Column, DateTime, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Table(Base):
    __tablename__ = "Document"

    id = Column(Integer, primary_key=True)
    text = Column(String)
    created_date = Column(DateTime, default=datetime.now)
    rubrics = Column(ARRAY(String))
