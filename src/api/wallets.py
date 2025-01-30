from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from tronpy.exceptions import AddressNotFound

from src.api.deps import get_wallet_service
from src.repositories.wallet_repository import FailedToInsert
from src.schemas.wallet import WalletRequestSchema, WalletResponse
from src.services.wallet_service import WalletService

router = APIRouter(prefix='/wallets', tags=['Wallets'])


@router.post('',
             response_model=WalletResponse,
             description='Получить и сохранить информацию по кошельку')
async def register_new_wallet_request(request: WalletRequestSchema,
                                      wallet_service: WalletService = Depends(get_wallet_service)):
    try:
        result = await wallet_service.process_wallet_request(**request.model_dump())
        return result
    except FailedToInsert as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    except AddressNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Address not found')


@router.get('',
            response_model=list[WalletResponse],
            description='Получить сохраненные кошельки')
async def list_wallets(page: int,
                       size: int = 10,
                       wallet_service: WalletService = Depends(get_wallet_service)):
    return await wallet_service.get_by_page(page, size)

