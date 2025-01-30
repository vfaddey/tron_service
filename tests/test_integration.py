import pytest
from httpx import AsyncClient
from src.schemas.wallet import WalletRequestSchema

@pytest.mark.asyncio
async def test_post_wallet(async_client: AsyncClient, wallet_service, tron_client_mock):
    tron_client_mock.get_account.return_value = {
        "balance": 1000000
    }
    tron_client_mock.get_account_resource.return_value = {
        "TotalNetLimit": 1000,
        "TotalEnergyLimit": 500
    }

    test_address = "TXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

    response = await async_client.post("/wallets", json={"address": test_address})
    assert response.status_code == 201
    data = response.json()
    assert data["address"] == test_address
    assert data["bandwidth"] == 1000
    assert data["energy"] == 500
    assert data["trx_balance"] == 1.0

@pytest.mark.asyncio
async def test_get_wallets(async_client: AsyncClient):
    response = await async_client.get("/wallets?page=1&size=10")
    assert response.status_code == 200
    data = response.json()
    assert "total" in data
    assert "page" in data
    assert "size" in data
    assert "records" in data
    assert isinstance(data["records"], list)
