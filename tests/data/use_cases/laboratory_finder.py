# pylint: disable=C0115:missing-class-docstring, R0903:too-few-public-methods, C0116:missing-function-docstring

from typing import Dict


class LaboratoryFinderSpy:

    def __init__(self) -> None:
        self.find_attributes = {}

    def find(self, cnpj: str) -> Dict:

        self.find_attributes["cnpj"] = cnpj

        attributes = {
            "full_name": "laboratory_1",
            "cnpj": cnpj,
            "alt_names": ["lab_1", "laborat_1"],
            "linked": ["laboratory_linked_1"],
        }

        response = {"type": "Medicines", "attributes": attributes}
        return response
