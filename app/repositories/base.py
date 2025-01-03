from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TypeVar
from sqlalchemy.ext.asyncio import AsyncSession


MT = TypeVar('MT')




@dataclass
class BaseRepository(ABC):
    model: MT
    session: AsyncSession


    @abstractmethod
    async def add(self, **data) -> int:
        ...

    @abstractmethod
    async def find_one_or_none(self, **filter) -> MT | None:
        ...

    
    @abstractmethod
    async def find_all(self, **filter):
        ...

    @abstractmethod
    async def delete(self, **filter):
        ...