from sqlalchemy import Integer, Column
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, DeclarativeBase, declared_attr


from config import proj_settings


class Base(DeclarativeBase):

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
    
    id = Column(Integer, primary_key=True, nullable=False)

db_url = f"postgresql+asyncpg://{proj_settings.db_user}:{proj_settings.db_pass}" \
         f"@{proj_settings.db_host}:{proj_settings.db_port}/{proj_settings.db_name}"

async_engine = create_async_engine(db_url, pool_timeout=60, pool_size=900, max_overflow=100)
async_session = sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)
