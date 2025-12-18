import unicodedata
import re
from typing import Optional


_whitespace_re = re.compile(r"\s+")


def normalize_text(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None

    value = value.strip()

    if not value:
        return None

    value = value.lower()

    value = unicodedata.normalize("NFKD", value)
    value = "".join(
        char for char in value if not unicodedata.combining(char)
    )

    value = _whitespace_re.sub(" ", value)

    return value
