import pytest
from decimal import Decimal
from src.models import WalletRequest
from src.repositories.wallet_repository import SqlaWalletRepository, FailedToInsert
from src.schemas.wallet import WalletRequestSchema
from sqlalchemy.exc import SQLAlchemyError

@pytest.mark.asyncio
async def test_create_wallet_request(async_session):
    """
    Тестирование метода create репозитория
    """
    repository = SqlaWalletRepository(async_session)
    wallet = WalletRequest(
        address="TXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
        trx_balance=Decimal("1.0"),
        energy=500,
        bandwidth=1000
    )

    inserted_wallet = await repository.create(wallet)

    assert inserted_wallet.id is not None
    assert inserted_wallet.address == wallet.address
    assert inserted_wallet.trx_balance == wallet.trx_balance
    assert inserted_wallet.energy == wallet.energy
    assert inserted_wallet.bandwidth == wallet.bandwidth

@pytest.mark.asyncio
async def test_create_wallet_request_failure(async_session, mocker):
    """
    Тестирование метода create репозитория при ошибке
    """
    repository = SqlaWalletRepository(async_session)
    wallet = WalletRequest(
        address="TXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
        trx_balance=Decimal("1.0"),
        energy=500,
        bandwidth=1000
    )

    # Мокаем метод commit для генерации исключения
    mocker.patch.object(async_session, 'commit', side_effect=SQLAlchemyError)

    with pytest.raises(FailedToInsert) as exc_info:
        await repository.create(wallet)

    assert str(exc_info.value) == 'Произошла ошибка при сохранении запроса'
