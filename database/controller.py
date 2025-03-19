from typing import Any, Union

from sqlalchemy.orm import Query
from sqlalchemy import update
from sqlalchemy.exc import (IntegrityError, OperationalError, 
                            StatementError, TimeoutError, InvalidRequestError)

from loader import logger
from database.db_initial import async_engine, async_session, Base
from database.models import Challenges, CommentsAnswers


class DatabaseInterface:

    def __init__(self):

        self.base = Base
        self.async_engine = async_engine
        self.async_session = async_session
    
    async def initial(self) -> None:
        async with self.async_engine.begin() as conn:
            await conn.run_sync(self.base.metadata.create_all)

    async def add_row(self, model: Any, **kwargs) -> Base:
        async with self.async_session() as session:
            row = model(**kwargs)
            session.add()
            try:
                await session.commit()
                return row
            except (IntegrityError, OperationalError, 
                    StatementError, TimeoutError, InvalidRequestError) as exc:
                logger.exception(f"Database error {exc}")
                logger.debug(f"Failed adding {model.__tablename__}")
                await session.rollback()

    async def get_row(self, model: Any, to_many: bool=False, order_by="id", **kwargs) -> Union[list[Base], Base]:
        async with self.async_session() as session:
            row = await session.execute(Query(model).filter_by(**kwargs).order_by(order_by))
            if to_many:
                result = [*row.scalars()]
            else: 
                result = row.scalar()
            return result
    
    async def change_row(self, model: Union[Challenges, CommentsAnswers], id: int, **kwargs) -> None:
        async with self.async_session() as session:
            await session.execute(update(model).where(model.id == id).values(**kwargs))
        
            try:
                await session.commit()
            except (IntegrityError, OperationalError, 
                    StatementError, TimeoutError, InvalidRequestError) as exc:
                logger.exception(f"Database error {exc}")
                logger.debug(f"Failed update {model.__tablename__}")
                await session.rollback()
    
    async def change_challenges_status(self, challenge_ids: list, status: bool) -> None:
        async with self.async_session() as session:
            await session.execute(update(Challenges).where(Challenges.id.in_(challenge_ids)).values(status=status))
        
            try:
                await session.commit()
            except (IntegrityError, OperationalError, 
                    StatementError, TimeoutError, InvalidRequestError) as exc:
                logger.exception(f"Database error {exc}")
                logger.debug(f"Failed update {Challenges.__tablename__}")
                await session.rollback()
