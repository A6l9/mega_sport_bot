from sqlalchemy import String, Date, Boolean, BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from database.db_initial import Base


class Challenges(Base):
    challenge_id: Mapped[int] = mapped_column(BigInteger, nullable=False, unique=True)
    text_challenge: Mapped[str] = mapped_column(String, nullable=False)
    is_ended: Mapped[bool] = mapped_column(Boolean, default=False)
    date_create: Mapped[Date] = mapped_column(Date, nullable=False)
    date_of_end: Mapped[Date] = mapped_column(Date, nullable=False)


class CommentsAnswers(Base):
    ...
