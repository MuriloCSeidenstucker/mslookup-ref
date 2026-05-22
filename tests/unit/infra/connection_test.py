from pytest_mock import MockerFixture

from src.infra.db.settings.connection import DBConnectionHandler


def test_db_connection_handler_init(mocker: MockerFixture):
    mock_create_engine = mocker.patch("src.infra.db.settings.connection.create_engine")
    mock_engine = mocker.MagicMock()
    mock_create_engine.return_value = mock_engine

    handler = DBConnectionHandler()

    mock_create_engine.assert_called_once_with("sqlite:///mslookup.db")
    assert handler.get_engine() == mock_engine
    assert handler.session is None


def test_db_connection_handler_context_manager(mocker: MockerFixture):
    mock_create_engine = mocker.patch("src.infra.db.settings.connection.create_engine")
    mock_engine = mocker.MagicMock()
    mock_create_engine.return_value = mock_engine
    mock_sessionmaker = mocker.patch("src.infra.db.settings.connection.sessionmaker")
    mock_session_maker_instance = mocker.MagicMock()
    mock_sessionmaker.return_value = mock_session_maker_instance
    mock_session = mocker.MagicMock()
    mock_session_maker_instance.return_value = mock_session

    with DBConnectionHandler() as handler:
        assert handler.session == mock_session

    mock_session.close.assert_called_once()
    mock_sessionmaker.assert_called_once_with(bind=mock_engine)
