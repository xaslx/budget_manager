from app.models.base import Base
from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column




class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str]
    registered_at: Mapped[DateTime] = mapped_column(DateTime)

