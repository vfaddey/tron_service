from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import AsyncSessionFactory
from src.repositories.wallet_repository import WalletRepository, SqlaWalletRepository
from src.services.wallet_service import WalletService
from src.adapters import tron_client


async def get_session() -> AsyncSession:
    async with AsyncSessionFactory() as session:
        try:
            yield session
            await session.commit()
        except:
            await session.rollback()
            raise
        finally:
            await session.close()


async def get_wallet_repository(session: AsyncSession = Depends(get_session)) -> SqlaWalletRepository:
    return SqlaWalletRepository(session)


async def get_wallet_service(wallet_repository: WalletRepository = Depends(get_wallet_repository)) -> WalletService:
    return WalletService(wallet_repository, tron_client)

