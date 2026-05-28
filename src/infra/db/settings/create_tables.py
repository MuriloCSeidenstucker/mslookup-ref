# pylint: disable=W0611:unused-import

import logging

from sqlalchemy.exc import SQLAlchemyError

from src.infra.db.entities.drug_entity import DrugEntity
from src.infra.db.settings.base import Base
from src.infra.db.settings.connection import get_engine

logger = logging.getLogger(__name__)


def create_tables() -> None:
    try:
        engine = get_engine()

        Base.metadata.create_all(engine)
        logger.debug("Database schema successfully created.")

    except SQLAlchemyError as exc:
        logger.error("Error creating database schema: %s", exc)
        raise


if __name__ == "__main__":
    create_tables()
