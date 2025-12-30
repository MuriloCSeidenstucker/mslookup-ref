from abc import ABC, abstractmethod
from typing import Iterable

from src.domain.models.drugs import Drug


class DrugsRepositoryInterface(ABC):

    @abstractmethod
    def insert_drugs(self, drugs: Iterable[Drug]) -> None:
        raise NotImplementedError

    @abstractmethod
    def find_drugs(
        self,
        *,
        product_name_normalized: str,
        active_ingredient_normalized: str | None = None,
        registration_holder_normalized: str | None = None,
        only_valid: bool = True,
        limit: int = 20,
    ) -> list[Drug]:
        raise NotImplementedError
