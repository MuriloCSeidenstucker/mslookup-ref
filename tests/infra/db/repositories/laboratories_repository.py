# pylint: disable=R0903:too-few-public-methods, C0301:line-too-long, C0115:missing-class-docstring, C0116:missing-function-docstring

from mslookup_ref.domain.models.laboratories import Laboratories


class LaboratoriesRepositorySpy:

    def __init__(self) -> None:
        self.insert_laboratory_attributes = {}
        self.select_laboratory_attributes = {}

    def insert_laboratory(self, laboratory: Laboratories) -> None:
        self.insert_laboratory_attributes["laboratory"] = laboratory

    def select_laboratory(self, cnpj: str) -> Laboratories:
        self.select_laboratory_attributes["cnpj"] = cnpj
        return Laboratories(
            full_name = "laboratory_spy_1",
            cnpj = "12345678901234",
            alt_names = ["lab_spy_1", "laborat_spy_1"],
            linked = ["laboratory_spy_linked_1"],
        )
