from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass
class Drug:
    registration_number: Optional[str]
    product_name: str
    active_ingredient: Optional[str]
    regulatory_category: str
    registration_holder: str
    registration_status: str
    registration_expiration_date: Optional[date]
    is_registration_valid: bool
