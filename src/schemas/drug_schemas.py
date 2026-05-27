from pydantic import BaseModel, Field


class DrugAttributesSchema(BaseModel):
    registration_number: str = Field(..., examples=["123456789"])
    product_name: str = Field(..., examples=["AMOXICILINA"])
    active_ingredient: str = Field(..., examples=["AMOXICILINA TRI-hIDRATADA"])
    registration_holder: str = Field(..., examples=["PRATI DONADUZZI & CIA LTDA"])
    regulatory_category: str = Field(..., examples=["Genérico"])
    expiration_date: str | None = Field(..., examples=["99/99/9999"])


class DrugResponseSchema(BaseModel):
    count: int
    data: list[DrugAttributesSchema]
