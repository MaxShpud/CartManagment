from contextlib import asynccontextmanager
from types import ModuleType
from typing import AsyncContextManager

from dependency_injector import containers, providers

from app.app_layer.use_cases.carts.create_cart import CreateCartUseCase
from app.app_layer.use_cases.carts.retrieve_cart import CartRetrieveUseCase
from app.config import Config
from app.infra.repositories.sqla.db import Database
from app.infra.unit_of_work.sqla import Uow


class DBContainer(containers.DeclarativeContainer):
    config = providers.Dependency(instance_of=Config)
    db = providers.Singleton(Database, config=config.provided.DB)
    uow = providers.Factory(Uow, session_factory=db.provided.session_factory)


class Container(containers.DeclarativeContainer):
    config = Config()

    db = providers.Container(DBContainer, config=config)

    create_cart_use_case = providers.Factory(
        CreateCartUseCase, uow=db.container.uow
    )

    cart_retrieve_use_case = providers.Factory(
        CartRetrieveUseCase, uow=db.container.uow
    )

    @classmethod
    @asynccontextmanager
    async def lifespan(
            cls, wireable_packages: list[ModuleType]
    ) -> AsyncContextManager["Container"]:
        container = cls()
        container.wire(packages=wireable_packages)

        #await container.init_resources()
        result = container.init_resources()
        if result:
            await result

        try:
            yield container
        finally:
            await container.shutdown_resources()
