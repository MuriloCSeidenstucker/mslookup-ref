from pytest_mock import MockerFixture
from src.ingest.downloader import download_anvisa_csv


def test_download_anvisa_csv(mocker: MockerFixture, tmp_path):
    mock_get = mocker.patch("src.ingest.downloader.requests.get")
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.content = b"col1,col2\nval1,val2"
    mock_get.return_value = mock_response

    test_path = tmp_path / "medicamentos.csv"

    response = download_anvisa_csv(
        url="https://fake-url.com/dados.csv",
        destination_path=test_path,
    )

    assert response.exists()
    assert response.read_bytes() == b"col1,col2\nval1,val2"
    mock_get.assert_called_once_with(
        "https://fake-url.com/dados.csv", 
        timeout=30,
        verify=False
    )
