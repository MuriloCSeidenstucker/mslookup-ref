from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass
class Drug:
    registration_number: str

    product_name: str
    product_name_normalized: str

    active_ingredient: Optional[str]
    active_ingredient_normalized: Optional[str]

    regulatory_category: str
    regulatory_category_normalized: str

    registration_holder: str
    registration_holder_normalized: str

    registration_status: str
    registration_expiration_date: Optional[date]
    is_registration_valid: bool
