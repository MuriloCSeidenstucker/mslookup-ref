import pytest

from src.infra.db.settings import DBConnectionHandler


@pytest.mark.skip(reason="sensitive test")
def test_create_database_engine():
    """Teste para verificar se a engine de conexão ao banco de dados é criada corretamente.

    Skipped:
        Este teste está sendo ignorado devido a questões sensíveis relacionadas ao banco de dados.
    """
    db_connection_handler = DBConnectionHandler()
    engine = db_connection_handler.get_engine()

    assert engine is not None
