from concurrent.futures import ThreadPoolExecutor
from decimal import Decimal

from tronpy import Tron

from src.models.wallet import WalletRequest
from src.repositories.wallet_repository import WalletRepository
from src.schemas.wallet import WalletResponse


class WalletService:
    def __init__(self,
                 wallet_repository: WalletRepository,
                 tron_client: Tron):
        self._wallet_repository = wallet_repository
        self._tron_client = tron_client

    async def process_wallet_request(self, address: str) -> WalletResponse:
        account = self._tron_client.get_account(address)
        account_resource = self._tron_client.get_account_resource(address)

        bandwidth = account_resource.get('TotalNetLimit', 0)
        energy = account_resource.get('TotalEnergyLimit', 0)
        balance = Decimal(account.get('balance', 0) / 1e6)
        to_insert = WalletRequest(address=address,
                                  trx_balance=balance,
                                  energy=energy,
                                  bandwidth=bandwidth)
        inserted = await self._wallet_repository.create(to_insert)
        return WalletResponse.from_orm(inserted)

    async def get_by_page(self, page: int, size: int) -> list[WalletResponse]:
        result = await self._wallet_repository.get_page(page, size)
        return [WalletResponse.from_orm(w) for w in result]
