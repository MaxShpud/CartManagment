from contextlib import asynccontextmanager
from logging.config import dictConfig
from typing import AsyncContextManager

from fastapi import FastAPI

from app.api import rest
from app.api.rest.controllers import init_rest_api
from app.config import Config
from app.containers import Container
from app.LOGGING import ctx, get_logging_config
import uvicorn


@asynccontextmanager
async def lifespan(app_: FastAPI) -> AsyncContextManager[None]:
    config = Config()
    dictConfig(
        config=get_logging_config(
            transaction_ctx=ctx,
            config=config.LOGGING,
        ),
    )
    async with Container.lifespan(wireable_packages=[rest]) as container:
        app_.container = container
        yield


app = FastAPI(lifespan=lifespan)

if __name__ == "__main__":
    uvicorn.run(init_rest_api(app), port=8000)
