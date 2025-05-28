# pylint: disable=C0115:missing-class-docstring, R0903:too-few-public-methods, C0116:missing-function-docstring

from typing import Dict

from mslookup_ref.domain.models.laboratories import Laboratories


class LaboratoryRegisterSpy:

    def __init__(self) -> None:
        self.find_attributes = {}

    def register(self, laboratory: Laboratories) -> Dict:
        self.find_attributes["laboratory"] = laboratory

        response = {"type": "Laboratories", "attributes": laboratory}
        return response
