from sqlalchemy import String, Date, Boolean, BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from database.db_initial import Base


class Challenges(Base):
    challenge_id: Mapped[int] = mapped_column(BigInteger, nullable=False, unique=True)
    text_challenge: Mapped[str] = mapped_column(String, nullable=False)
    is_ended: Mapped[bool] = mapped_column(Boolean, default=False)
    date_create: Mapped[Date] = mapped_column(Date, nullable=False)
    date_of_end: Mapped[Date] = mapped_column(Date, nullable=False)


class Comments(Base):
    comment_id: Mapped[int] = mapped_column(BigInteger, nullable=False, unique=True)
    challenge_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    challenge_name: Mapped[str] = mapped_column(String, nullable=False)
    full_name: Mapped[str] = mapped_column(String, nullable=False)
    club_name: Mapped[str] = mapped_column(String, nullable=False)
    role: Mapped[str] = mapped_column(String, nullable=False)
    result: Mapped[str] = mapped_column(String, nullable=False)
    time_of_execution: Mapped[str] = mapped_column(String, nullable=False)
    video_link: Mapped[str] = mapped_column(String, nullable=False)
    comment_text: Mapped[str] = mapped_column(String, nullable=False)
    is_answered: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    comment_answer: Mapped[str] = mapped_column(String, nullable=True)
