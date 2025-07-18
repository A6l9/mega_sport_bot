from typing import Any, Union

from sqlalchemy.orm import Query
from sqlalchemy import update
from sqlalchemy.exc import (IntegrityError, OperationalError, 
                            StatementError, TimeoutError, InvalidRequestError)

from load_services import logger
from database.db_initial import async_engine, async_session, Base


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
            session.add(row)
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
    
    async def change_row(self, model: Base, id: int, **kwargs) -> None:
        async with self.async_session() as session:
            await session.execute(update(model).where(model.id == id).values(**kwargs))
        
            try:
                await session.commit()
            except (IntegrityError, OperationalError, 
                    StatementError, TimeoutError, InvalidRequestError) as exc:
                logger.exception(f"Database error {exc}")
                logger.debug(f"Failed update {model.__tablename__}")
                await session.rollback()
    
    async def change_challenges_status(self, challenge_ids: list, status: bool, model: Base) -> None:
        async with self.async_session() as session:
            await session.execute(update(model).where(model.challenge_id.in_(challenge_ids)).values(is_ended=status))
        
            try:
                await session.commit()
            except (IntegrityError, OperationalError, 
                    StatementError, TimeoutError, InvalidRequestError) as exc:
                logger.exception(f"Database error {exc}")
                logger.debug(f"Failed update {model.__tablename__}")
                await session.rollback()

    async def change_comments_status_text_answer(self, comment_id: int, status: bool, comment_answer: str, model: Base) -> None:
        async with self.async_session() as session:
            await session.execute(update(model).where(model.comment_id == comment_id).values(is_answered=status, 
                                                                                                   comment_answer=comment_answer))
        
            try:
                await session.commit()
            except (IntegrityError, OperationalError, 
                    StatementError, TimeoutError, InvalidRequestError) as exc:
                logger.exception(f"Database error {exc}")
                logger.debug(f"Failed update {model.__tablename__}")
                await session.rollback()
