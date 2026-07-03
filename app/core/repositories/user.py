from typing import Optional
from abc import ABC, abstractmethod
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, delete, or_

from app.infostructure.db.sqlite.models.user import Users
from app.core.schemes.user import (
    UserCreateScheme,
    UserPrivateScheme,
    UserDTO
)


class AbstractUserRepository(ABC):
    _MODEL = None

    @abstractmethod
    async def get_by_id(self, user_id: UUID) -> Optional[UserPrivateScheme]:
        ...

    @abstractmethod
    async def get_existing(self, username: str, email: str) -> Optional[UserPrivateScheme]:
        ...

    @abstractmethod
    async def create(self, user: UserCreateScheme) -> UserPrivateScheme:
        ...

    @abstractmethod
    async def remove(self, user_id: UUID) -> None:
        ...


class SQLUserRepository(AbstractUserRepository):
    _MODEL = Users

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, user_id: UUID) -> Optional[UserPrivateScheme]:
        query = select(self._MODEL.id, self._MODEL.username, self._MODEL.email).filter(self._MODEL.id == user_id)

        result = (await self._session.execute(query)).mappings().one_or_none()

        if result:
            return UserPrivateScheme.model_validate(result)

        return None

    async def get_existing(self, username: str, email: str) -> Optional[UserPrivateScheme]:
        query = (
            select(self._MODEL.id, self._MODEL.username, self._MODEL.email)
            .filter(
                or_(
                    self._MODEL.username == username, 
                    self._MODEL.email == email
                )
            )
        )

        result = (await self._session.execute(query)).mappings().one_or_none()

        if result:
            return UserPrivateScheme.model_validate(result)
        
        return None

    async def create(self, user: UserCreateScheme) -> UserPrivateScheme:
        stmt = (
                insert(self._MODEL)
                .values(**UserDTO.from_create_scheme(user).model_dump())
                .returning(self._MODEL.id, self._MODEL.username, self._MODEL.email)
        )

        result = (await self._session.execute(stmt)).one()

        await self._session.commit()

        return UserPrivateScheme.model_validate(result)

    async def remove(self, user_id: UUID) -> None:
        query = delete(self._MODEL).filter(self._MODEL.id == user_id)
        
        await self._session.execute(query)
        await self._session.commit()


