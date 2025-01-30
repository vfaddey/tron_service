from abc import ABC, abstractmethod

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import WalletRequest


class WalletRepository(ABC):
    @abstractmethod
    async def create(self, wallet):
        raise NotImplementedError

    async def get_page(self,
                       page: int,
                       size: int):
        raise NotImplementedError


class SqlaWalletRepository(WalletRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create(self, wallet: WalletRequest) -> WalletRequest:
        try:
            self._session.add(wallet)
            await self._session.commit()
            await self._session.refresh(wallet)
            return wallet
        except SQLAlchemyError:
            await self._session.rollback()
            raise FailedToInsert('Произошла ошибка при сохранении запроса')


    async def get_page(self,
                       page: int,
                       size: int):
        stmt = select(WalletRequest).order_by(WalletRequest.timestamp.desc()).offset((page - 1) * size).limit(size)
        result = await self._session.execute(stmt)
        return result.unique().scalars().all()


class FailedToInsert(Exception):
    ...