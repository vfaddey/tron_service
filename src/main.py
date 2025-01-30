from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from src.api import wallet_router
from src.adapters import tron_client

from src.config import settings

app = FastAPI(
    title=settings.APP_NAME
)


app.include_router(wallet_router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



