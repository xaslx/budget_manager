from app.repositories.sqlalchemy import SQLAlchemyRepository
from dataclasses import dataclass




@dataclass
class UserRepository(SQLAlchemyRepository):
    ...

