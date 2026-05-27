from pytest_mock import MockerFixture


def test_db_connection(mocker: MockerFixture):
    mocker.patch("src.infra.db.settings.connection.Session")
