import asyncio
from contextlib import asynccontextmanager
from functools import wraps
from logging.config import dictConfig
from typing import Callable, Any, AsyncContextManager

import typer

from app.api import cli
from app.config import Config
from app.containers import Container
from app.LOGGING import get_logging_config, ctx

app = typer.Typer()


def coro(func: Callable[..., Any]) -> Callable[..., Any]:
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        return asyncio.run(func(*args, **kwargs))

    return wrapper


@asynccontextmanager
async def container() -> AsyncContextManager[Container]:  # pragma: no cover
    config = Config()
    dictConfig(
        config=get_logging_config(
            transaction_ctx=ctx,
            config=config.LOGGING,
        ),
    )

    async with Container.lifespan(wireable_packages=[cli]) as cont:
        yield cont


app.container = container


@app.command()
def dummy() -> None:  # pragma: no cover
    print("dummy")  # noqa: T201


if __name__ == "__main__":
    app()
