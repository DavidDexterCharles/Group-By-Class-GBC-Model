# pylint: disable=C0115:missing-class-docstring,C0114:missing-module-docstring,C0301:line-too-long
# pylint: disable=W0612:unused-variable
# import asyncio
# from datetime import datetime
from sqlalchemy import Column, Integer, String#,Boolean, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base,engine

class Label(Base):
    __tablename__ = 'label'
    id = Column(Integer,primary_key=True,autoincrement=True)
    name = Column(String,nullable=False, unique=True)
    description = Column(String,nullable=False, unique=True)
    corpus_label = relationship("CorpusLabel", back_populates="label")

Base.metadata.create_all(engine)# by importing this class the sqlite db gets aautomatically created if it doesnt exists, possibly due to fastapi dependency injection system
# async def init_models(): #https://stackoverflow.com/a/74000761/5826992
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)
# asyncio.run(init_models())
