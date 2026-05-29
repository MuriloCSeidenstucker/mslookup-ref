import pytest
import requests

import src.tasks.downloader as module


class FakeResponse:
    def __init__(self, status_code=200, content=b"data"):
        self.status_code = status_code
        self.content = content


def test_download_success(mocker, tmp_path):
    url = "https://anvisa.gov.br/file.csv"
    destination = tmp_path / "anvisa.csv"

    mocker.patch(
        "src.tasks.downloader.requests.get",
        return_value=FakeResponse(status_code=200, content=b"csv-content"),
    )

    logger = mocker.patch("src.tasks.downloader.logger")

    result = module.download_anvisa_csv(url, destination)

    assert result == destination
    assert destination.exists()
    assert destination.read_bytes() == b"csv-content"

    logger.info.assert_any_call("Download completed successfully")
    logger.info.assert_any_call("File saved to: %s", destination)


def test_download_creates_parent_directories(mocker, tmp_path):
    url = "https://anvisa.gov.br/file.csv"
    destination = tmp_path / "nested" / "dir" / "file.csv"

    mocker.patch(
        "src.tasks.downloader.requests.get",
        return_value=FakeResponse(),
    )

    module.download_anvisa_csv(url, destination)

    assert destination.parent.exists()
    assert destination.exists()


def test_download_request_exception_raises_download_error(mocker, tmp_path):
    mocker.patch(
        "src.tasks.downloader.requests.get",
        side_effect=requests.RequestException("network error"),
    )

    logger = mocker.patch("src.tasks.downloader.logger")

    with pytest.raises(module.DownloadError) as exc:
        module.download_anvisa_csv(
            "https://anvisa.gov.br/file.csv",
            tmp_path / "file.csv",
        )

    assert "Failed to connect to ANVISA source" in str(exc.value)
    logger.error.assert_any_call("Request to ANVISA failed")


@pytest.mark.parametrize("status_code", [400, 401, 403, 404, 500])
def test_download_invalid_status_code_raises_error(mocker, tmp_path, status_code):
    mocker.patch(
        "src.tasks.downloader.requests.get",
        return_value=FakeResponse(status_code=status_code, content=b"error"),
    )

    logger = mocker.patch("src.tasks.downloader.logger")

    with pytest.raises(module.DownloadError) as exc:
        module.download_anvisa_csv(
            "https://anvisa.gov.br/file.csv",
            tmp_path / "file.csv",
        )

    assert f"Unexpected status code: {status_code}" in str(exc.value)
    logger.error.assert_any_call(
        "Unexpected HTTP status code: %s",
        status_code,
    )


def test_download_empty_content_raises_error(mocker, tmp_path):
    mocker.patch(
        "src.tasks.downloader.requests.get",
        return_value=FakeResponse(status_code=200, content=b""),
    )

    logger = mocker.patch("src.tasks.downloader.logger")

    with pytest.raises(module.DownloadError) as exc:
        module.download_anvisa_csv(
            "https://anvisa.gov.br/file.csv",
            tmp_path / "file.csv",
        )

    assert "Downloaded file is empty" in str(exc.value)
    logger.error.assert_any_call("Downloaded file is empty")


def test_download_passes_timeout_and_verify_flag(mocker, tmp_path):
    get_mock = mocker.patch(
        "src.tasks.downloader.requests.get",
        return_value=FakeResponse(),
    )

    module.download_anvisa_csv(
        "https://anvisa.gov.br/file.csv",
        tmp_path / "file.csv",
        timeout=10,
    )

    get_mock.assert_called_once_with(
        "https://anvisa.gov.br/file.csv",
        timeout=10,
        verify=False,
    )
