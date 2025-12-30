# pylint: disable=R0903:too-few-public-methods

from abc import ABC, abstractmethod
from typing import Dict, Optional


class DrugFinderInterface(ABC):

    @abstractmethod
    def find(
        self,
        *,
        name: str,
        active_ingredient: Optional[str] = None,
        registration_holder: Optional[str] = None,
    ) -> Dict:
        raise NotImplementedError
