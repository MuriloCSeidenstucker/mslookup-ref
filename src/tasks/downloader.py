import logging
from pathlib import Path

import requests

logger = logging.getLogger(__name__)


class DownloadError(Exception):
    """Raised when the CSV download fails."""


def download_anvisa_csv(
    url: str,
    destination_path: Path,
    timeout: int = 30,
) -> Path:
    logger.info("Starting download from ANVISA source")
    logger.info("Source URL: %s", url)

    destination_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        response = requests.get(url, timeout=timeout, verify=False)
    except requests.RequestException as exc:
        logger.error("Request to ANVISA failed")
        raise DownloadError("Failed to connect to ANVISA source") from exc

    if response.status_code != 200:
        logger.error(
            "Unexpected HTTP status code: %s",
            response.status_code,
        )
        raise DownloadError(f"Unexpected status code: {response.status_code}")

    if not response.content:
        logger.error("Downloaded file is empty")
        raise DownloadError("Downloaded file is empty")

    destination_path.write_bytes(response.content)

    file_size = destination_path.stat().st_size
    logger.info("Download completed successfully")
    logger.info("File saved to: %s", destination_path)
    logger.info("File size: %d bytes", file_size)

    return destination_path
