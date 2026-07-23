from dependency_injector import containers, providers

from core.config.settings import DatabaseSettings
from core.db.session import create_engine, create_session_factory


class CoreContainer(containers.DeclarativeContainer):
    db_settings = providers.Singleton(DatabaseSettings)

    engine = providers.Singleton(create_engine, db_settings.provided.db_url)

    session_factory = providers.Singleton(create_session_factory, engine)